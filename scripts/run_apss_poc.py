from __future__ import annotations

import argparse
import json
import math
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Callable

import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parents[1]


@dataclass
class FittedModel:
    model_id: str
    feature_names: list[str]
    beta: np.ndarray
    intercept: float
    mean: np.ndarray
    std: np.ndarray
    thresholds: np.ndarray
    classes: list[int]
    complexity_units: float
    selected_interactions: list[tuple[str, str]]
    nonmonotone_criteria: list[str]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="APSS proof-of-concept benchmark runner")
    parser.add_argument("--manifest", default="data/metadata/bench_manifest.csv")
    parser.add_argument("--out-dir", default="")
    parser.add_argument(
        "--groups",
        nargs="+",
        default=["synthetic_structure_recovery", "monotone_classification"],
        help="Dataset groups from bench_manifest.csv",
    )
    parser.add_argument("--seeds", type=int, default=5)
    parser.add_argument("--max-interactions", type=int, default=4)
    parser.add_argument(
        "--interaction-selection",
        choices=["topk", "forward"],
        default="topk",
        help="How M4/M5 choose candidate interactions.",
    )
    parser.add_argument(
        "--interaction-candidate-pool",
        type=int,
        default=40,
        help="Candidate pair pool for forward interaction selection; <=0 means all pairs.",
    )
    parser.add_argument(
        "--interaction-gain-threshold",
        type=float,
        default=0.0,
        help="Minimum validation-objective improvement required to add one interaction in forward mode.",
    )
    parser.add_argument("--ridge-alpha", type=float, default=1.0)
    parser.add_argument("--complexity-lambda", type=float, default=0.02)
    parser.add_argument("--train-frac", type=float, default=0.60)
    parser.add_argument("--val-frac", type=float, default=0.20)
    parser.add_argument("--limit-datasets", nargs="*", default=None)
    return parser.parse_args()


def criteria_columns(df: pd.DataFrame) -> list[str]:
    return [c for c in df.columns if c.startswith("g") and c[1:].isdigit()]


def stratified_split(
    y: np.ndarray,
    seed: int,
    train_frac: float,
    val_frac: float,
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    rng = np.random.default_rng(seed)
    train_idx: list[int] = []
    val_idx: list[int] = []
    test_idx: list[int] = []
    for cls in sorted(np.unique(y).tolist()):
        idx = np.where(y == cls)[0].copy()
        rng.shuffle(idx)
        n = len(idx)
        n_train = max(1, int(round(n * train_frac)))
        n_val = max(1, int(round(n * val_frac))) if n - n_train > 1 else 0
        if n_train + n_val >= n:
            n_val = max(0, n - n_train - 1)
        train_idx.extend(idx[:n_train].tolist())
        val_idx.extend(idx[n_train : n_train + n_val].tolist())
        test_idx.extend(idx[n_train + n_val :].tolist())
    return np.array(train_idx), np.array(val_idx), np.array(test_idx)


def standardize_fit(X: np.ndarray) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    mean = X.mean(axis=0)
    std = X.std(axis=0)
    std[std < 1e-12] = 1.0
    return (X - mean) / std, mean, std


def standardize_apply(X: np.ndarray, mean: np.ndarray, std: np.ndarray) -> np.ndarray:
    return (X - mean) / std


def ridge_fit(X: np.ndarray, y: np.ndarray, alpha: float) -> tuple[np.ndarray, float, np.ndarray, np.ndarray]:
    Xs, mean, std = standardize_fit(X)
    yc = y.astype(float)
    y_mean = float(yc.mean())
    y_centered = yc - y_mean
    gram = Xs.T @ Xs
    penalty = np.eye(gram.shape[0]) * alpha
    beta = np.linalg.pinv(gram + penalty) @ Xs.T @ y_centered
    return beta, y_mean, mean, std


def nonnegative_ridge_fit(
    X: np.ndarray,
    y: np.ndarray,
    alpha: float,
    max_iter: int = 500,
    tol: float = 1e-8,
) -> tuple[np.ndarray, float, np.ndarray, np.ndarray]:
    Xs, mean, std = standardize_fit(X)
    yc = y.astype(float)
    y_mean = float(yc.mean())
    residual = yc - y_mean
    n_features = Xs.shape[1]
    beta = np.zeros(n_features, dtype=float)
    denom = (Xs * Xs).sum(axis=0) + alpha
    for _ in range(max_iter):
        old = beta.copy()
        for j in range(n_features):
            residual = residual + Xs[:, j] * beta[j]
            beta[j] = max(0.0, float(Xs[:, j] @ residual) / float(denom[j]))
            residual = residual - Xs[:, j] * beta[j]
        if np.max(np.abs(beta - old)) < tol:
            break
    return beta, y_mean, mean, std


def make_thresholds(scores: np.ndarray, y: np.ndarray, classes: list[int]) -> np.ndarray:
    means = []
    for cls in classes:
        cls_scores = scores[y == cls]
        means.append(float(cls_scores.mean()) if len(cls_scores) else np.nan)
    means_arr = np.array(means, dtype=float)
    if np.all(np.isfinite(means_arr)) and np.all(np.diff(means_arr) > 1e-10):
        return (means_arr[:-1] + means_arr[1:]) / 2

    thresholds = []
    counts = np.array([np.sum(y == cls) for cls in classes], dtype=float)
    cum_props = np.cumsum(counts / counts.sum())[:-1]
    for q in cum_props:
        thresholds.append(float(np.quantile(scores, q)))
    return np.array(thresholds, dtype=float)


def predict_scores(model: FittedModel, X: np.ndarray) -> np.ndarray:
    Xs = standardize_apply(X, model.mean, model.std)
    return Xs @ model.beta + model.intercept


def predict_classes(model: FittedModel, X: np.ndarray) -> np.ndarray:
    scores = predict_scores(model, X)
    class_min = min(model.classes)
    pred = np.digitize(scores, model.thresholds, right=False) + class_min
    return np.clip(pred, min(model.classes), max(model.classes)).astype(int)


def macro_f1(y_true: np.ndarray, y_pred: np.ndarray, classes: list[int]) -> float:
    f1s = []
    for cls in classes:
        tp = np.sum((y_true == cls) & (y_pred == cls))
        fp = np.sum((y_true != cls) & (y_pred == cls))
        fn = np.sum((y_true == cls) & (y_pred != cls))
        precision = tp / (tp + fp) if tp + fp else 0.0
        recall = tp / (tp + fn) if tp + fn else 0.0
        f1 = 2 * precision * recall / (precision + recall) if precision + recall else 0.0
        f1s.append(f1)
    return float(np.mean(f1s))


def balanced_accuracy(y_true: np.ndarray, y_pred: np.ndarray, classes: list[int]) -> float:
    recalls = []
    for cls in classes:
        mask = y_true == cls
        recalls.append(float(np.mean(y_pred[mask] == cls)) if np.any(mask) else 0.0)
    return float(np.mean(recalls))


def metrics(y_true: np.ndarray, y_pred: np.ndarray, classes: list[int]) -> dict[str, float]:
    return {
        "accuracy": float(np.mean(y_true == y_pred)),
        "macro_f1": macro_f1(y_true, y_pred, classes),
        "balanced_accuracy": balanced_accuracy(y_true, y_pred, classes),
        "ordinal_mae": float(np.mean(np.abs(y_true - y_pred))),
        "within_one_accuracy": float(np.mean(np.abs(y_true - y_pred) <= 1)),
    }


def base_feature_matrix(X: np.ndarray, names: list[str]) -> tuple[np.ndarray, list[str]]:
    return X.copy(), names.copy()


def quadratic_feature_matrix(X: np.ndarray, names: list[str]) -> tuple[np.ndarray, list[str]]:
    parts = [X]
    feature_names = names.copy()
    parts.append(X**2)
    feature_names.extend([f"{name}^2" for name in names])
    return np.column_stack(parts), feature_names


def rank_interaction_candidates(
    X: np.ndarray,
    y: np.ndarray,
    names: list[str],
    alpha: float,
    residual_builder: Callable[[np.ndarray, list[str]], tuple[np.ndarray, list[str]]],
    candidate_pool: int,
) -> list[tuple[int, int]]:
    base_X, _ = residual_builder(X, names)
    beta, intercept, mean, std = ridge_fit(base_X, y, alpha)
    residual = y.astype(float) - (standardize_apply(base_X, mean, std) @ beta + intercept)
    scored: list[tuple[float, int, int]] = []
    for i in range(X.shape[1]):
        for j in range(i + 1, X.shape[1]):
            z = X[:, i] * X[:, j]
            zc = z - z.mean()
            denom = float(np.sqrt(np.sum(zc**2)) * np.sqrt(np.sum((residual - residual.mean()) ** 2)))
            score = abs(float(zc @ (residual - residual.mean())) / denom) if denom > 1e-12 else 0.0
            scored.append((score, i, j))
    scored.sort(reverse=True)
    if candidate_pool > 0:
        scored = scored[:candidate_pool]
    return [(i, j) for _, i, j in scored]


def select_topk_interactions(
    X: np.ndarray,
    y: np.ndarray,
    names: list[str],
    alpha: float,
    max_interactions: int,
    residual_builder: Callable[[np.ndarray, list[str]], tuple[np.ndarray, list[str]]],
) -> list[tuple[int, int]]:
    return rank_interaction_candidates(
        X,
        y,
        names,
        alpha,
        residual_builder,
        candidate_pool=max_interactions,
    )


def val_ordinal_mae_for_interactions(
    X_train_raw: np.ndarray,
    y_train: np.ndarray,
    X_val_raw: np.ndarray,
    y_val: np.ndarray,
    criteria: list[str],
    classes: list[int],
    alpha: float,
    pairs: list[tuple[int, int]],
    include_quadratic: bool,
) -> float:
    X_train, _ = interaction_feature_matrix(X_train_raw, criteria, pairs, include_quadratic=include_quadratic)
    beta, intercept, mean, std = ridge_fit(X_train, y_train, alpha)
    train_scores = standardize_apply(X_train, mean, std) @ beta + intercept
    thresholds = make_thresholds(train_scores, y_train, classes)
    X_val, _ = interaction_feature_matrix(X_val_raw, criteria, pairs, include_quadratic=include_quadratic)
    val_scores = standardize_apply(X_val, mean, std) @ beta + intercept
    class_min = min(classes)
    pred = np.digitize(val_scores, thresholds, right=False) + class_min
    pred = np.clip(pred, min(classes), max(classes)).astype(int)
    return float(np.mean(np.abs(y_val - pred)))


def select_forward_interactions(
    X_train_raw: np.ndarray,
    y_train: np.ndarray,
    X_val_raw: np.ndarray,
    y_val: np.ndarray,
    criteria: list[str],
    classes: list[int],
    alpha: float,
    max_interactions: int,
    residual_builder: Callable[[np.ndarray, list[str]], tuple[np.ndarray, list[str]]],
    include_quadratic: bool,
    complexity_lambda: float,
    candidate_pool: int,
    gain_threshold: float,
) -> list[tuple[int, int]]:
    if max_interactions <= 0 or X_train_raw.shape[1] < 2 or len(y_val) == 0:
        return []

    pool_size = candidate_pool if candidate_pool <= 0 else max(candidate_pool, max_interactions)
    candidates = rank_interaction_candidates(
        X_train_raw,
        y_train,
        criteria,
        alpha,
        residual_builder,
        candidate_pool=pool_size,
    )
    selected: list[tuple[int, int]] = []
    pair_penalty = complexity_lambda / max(1, len(criteria))

    def objective(pairs: list[tuple[int, int]]) -> float:
        mae = val_ordinal_mae_for_interactions(
            X_train_raw,
            y_train,
            X_val_raw,
            y_val,
            criteria,
            classes,
            alpha,
            pairs,
            include_quadratic,
        )
        return mae + pair_penalty * len(pairs)

    current_objective = objective(selected)
    for _ in range(max_interactions):
        best_pair: tuple[int, int] | None = None
        best_objective = current_objective
        for pair in candidates:
            if pair in selected:
                continue
            candidate_pairs = selected + [pair]
            candidate_objective = objective(candidate_pairs)
            if candidate_objective < best_objective:
                best_pair = pair
                best_objective = candidate_objective
        if best_pair is None or current_objective - best_objective <= gain_threshold:
            break
        selected.append(best_pair)
        current_objective = best_objective
    return selected


def interaction_feature_matrix(
    X: np.ndarray,
    names: list[str],
    pairs: list[tuple[int, int]],
    include_quadratic: bool = False,
) -> tuple[np.ndarray, list[str]]:
    if include_quadratic:
        base_X, feature_names = quadratic_feature_matrix(X, names)
    else:
        base_X, feature_names = base_feature_matrix(X, names)
    parts = [base_X]
    for i, j in pairs:
        parts.append((X[:, i] * X[:, j]).reshape(-1, 1))
        feature_names.append(f"{names[i]}:{names[j]}")
    return np.column_stack(parts), feature_names


def detect_nonmonotone(
    model_id: str,
    feature_names: list[str],
    beta: np.ndarray,
    criteria: list[str],
    mean: np.ndarray,
    std: np.ndarray,
) -> list[str]:
    if model_id not in {"M3_nonmonotone_additive", "M5_full_flexible"}:
        return []
    coef = {name: beta[idx] / std[idx] for idx, name in enumerate(feature_names)}
    detected = []
    for name in criteria:
        b1 = float(coef.get(name, 0.0))
        b2 = float(coef.get(f"{name}^2", 0.0))
        deriv_0 = b1
        deriv_1 = b1 + 2 * b2
        if abs(b2) > 1e-6 and deriv_0 * deriv_1 < 0:
            detected.append(name)
    return detected


def fit_model(
    model_id: str,
    X_train_raw: np.ndarray,
    y_train: np.ndarray,
    X_val_raw: np.ndarray,
    y_val: np.ndarray,
    criteria: list[str],
    classes: list[int],
    alpha: float,
    max_interactions: int,
    complexity_lambda: float,
    interaction_selection: str,
    interaction_candidate_pool: int,
    interaction_gain_threshold: float,
) -> FittedModel:
    pairs: list[tuple[int, int]] = []
    if model_id == "M1_linear_additive":
        X_train, feature_names = base_feature_matrix(X_train_raw, criteria)
        beta, intercept, mean, std = ridge_fit(X_train, y_train, alpha)
        complexity_units = 0.0
    elif model_id == "M2_monotone_additive":
        X_train, feature_names = base_feature_matrix(X_train_raw, criteria)
        beta, intercept, mean, std = nonnegative_ridge_fit(X_train, y_train, alpha)
        complexity_units = 0.10
    elif model_id == "M3_nonmonotone_additive":
        X_train, feature_names = quadratic_feature_matrix(X_train_raw, criteria)
        beta, intercept, mean, std = ridge_fit(X_train, y_train, alpha)
        complexity_units = 1.0
    elif model_id == "M4_sparse_interaction":
        if interaction_selection == "forward":
            pairs = select_forward_interactions(
                X_train_raw,
                y_train,
                X_val_raw,
                y_val,
                criteria,
                classes,
                alpha,
                max_interactions,
                base_feature_matrix,
                include_quadratic=False,
                complexity_lambda=complexity_lambda,
                candidate_pool=interaction_candidate_pool,
                gain_threshold=interaction_gain_threshold,
            )
        else:
            pairs = select_topk_interactions(X_train_raw, y_train, criteria, alpha, max_interactions, base_feature_matrix)
        X_train, feature_names = interaction_feature_matrix(X_train_raw, criteria, pairs, include_quadratic=False)
        beta, intercept, mean, std = ridge_fit(X_train, y_train, alpha)
        complexity_units = 1.0 + len(pairs) / max(1, len(criteria))
    elif model_id == "M5_full_flexible":
        if interaction_selection == "forward":
            pairs = select_forward_interactions(
                X_train_raw,
                y_train,
                X_val_raw,
                y_val,
                criteria,
                classes,
                alpha,
                max_interactions,
                quadratic_feature_matrix,
                include_quadratic=True,
                complexity_lambda=complexity_lambda,
                candidate_pool=interaction_candidate_pool,
                gain_threshold=interaction_gain_threshold,
            )
        else:
            pairs = select_topk_interactions(X_train_raw, y_train, criteria, alpha, max_interactions, quadratic_feature_matrix)
        X_train, feature_names = interaction_feature_matrix(X_train_raw, criteria, pairs, include_quadratic=True)
        beta, intercept, mean, std = ridge_fit(X_train, y_train, alpha)
        complexity_units = 2.0 + len(pairs) / max(1, len(criteria))
    else:
        raise ValueError(f"Unknown model_id: {model_id}")

    train_scores = standardize_apply(X_train, mean, std) @ beta + intercept
    thresholds = make_thresholds(train_scores, y_train, classes)
    selected_interactions = [(criteria[i], criteria[j]) for i, j in pairs]
    nonmono = detect_nonmonotone(model_id, feature_names, beta, criteria, mean, std)
    return FittedModel(
        model_id=model_id,
        feature_names=feature_names,
        beta=beta,
        intercept=intercept,
        mean=mean,
        std=std,
        thresholds=thresholds,
        classes=classes,
        complexity_units=complexity_units,
        selected_interactions=selected_interactions,
        nonmonotone_criteria=nonmono,
    )


def transform_for_model(model: FittedModel, X_raw: np.ndarray, criteria: list[str]) -> np.ndarray:
    columns = []
    raw_by_name = {name: X_raw[:, idx] for idx, name in enumerate(criteria)}
    for feature in model.feature_names:
        if feature.endswith("^2"):
            base = feature[:-2]
            columns.append(raw_by_name[base] ** 2)
        elif ":" in feature:
            left, right = feature.split(":", 1)
            columns.append(raw_by_name[left] * raw_by_name[right])
        else:
            columns.append(raw_by_name[feature])
    return np.column_stack(columns)


def eval_model(model: FittedModel, X_raw: np.ndarray, y: np.ndarray, criteria: list[str]) -> dict[str, float]:
    X = transform_for_model(model, X_raw, criteria)
    pred = predict_classes(model, X)
    return metrics(y, pred, model.classes)


def majority_predict(y_train: np.ndarray, n: int) -> np.ndarray:
    values, counts = np.unique(y_train, return_counts=True)
    return np.repeat(values[np.argmax(counts)], n)


def prf_sets(pred: set[tuple[str, str]] | set[str], true: set[tuple[str, str]] | set[str]) -> dict[str, float]:
    tp = len(pred & true)
    fp = len(pred - true)
    fn = len(true - pred)
    precision = tp / (tp + fp) if tp + fp else (1.0 if not true and not pred else 0.0)
    recall = tp / (tp + fn) if tp + fn else (1.0 if not true and not pred else 0.0)
    f1 = 2 * precision * recall / (precision + recall) if precision + recall else 0.0
    return {"precision": precision, "recall": recall, "f1": f1, "tp": tp, "fp": fp, "fn": fn}


def parse_truth(raw_truth: str) -> tuple[set[str], set[tuple[str, str]]]:
    if not isinstance(raw_truth, str) or not raw_truth.strip().startswith("{"):
        return set(), set()
    truth = json.loads(raw_truth)
    nonmono = {
        criterion
        for criterion, shape in truth.get("marginal_shapes", {}).items()
        if shape != "monotone_increasing_linear"
    }
    interactions = set()
    for item in truth.get("interactions", []):
        criteria = sorted(item["criteria"])
        interactions.add((criteria[0], criteria[1]))
    return nonmono, interactions


def run_dataset(
    row: pd.Series,
    seeds: int,
    train_frac: float,
    val_frac: float,
    alpha: float,
    max_interactions: int,
    complexity_lambda: float,
    interaction_selection: str,
    interaction_candidate_pool: int,
    interaction_gain_threshold: float,
) -> tuple[list[dict[str, object]], list[dict[str, object]]]:
    path = ROOT / row["processed_path"]
    df = pd.read_csv(path)
    criteria = criteria_columns(df)
    X = df[criteria].to_numpy(dtype=float)
    y = df["class_index"].to_numpy(dtype=int)
    classes = sorted(np.unique(y).astype(int).tolist())
    model_ids = [
        "M1_linear_additive",
        "M2_monotone_additive",
        "M3_nonmonotone_additive",
        "M4_sparse_interaction",
        "M5_full_flexible",
    ]
    result_rows: list[dict[str, object]] = []
    structure_rows: list[dict[str, object]] = []
    truth_nonmono, truth_interactions = parse_truth(str(row.get("structural_truth", "")))

    for split_seed in range(seeds):
        seed = 20260629 + split_seed
        train_idx, val_idx, test_idx = stratified_split(y, seed, train_frac, val_frac)
        X_train, y_train = X[train_idx], y[train_idx]
        X_val, y_val = X[val_idx], y[val_idx]
        X_test, y_test = X[test_idx], y[test_idx]

        m0_pred_val = majority_predict(y_train, len(y_val))
        m0_pred_test = majority_predict(y_train, len(y_test))
        m0_val = metrics(y_val, m0_pred_val, classes)
        m0_test = metrics(y_test, m0_pred_test, classes)
        result_rows.append(
            {
                "dataset_id": row["dataset_id"],
                "group": row["group"],
                "seed": split_seed,
                "model_id": "M0_majority",
                "selected_by_apss": False,
                "selected_base_model": "",
                "complexity_units": 0.0,
                **{f"val_{k}": v for k, v in m0_val.items()},
                **{f"test_{k}": v for k, v in m0_test.items()},
                "nonmonotone_criteria": "",
                "selected_interactions": "",
            }
        )

        candidates: list[tuple[FittedModel, dict[str, float], dict[str, float]]] = []
        for model_id in model_ids:
            model = fit_model(
                model_id,
                X_train,
                y_train,
                X_val,
                y_val,
                criteria,
                classes,
                alpha,
                max_interactions,
                complexity_lambda,
                interaction_selection,
                interaction_candidate_pool,
                interaction_gain_threshold,
            )
            val_metrics = eval_model(model, X_val, y_val, criteria)
            test_metrics = eval_model(model, X_test, y_test, criteria)
            candidates.append((model, val_metrics, test_metrics))
            result_rows.append(
                {
                    "dataset_id": row["dataset_id"],
                    "group": row["group"],
                    "seed": split_seed,
                    "model_id": model.model_id,
                    "selected_by_apss": False,
                    "selected_base_model": "",
                    "complexity_units": model.complexity_units,
                    **{f"val_{k}": v for k, v in val_metrics.items()},
                    **{f"test_{k}": v for k, v in test_metrics.items()},
                    "nonmonotone_criteria": ";".join(model.nonmonotone_criteria),
                    "selected_interactions": ";".join(f"{a}:{b}" for a, b in model.selected_interactions),
                }
            )

        best_model, best_val, best_test = min(
            candidates,
            key=lambda item: item[1]["ordinal_mae"] + complexity_lambda * item[0].complexity_units,
        )
        result_rows.append(
            {
                "dataset_id": row["dataset_id"],
                "group": row["group"],
                "seed": split_seed,
                "model_id": "M6_APSS",
                "selected_by_apss": True,
                "selected_base_model": best_model.model_id,
                "complexity_units": best_model.complexity_units,
                **{f"val_{k}": v for k, v in best_val.items()},
                **{f"test_{k}": v for k, v in best_test.items()},
                "nonmonotone_criteria": ";".join(best_model.nonmonotone_criteria),
                "selected_interactions": ";".join(f"{a}:{b}" for a, b in best_model.selected_interactions),
            }
        )

        if row["group"] == "synthetic_structure_recovery":
            pred_nonmono = set(best_model.nonmonotone_criteria)
            pred_interactions = {tuple(sorted(pair)) for pair in best_model.selected_interactions}
            nm = prf_sets(pred_nonmono, truth_nonmono)
            inter = prf_sets(pred_interactions, truth_interactions)
            structure_rows.append(
                {
                    "dataset_id": row["dataset_id"],
                    "seed": split_seed,
                    "selected_base_model": best_model.model_id,
                    "true_nonmonotone": ";".join(sorted(truth_nonmono)),
                    "pred_nonmonotone": ";".join(sorted(pred_nonmono)),
                    "nonmonotone_precision": nm["precision"],
                    "nonmonotone_recall": nm["recall"],
                    "nonmonotone_f1": nm["f1"],
                    "true_interactions": ";".join(f"{a}:{b}" for a, b in sorted(truth_interactions)),
                    "pred_interactions": ";".join(f"{a}:{b}" for a, b in sorted(pred_interactions)),
                    "interaction_precision": inter["precision"],
                    "interaction_recall": inter["recall"],
                    "interaction_f1": inter["f1"],
                    "false_complexity_count": len(pred_nonmono - truth_nonmono)
                    + len(pred_interactions - truth_interactions),
                }
            )

    return result_rows, structure_rows


def summarize_results(results: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    metric_cols = [
        "test_accuracy",
        "test_macro_f1",
        "test_balanced_accuracy",
        "test_ordinal_mae",
        "test_within_one_accuracy",
        "val_ordinal_mae",
        "complexity_units",
    ]
    summary = (
        results.groupby(["group", "dataset_id", "model_id"], dropna=False)[metric_cols]
        .agg(["mean", "std"])
        .reset_index()
    )
    summary.columns = [
        "_".join([str(part) for part in col if part != ""]).rstrip("_")
        if isinstance(col, tuple)
        else str(col)
        for col in summary.columns
    ]

    apss = results[results["model_id"] == "M6_APSS"].copy()
    selection = (
        apss.groupby(["group", "dataset_id", "selected_base_model"])
        .size()
        .reset_index(name="count")
    )
    selection["frequency"] = selection["count"] / selection.groupby(["group", "dataset_id"])["count"].transform("sum")
    return summary, selection


def dataframe_to_markdown(df: pd.DataFrame) -> str:
    if df.empty:
        return "_Empty table._"
    display = df.copy()
    for col in display.columns:
        if pd.api.types.is_float_dtype(display[col]):
            display[col] = display[col].map(lambda value: f"{value:.4f}")
        else:
            display[col] = display[col].astype(str)
    headers = [str(c) for c in display.columns]
    lines = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join(["---"] * len(headers)) + " |",
    ]
    for _, row in display.iterrows():
        lines.append("| " + " | ".join(str(row[col]) for col in display.columns) + " |")
    return "\n".join(lines)


def write_markdown_report(
    out_dir: Path,
    args: argparse.Namespace,
    results: pd.DataFrame,
    summary: pd.DataFrame,
    selection: pd.DataFrame,
    structure: pd.DataFrame,
    elapsed: float,
) -> None:
    lines = [
        "# APSS Proof-of-Concept Run",
        "",
        "## Material Passport",
        "",
        "- Origin Skill: academic-research-suite / experiment-agent",
        "- Origin Mode: run",
        "- Verification Status: ANALYZED",
        "- Version Label: apss_poc_v2",
        f"- Runtime Seconds: {elapsed:.2f}",
        "",
        "## Configuration",
        "",
        f"- groups: `{', '.join(args.groups)}`",
        f"- seeds per dataset: `{args.seeds}`",
        f"- ridge alpha: `{args.ridge_alpha}`",
        f"- max interactions: `{args.max_interactions}`",
        f"- interaction selection: `{args.interaction_selection}`",
        f"- interaction candidate pool: `{args.interaction_candidate_pool}`",
        f"- interaction gain threshold: `{args.interaction_gain_threshold}`",
        f"- complexity lambda: `{args.complexity_lambda}`",
        "",
        "## Files",
        "",
        "- `split_results.csv`: every dataset/seed/model result.",
        "- `summary_by_dataset_model.csv`: mean/std summary.",
        "- `apss_selection_frequencies.csv`: selected base model frequencies.",
        "- `synthetic_structure_recovery.csv`: structure recovery diagnostics for synthetic datasets.",
        "",
        "## APSS Selection Frequencies",
        "",
        dataframe_to_markdown(selection) if len(selection) else "_No APSS selection rows._",
        "",
        "## Synthetic Structure Recovery",
        "",
    ]
    if len(structure):
        structure_summary = (
            structure.groupby("dataset_id")[
                [
                    "nonmonotone_precision",
                    "nonmonotone_recall",
                    "nonmonotone_f1",
                    "interaction_precision",
                    "interaction_recall",
                    "interaction_f1",
                    "false_complexity_count",
                ]
            ]
            .mean()
            .reset_index()
        )
        lines.append(dataframe_to_markdown(structure_summary))
    else:
        lines.append("_No synthetic structure diagnostics._")
    lines.extend(
        [
            "",
            "## Notes",
            "",
            "- This is a lightweight proof-of-concept, not the formal paper experiment.",
            "- Models are thresholded score models implemented with `numpy/pandas` only.",
            "- M3/M5 non-monotonicity detection is based on derivative sign changes in quadratic marginal terms.",
            "- M4/M5 interactions use either train-residual top-K selection or validation-gated forward selection, depending on configuration.",
            "- APSS selection minimizes validation ordinal MAE plus a small complexity penalty.",
        ]
    )
    (out_dir / "README.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    args = parse_args()
    timestamp = time.strftime("%Y%m%d-%H%M%S")
    out_dir = Path(args.out_dir) if args.out_dir else ROOT / "experiments" / f"{timestamp}-apss-poc"
    if not out_dir.is_absolute():
        out_dir = ROOT / out_dir
    out_dir = out_dir.resolve()
    out_dir.mkdir(parents=True, exist_ok=True)

    start = time.time()
    manifest = pd.read_csv(ROOT / args.manifest)
    manifest = manifest[manifest["group"].isin(args.groups)].copy()
    if args.limit_datasets:
        manifest = manifest[manifest["dataset_id"].isin(args.limit_datasets)].copy()
    manifest = manifest.sort_values(["group", "dataset_id"])

    all_results: list[dict[str, object]] = []
    all_structure: list[dict[str, object]] = []
    for _, row in manifest.iterrows():
        print(f"[run] {row['dataset_id']} ({row['group']})")
        result_rows, structure_rows = run_dataset(
            row,
            seeds=args.seeds,
            train_frac=args.train_frac,
            val_frac=args.val_frac,
            alpha=args.ridge_alpha,
            max_interactions=args.max_interactions,
            complexity_lambda=args.complexity_lambda,
            interaction_selection=args.interaction_selection,
            interaction_candidate_pool=args.interaction_candidate_pool,
            interaction_gain_threshold=args.interaction_gain_threshold,
        )
        all_results.extend(result_rows)
        all_structure.extend(structure_rows)

    results = pd.DataFrame(all_results)
    structure = pd.DataFrame(all_structure)
    summary, selection = summarize_results(results)

    results.to_csv(out_dir / "split_results.csv", index=False, encoding="utf-8")
    summary.to_csv(out_dir / "summary_by_dataset_model.csv", index=False, encoding="utf-8")
    selection.to_csv(out_dir / "apss_selection_frequencies.csv", index=False, encoding="utf-8")
    structure.to_csv(out_dir / "synthetic_structure_recovery.csv", index=False, encoding="utf-8")
    (out_dir / "manifest.json").write_text(
        json.dumps(
            {
                "args": vars(args),
                "datasets": manifest["dataset_id"].tolist(),
                "output_dir": str(out_dir.relative_to(ROOT)),
                "runtime_seconds": time.time() - start,
            },
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )
    write_markdown_report(out_dir, args, results, summary, selection, structure, time.time() - start)
    print(f"[done] wrote {out_dir}")


if __name__ == "__main__":
    main()
