from __future__ import annotations

import json
import io
import math
import re
import zipfile
from pathlib import Path

import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "raw"
PROCESSED = ROOT / "data" / "processed"
METADATA = ROOT / "data" / "metadata"

RNG = np.random.default_rng(20260629)


def ensure_dirs() -> None:
    for path in [
        PROCESSED / "monotone_classification",
        PROCESSED / "polish_research_units",
        PROCESSED / "education_evaluation",
        PROCESSED / "health_risk_evaluation",
        PROCESSED / "toc_uco_ordinal_classification",
        PROCESSED / "wine_quality",
        PROCESSED / "qs_university_rankings",
        PROCESSED / "synthetic_structure_recovery",
        METADATA,
    ]:
        path.mkdir(parents=True, exist_ok=True)


def parse_class_index(value: object) -> int:
    match = re.search(r"(\d+)", str(value))
    if not match:
        raise ValueError(f"Cannot parse class index from {value!r}")
    return int(match.group(1))


def numeric_series(series: pd.Series) -> pd.Series:
    cleaned = (
        series.astype(str)
        .str.replace("\u00a0", " ", regex=False)
        .str.replace(",", "", regex=False)
        .str.extract(r"([-+]?\d*\.?\d+)")[0]
    )
    return pd.to_numeric(cleaned, errors="coerce")


def minmax(series: pd.Series) -> pd.Series:
    values = pd.to_numeric(series, errors="coerce")
    lo = values.min()
    hi = values.max()
    if pd.isna(lo) or pd.isna(hi) or math.isclose(float(lo), float(hi)):
        return pd.Series(np.zeros(len(values)), index=series.index, dtype=float)
    return (values - lo) / (hi - lo)


def class_label_from_index(index: int) -> str:
    return f"Cl{int(index)}"


def clean_id(value: object) -> str:
    text = str(value).strip().lower()
    text = re.sub(r"[^a-z0-9]+", "_", text)
    return text.strip("_")


def rank_to_qs_class(rank: float) -> int:
    if pd.isna(rank):
        return np.nan
    if rank < 1 or rank > 500:
        return np.nan
    # Rank 1-100 is the best class Cl5; rank 401-500 is Cl1.
    return int(6 - math.ceil(float(rank) / 100.0))


def save_dataset(
    df: pd.DataFrame,
    relative_path: Path,
    manifest_rows: list[dict[str, object]],
    *,
    dataset_id: str,
    group: str,
    raw_source_path: str,
    source_url: str,
    label_source: str,
    intended_role: str,
    structural_truth: str,
    notes: str,
) -> None:
    output_path = PROCESSED / relative_path
    output_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(output_path, index=False, encoding="utf-8")

    criteria_cols = [c for c in df.columns if re.fullmatch(r"g\d+", c)]
    class_values = sorted(pd.Series(df["class_index"]).dropna().astype(int).unique().tolist())
    manifest_rows.append(
        {
            "dataset_id": dataset_id,
            "group": group,
            "processed_path": str(output_path.relative_to(ROOT)).replace("\\", "/"),
            "raw_source_path": raw_source_path.replace("\\", "/"),
            "source_url": source_url,
            "n_alternatives": int(len(df)),
            "n_criteria": int(len(criteria_cols)),
            "criteria_columns": ";".join(criteria_cols),
            "n_classes": int(len(class_values)),
            "class_order": ";".join(f"Cl{i}" for i in class_values),
            "label_source": label_source,
            "intended_benchmark_role": intended_role,
            "structural_truth": structural_truth,
            "notes": notes,
        }
    )


def process_monotone_classification(manifest_rows: list[dict[str, object]]) -> None:
    source_dir = RAW / "ijoc-data" / "monotone-classification-problems"
    source_url = "https://github.com/ijoc-data/download/tree/master/monotone-classification-problems"
    for path in sorted(source_dir.glob("*.csv")):
        raw = pd.read_csv(path)
        criteria = [c for c in raw.columns if re.fullmatch(r"g\d+", c)]
        dataset_id = f"mcs_{path.stem.lower()}"
        out = pd.DataFrame(
            {
                "alternative_id": raw["Alternative"].astype(str),
                "dataset_id": dataset_id,
            }
        )
        for criterion in criteria:
            out[criterion] = pd.to_numeric(raw[criterion], errors="coerce")
        out["class_label"] = raw["Class"].astype(str)
        out["class_index"] = raw["Class"].map(parse_class_index)
        save_dataset(
            out,
            Path("monotone_classification") / f"{dataset_id}.csv",
            manifest_rows,
            dataset_id=dataset_id,
            group="monotone_classification",
            raw_source_path=str(path.relative_to(ROOT)),
            source_url=source_url,
            label_source="IJOC ordered classes; greater class index is more preferred.",
            intended_role="Real public monotone benchmark; tests whether adaptive models avoid unnecessary non-monotonicity or interactions.",
            structural_truth="Known benchmark assumption: gain-type ordered criteria and ordered classes; exact generative structure is unknown.",
            notes="Criteria are already normalized to [0,1] in the source repository.",
        )


def process_polish_research_units(manifest_rows: list[dict[str, object]]) -> None:
    path = RAW / "ijoc-data" / "research-unit-evaluation" / "PLS.csv"
    raw = pd.read_csv(path)
    source_url = "https://github.com/ijoc-data/download/tree/master/research-unit-evaluation"
    criteria = [c for c in raw.columns if re.fullmatch(r"g\d+", c)]

    def make_output(frame: pd.DataFrame, dataset_id: str) -> pd.DataFrame:
        out = pd.DataFrame(
            {
                "alternative_id": frame["Alternative"].astype(str),
                "dataset_id": dataset_id,
                "subset": frame["Subset"].astype(str),
            }
        )
        for criterion in criteria:
            out[criterion] = minmax(frame[criterion])
        out["class_label"] = frame["Class"].astype(str)
        out["class_index"] = frame["Class"].map(parse_class_index)
        return out

    all_id = "polish_research_units_all"
    save_dataset(
        make_output(raw, all_id),
        Path("polish_research_units") / f"{all_id}.csv",
        manifest_rows,
        dataset_id=all_id,
        group="polish_research_units",
        raw_source_path=str(path.relative_to(ROOT)),
        source_url=source_url,
        label_source="Polish Ministry of Science and Higher Education 2017 evaluation classes.",
        intended_role="Real MCDA-like application benchmark with official ordered labels.",
        structural_truth="No structure truth; all four criteria are gain type according to source README.",
        notes="Criteria are min-max normalized across all 993 units in the processed all-units file.",
    )

    for subset in sorted(raw["Subset"].dropna().unique()):
        frame = raw[raw["Subset"] == subset].copy()
        dataset_id = f"polish_research_units_{str(subset).lower()}"
        save_dataset(
            make_output(frame, dataset_id),
            Path("polish_research_units") / f"{dataset_id}.csv",
            manifest_rows,
            dataset_id=dataset_id,
            group="polish_research_units",
            raw_source_path=str(path.relative_to(ROOT)),
            source_url=source_url,
            label_source=f"Polish Ministry 2017 evaluation classes for subset {subset}.",
            intended_role="Subset-level application benchmark matching the literature split by research field.",
            structural_truth="No structure truth; all four criteria are gain type according to source README.",
            notes="Criteria are min-max normalized within this subset in the processed file.",
        )


def process_wine_quality(manifest_rows: list[dict[str, object]]) -> None:
    zip_path = RAW / "uci_wine_quality" / "wine_quality.zip"
    source_url = "https://archive.ics.uci.edu/dataset/186/wine%2Bquality"
    with zipfile.ZipFile(zip_path) as archive:
        frames = []
        for wine_type, member in [("red", "winequality-red.csv"), ("white", "winequality-white.csv")]:
            raw = pd.read_csv(archive.open(member), sep=";")
            raw.insert(0, "wine_type", wine_type)
            frames.append(raw)
            process_wine_frame(
                raw,
                f"wine_quality_{wine_type}",
                f"{zip_path.relative_to(ROOT)}::{member}",
                source_url,
                manifest_rows,
                notes=f"{wine_type.title()} wine subset; criteria min-max normalized within subset.",
            )

        combined = pd.concat(frames, ignore_index=True)
        process_wine_frame(
            combined,
            "wine_quality_combined",
            f"{zip_path.relative_to(ROOT)}::winequality-red.csv,winequality-white.csv",
            source_url,
            manifest_rows,
            notes="Combined red and white wine data; criteria min-max normalized across combined data.",
        )


def process_wine_frame(
    raw: pd.DataFrame,
    dataset_id: str,
    raw_source_path: str,
    source_url: str,
    manifest_rows: list[dict[str, object]],
    *,
    notes: str,
) -> None:
    feature_cols = [c for c in raw.columns if c not in {"quality", "wine_type"}]
    out = pd.DataFrame(
        {
            "alternative_id": [f"{dataset_id}_{i + 1}" for i in range(len(raw))],
            "dataset_id": dataset_id,
        }
    )
    if "wine_type" in raw.columns:
        out["wine_type"] = raw["wine_type"].astype(str)
    for idx, column in enumerate(feature_cols, start=1):
        out[f"g{idx}"] = minmax(raw[column])
    quality = pd.to_numeric(raw["quality"], errors="coerce").astype(int)
    min_quality = int(quality.min())
    out["original_quality"] = quality
    out["class_index"] = quality - min_quality + 1
    out["class_label"] = out["class_index"].map(lambda value: f"Cl{int(value)}")
    save_dataset(
        out,
        Path("wine_quality") / f"{dataset_id}.csv",
        manifest_rows,
        dataset_id=dataset_id,
        group="wine_quality",
        raw_source_path=raw_source_path,
        source_url=source_url,
        label_source="UCI sensory quality score converted to ordered classes.",
        intended_role="Real ordered-class benchmark likely requiring non-linear or non-monotonic criterion effects.",
        structural_truth="No structure truth; physicochemical criteria are not assumed to be monotone gain criteria.",
        notes=notes,
    )


def student_grade_to_class(value: object) -> float:
    if pd.isna(value):
        return np.nan
    grade = float(value)
    if grade <= 9:
        return 1
    if grade <= 11:
        return 2
    if grade <= 13:
        return 3
    if grade <= 15:
        return 4
    return 5


def process_education_evaluation(manifest_rows: list[dict[str, object]]) -> None:
    process_student_performance(manifest_rows)
    process_higher_education_students_performance(manifest_rows)


def process_student_performance(manifest_rows: list[dict[str, object]]) -> None:
    zip_path = RAW / "uci_student_performance" / "student_performance.zip"
    source_url = "https://archive.ics.uci.edu/dataset/320/student+performance"
    ordered_cols = [
        "age",
        "Medu",
        "Fedu",
        "traveltime",
        "studytime",
        "failures",
        "famrel",
        "freetime",
        "goout",
        "Dalc",
        "Walc",
        "health",
        "absences",
    ]
    binary_cols = [
        "schoolsup",
        "famsup",
        "paid",
        "activities",
        "nursery",
        "higher",
        "internet",
        "romantic",
    ]
    prior_grade_cols = ["G1", "G2"]
    members = [("math", "student-mat.csv"), ("portuguese", "student-por.csv")]

    with zipfile.ZipFile(zip_path) as outer:
        nested_bytes = outer.read("student.zip")
    with zipfile.ZipFile(io.BytesIO(nested_bytes)) as archive:
        for subject, member in members:
            raw = pd.read_csv(archive.open(member), sep=";")
            for include_prior in [False, True]:
                suffix = "with_prior_grades" if include_prior else "no_prior_grades"
                dataset_id = f"student_performance_{subject}_{suffix}"
                feature_cols = ordered_cols + binary_cols + (prior_grade_cols if include_prior else [])
                out = pd.DataFrame(
                    {
                        "alternative_id": [f"{dataset_id}_{i + 1}" for i in range(len(raw))],
                        "dataset_id": dataset_id,
                        "subject": subject,
                    }
                )
                for idx, column in enumerate(feature_cols, start=1):
                    if column in binary_cols:
                        values = raw[column].astype(str).str.lower().map({"yes": 1.0, "no": 0.0})
                        out[f"g{idx}"] = values
                    else:
                        out[f"g{idx}"] = minmax(raw[column])
                out["original_grade"] = pd.to_numeric(raw["G3"], errors="coerce")
                out["class_index"] = out["original_grade"].map(student_grade_to_class)
                out["class_label"] = out["class_index"].map(class_label_from_index)
                model_cols = [c for c in out.columns if re.fullmatch(r"g\d+", c)] + ["class_index"]
                out = out.dropna(subset=model_cols).copy()
                out["class_index"] = out["class_index"].astype(int)
                save_dataset(
                    out,
                    Path("education_evaluation") / f"{dataset_id}.csv",
                    manifest_rows,
                    dataset_id=dataset_id,
                    group="education_evaluation",
                    raw_source_path=f"{zip_path.relative_to(ROOT)}::student.zip::{member}",
                    source_url=source_url,
                    label_source="UCI Student Performance final grade G3 converted into five ordered grade bands.",
                    intended_role=(
                        "Education evaluation benchmark; no-prior and with-prior variants separate "
                        "the harder background-only setting from the easier prior-grade setting."
                    ),
                    structural_truth="No structure truth; features include ordinal and binary student descriptors.",
                    notes=(
                        "Class bands: G3 0-9 -> Cl1, 10-11 -> Cl2, 12-13 -> Cl3, "
                        "14-15 -> Cl4, 16-20 -> Cl5. Features are normalized or binary encoded; "
                        "not all criteria have a normative gain direction."
                    ),
                )


def process_higher_education_students_performance(manifest_rows: list[dict[str, object]]) -> None:
    zip_path = (
        RAW
        / "uci_higher_education_students_performance"
        / "higher_education_students_performance.zip"
    )
    source_url = "https://archive.ics.uci.edu/dataset/856/higher+education+students+performance+evaluation"
    with zipfile.ZipFile(zip_path) as archive:
        member = "DATA (1).csv"
        raw = pd.read_csv(archive.open(member))

    dataset_id = "higher_education_students_performance"
    feature_cols = [str(i) for i in range(1, 31)]
    out = pd.DataFrame(
        {
            "alternative_id": raw["STUDENT ID"].astype(str),
            "dataset_id": dataset_id,
            "course_id": raw["COURSE ID"].astype(str),
        }
    )
    for idx, column in enumerate(feature_cols, start=1):
        out[f"g{idx}"] = minmax(raw[column])
    grade = pd.to_numeric(raw["GRADE"], errors="coerce")
    out["original_grade"] = grade
    out["class_index"] = grade.astype(int) + 1
    out["class_label"] = out["class_index"].map(class_label_from_index)
    model_cols = [c for c in out.columns if re.fullmatch(r"g\d+", c)] + ["class_index"]
    out = out.dropna(subset=model_cols).copy()
    out["class_index"] = out["class_index"].astype(int)
    save_dataset(
        out,
        Path("education_evaluation") / f"{dataset_id}.csv",
        manifest_rows,
        dataset_id=dataset_id,
        group="education_evaluation",
        raw_source_path=f"{zip_path.relative_to(ROOT)}::{member}",
        source_url=source_url,
        label_source="UCI Higher Education Students Performance Evaluation GRADE target shifted to Cl1-Cl8.",
        intended_role="Small education-evaluation ordered-class benchmark for external validity.",
        structural_truth="No structure truth; source attributes are encoded questionnaire/course descriptors.",
        notes="Columns 1-30 are min-max normalized as criteria; COURSE ID is kept as metadata, not a model criterion.",
    )


def process_health_risk_evaluation(manifest_rows: list[dict[str, object]]) -> None:
    zip_path = RAW / "uci_maternal_health_risk" / "maternal_health_risk.zip"
    source_url = "https://archive.ics.uci.edu/dataset/863/maternal+health+risk"
    with zipfile.ZipFile(zip_path) as archive:
        member = "Maternal Health Risk Data Set.csv"
        raw = pd.read_csv(archive.open(member))

    dataset_id = "maternal_health_risk"
    feature_cols = ["Age", "SystolicBP", "DiastolicBP", "BS", "BodyTemp", "HeartRate"]
    out = pd.DataFrame(
        {
            "alternative_id": [f"{dataset_id}_{i + 1}" for i in range(len(raw))],
            "dataset_id": dataset_id,
        }
    )
    for idx, column in enumerate(feature_cols, start=1):
        out[f"g{idx}"] = minmax(raw[column])

    risk_map = {"high risk": 1, "mid risk": 2, "low risk": 3}
    out["risk_level"] = raw["RiskLevel"].astype(str)
    out["class_index"] = out["risk_level"].str.lower().map(risk_map)
    out["class_label"] = out["class_index"].map(class_label_from_index)
    model_cols = [c for c in out.columns if re.fullmatch(r"g\d+", c)] + ["class_index"]
    out = out.dropna(subset=model_cols).copy()
    out["class_index"] = out["class_index"].astype(int)
    save_dataset(
        out,
        Path("health_risk_evaluation") / f"{dataset_id}.csv",
        manifest_rows,
        dataset_id=dataset_id,
        group="health_risk_evaluation",
        raw_source_path=f"{zip_path.relative_to(ROOT)}::{member}",
        source_url=source_url,
        label_source="UCI Maternal Health Risk risk level mapped as high -> Cl1, mid -> Cl2, low -> Cl3.",
        intended_role="Risk-stratification benchmark with clinically interpretable criteria and ordered labels.",
        structural_truth="No structure truth; criteria are clinical measurements and may be monotone or non-monotone.",
        notes=(
            "Larger class_index means lower risk / more preferred health status. "
            "Clinical measurements are min-max normalized in their original direction."
        ),
    )


def process_toc_uco_ordinal_classification(manifest_rows: list[dict[str, object]]) -> None:
    zip_path = RAW / "toc_uco" / "TOC-UCO.zip"
    source_url = "https://www.uco.es/grupos/ayrna/materials/tocuco/"
    with zipfile.ZipFile(zip_path) as archive:
        metadata = pd.read_csv(archive.open("TOC-UCO/metadata.csv"))
        ordinal_metadata = metadata[metadata["is_oc"].astype(bool)].sort_values("dataset")
        for _, meta_row in ordinal_metadata.iterrows():
            source_name = str(meta_row["dataset"])
            member = f"TOC-UCO/data/{source_name}.csv"
            raw = pd.read_csv(archive.open(member))
            feature_cols = [c for c in raw.columns if c != "y"]
            dataset_id = f"toc_uco_{clean_id(source_name)}"
            out = pd.DataFrame(
                {
                    "alternative_id": [f"{dataset_id}_{i + 1}" for i in range(len(raw))],
                    "dataset_id": dataset_id,
                    "source_dataset": source_name,
                }
            )
            for idx, column in enumerate(feature_cols, start=1):
                out[f"g{idx}"] = minmax(raw[column])
            y = pd.to_numeric(raw["y"], errors="coerce")
            class_values = sorted(v for v in y.dropna().unique().tolist())
            class_map = {value: idx + 1 for idx, value in enumerate(class_values)}
            out["source_y"] = y
            out["class_index"] = y.map(class_map)
            out["class_label"] = out["class_index"].map(class_label_from_index)
            model_cols = [c for c in out.columns if re.fullmatch(r"g\d+", c)] + ["class_index"]
            out = out.dropna(subset=model_cols).copy()
            out["class_index"] = out["class_index"].astype(int)
            save_dataset(
                out,
                Path("toc_uco_ordinal_classification") / f"{dataset_id}.csv",
                manifest_rows,
                dataset_id=dataset_id,
                group="toc_uco_ordinal_classification",
                raw_source_path=f"{zip_path.relative_to(ROOT)}::{member}",
                source_url=source_url,
                label_source="TOC-UCO original ordinal-classification label y mapped by sorted class order.",
                intended_role=(
                    "Broad tabular ordinal-classification generalization benchmark; used to test whether "
                    "adaptive structure selection is robust beyond MCDA-specific datasets."
                ),
                structural_truth="No structure truth; TOC-UCO provides ordinal labels but not preference-structure ground truth.",
                notes=(
                    "Only TOC-UCO datasets with is_oc=True are processed. Features are min-max normalized; "
                    "larger class_index follows the source ordinal order and may not always mean preference desirability."
                ),
            )


def find_qs_file(year: str, suffix: str) -> Path:
    matches = sorted((RAW / "local_qs").glob(f"*{year}*{suffix}"))
    if not matches:
        raise FileNotFoundError(f"No QS {year} {suffix} file in data/raw/local_qs")
    return matches[0]


def read_local_qs_csv(path: Path) -> pd.DataFrame:
    for encoding in ["utf-8-sig", "gb18030", "gbk", "latin1"]:
        try:
            return pd.read_csv(path, encoding=encoding)
        except UnicodeDecodeError:
            continue
    return pd.read_csv(path, encoding="latin1")


def process_qs_rankings(manifest_rows: list[dict[str, object]]) -> None:
    qs_url = "https://www.topuniversities.com/world-university-rankings/methodology"
    process_qs_legacy_csv(
        find_qs_file("2020", ".csv"),
        "qs_2020_top500_common6",
        rank_col=1,
        name_col=2,
        feature_cols=[4, 5, 6, 7, 8, 9],
        criterion_names=[
            "international_students",
            "international_faculty",
            "faculty_student_ratio",
            "citations_per_faculty",
            "academic_reputation",
            "employer_reputation",
        ],
        source_url=qs_url,
        manifest_rows=manifest_rows,
    )
    process_qs_legacy_csv(
        find_qs_file("2022", ".csv"),
        "qs_2022_top500_common6",
        rank_col=0,
        name_col=1,
        feature_cols=[4, 5, 6, 7, 8, 9],
        criterion_names=[
            "international_students",
            "international_faculty",
            "faculty_student_ratio",
            "citations_per_faculty",
            "academic_reputation",
            "employer_reputation",
        ],
        source_url=qs_url,
        manifest_rows=manifest_rows,
    )

    path_2026 = find_qs_file("2026", ".xlsx")
    raw_2026 = pd.read_excel(path_2026)
    common6_cols = [2, 4, 5, 6, 7, 8]
    all10_cols = list(range(2, 12))
    process_qs_2026_frame(
        raw_2026,
        "qs_2026_top500_common6",
        path_2026,
        common6_cols,
        [
            "international_students",
            "international_faculty",
            "faculty_student_ratio",
            "citations_per_faculty",
            "academic_reputation",
            "employer_reputation",
        ],
        qs_url,
        manifest_rows,
        notes="Uses the six criteria common to the 2020/2022 local files. Rank is inferred from row order.",
    )
    process_qs_2026_frame(
        raw_2026,
        "qs_2026_top500_all10",
        path_2026,
        all10_cols,
        [
            "international_students",
            "international_research_network",
            "international_faculty",
            "faculty_student_ratio",
            "citations_per_faculty",
            "academic_reputation",
            "employer_reputation",
            "employment_outcomes",
            "sustainability",
            "international_student_diversity",
        ],
        qs_url,
        manifest_rows,
        notes="Uses all ten available criteria in the local 2026 file. Rank is inferred from row order.",
    )


def process_qs_legacy_csv(
    path: Path,
    dataset_id: str,
    *,
    rank_col: int,
    name_col: int,
    feature_cols: list[int],
    criterion_names: list[str],
    source_url: str,
    manifest_rows: list[dict[str, object]],
) -> None:
    raw = read_local_qs_csv(path)
    ranks = numeric_series(raw.iloc[:, rank_col])
    frame = raw.assign(_rank=ranks)
    frame = frame[(frame["_rank"] >= 1) & (frame["_rank"] <= 500)].copy()
    frame = frame.sort_values("_rank").head(500).reset_index(drop=True)

    out = pd.DataFrame(
        {
            "alternative_id": [f"{dataset_id}_{int(rank)}" for rank in frame["_rank"]],
            "dataset_id": dataset_id,
            "rank": frame["_rank"].astype(int),
            "university_name_raw": frame.iloc[:, name_col].astype(str),
        }
    )
    for idx, col in enumerate(feature_cols, start=1):
        values = numeric_series(frame.iloc[:, col])
        out[f"g{idx}"] = (values / 100.0).clip(0, 1)
    out["class_index"] = out["rank"].map(rank_to_qs_class).astype(int)
    out["class_label"] = out["class_index"].map(lambda value: f"Cl{int(value)}")
    out = out.dropna(subset=[f"g{i}" for i in range(1, len(feature_cols) + 1)])
    save_dataset(
        out,
        Path("qs_university_rankings") / f"{dataset_id}.csv",
        manifest_rows,
        dataset_id=dataset_id,
        group="qs_university_rankings",
        raw_source_path=str(path.relative_to(ROOT)),
        source_url=source_url,
        label_source="QS rank converted into five ordered classes: ranks 1-100 -> Cl5, ..., 401-500 -> Cl1.",
        intended_role="Application benchmark using an external ranking signal; not treated as objective ground truth.",
        structural_truth="No structure truth; QS is an external ranking formula/survey signal.",
        notes=f"Criteria are divided by 100. Criterion order: {', '.join(criterion_names)}. Local university names are kept as raw strings because the source CSV appears mojibaked.",
    )


def process_qs_2026_frame(
    raw: pd.DataFrame,
    dataset_id: str,
    path: Path,
    feature_cols: list[int],
    criterion_names: list[str],
    source_url: str,
    manifest_rows: list[dict[str, object]],
    *,
    notes: str,
) -> None:
    frame = raw.head(500).copy().reset_index(drop=True)
    ranks = pd.Series(np.arange(1, len(frame) + 1), index=frame.index)
    out = pd.DataFrame(
        {
            "alternative_id": [f"{dataset_id}_{int(rank)}" for rank in ranks],
            "dataset_id": dataset_id,
            "rank": ranks.astype(int),
            "university_name_raw": frame.iloc[:, 0].astype(str),
        }
    )
    for idx, col in enumerate(feature_cols, start=1):
        values = numeric_series(frame.iloc[:, col])
        out[f"g{idx}"] = (values / 100.0).clip(0, 1)
    out["class_index"] = out["rank"].map(rank_to_qs_class).astype(int)
    out["class_label"] = out["class_index"].map(lambda value: f"Cl{int(value)}")
    out = out.dropna(subset=[f"g{i}" for i in range(1, len(feature_cols) + 1)])
    save_dataset(
        out,
        Path("qs_university_rankings") / f"{dataset_id}.csv",
        manifest_rows,
        dataset_id=dataset_id,
        group="qs_university_rankings",
        raw_source_path=str(path.relative_to(ROOT)),
        source_url=source_url,
        label_source="QS row-order rank converted into five ordered classes: ranks 1-100 -> Cl5, ..., 401-500 -> Cl1.",
        intended_role="Application benchmark and potential cross-year generalization check; not treated as objective ground truth.",
        structural_truth="No structure truth; QS is an external ranking formula/survey signal.",
        notes=f"{notes} Criteria are divided by 100. Criterion order: {', '.join(criterion_names)}.",
    )


def ordered_classes_from_score(score: np.ndarray, n_classes: int = 4) -> np.ndarray:
    thresholds = np.quantile(score, np.linspace(0, 1, n_classes + 1)[1:-1])
    return np.digitize(score, thresholds, right=False) + 1


def save_synthetic(
    dataset_id: str,
    x: np.ndarray,
    score: np.ndarray,
    truth: dict[str, object],
    manifest_rows: list[dict[str, object]],
) -> None:
    classes = ordered_classes_from_score(score, 4)
    out = pd.DataFrame(
        {
            "alternative_id": [f"{dataset_id}_{i + 1}" for i in range(len(x))],
            "dataset_id": dataset_id,
        }
    )
    for idx in range(x.shape[1]):
        out[f"g{idx + 1}"] = x[:, idx]
    out["latent_score"] = score
    out["class_index"] = classes.astype(int)
    out["class_label"] = out["class_index"].map(lambda value: f"Cl{int(value)}")
    save_dataset(
        out,
        Path("synthetic_structure_recovery") / f"{dataset_id}.csv",
        manifest_rows,
        dataset_id=dataset_id,
        group="synthetic_structure_recovery",
        raw_source_path="generated",
        source_url="generated by scripts/prepare_bench_data.py",
        label_source="Generated from known latent preference score and quantile class thresholds.",
        intended_role="Structure-recovery benchmark with known ground-truth preference structure.",
        structural_truth=json.dumps(truth, ensure_ascii=False, sort_keys=True),
        notes="All criteria are sampled in [0,1]. Classes are balanced by latent-score quantiles.",
    )


def process_synthetic_structure_recovery(manifest_rows: list[dict[str, object]]) -> None:
    n = 1200
    m = 6
    noise = 0.025

    x = RNG.uniform(0, 1, size=(n, m))
    weights = np.array([0.24, 0.20, 0.18, 0.16, 0.13, 0.09])
    score = x @ weights + RNG.normal(0, noise, size=n)
    save_synthetic(
        "synthetic_monotone_additive",
        x,
        score,
        {
            "marginal_shapes": {f"g{i + 1}": "monotone_increasing_linear" for i in range(m)},
            "interactions": [],
            "weights": weights.round(4).tolist(),
        },
        manifest_rows,
    )

    x = RNG.uniform(0, 1, size=(n, m))
    g1_peak = 1 - 4 * (x[:, 0] - 0.5) ** 2
    g2_valley = 4 * (x[:, 1] - 0.5) ** 2
    score = (
        0.25 * g1_peak
        + 0.18 * g2_valley
        + 0.18 * x[:, 2]
        + 0.14 * x[:, 3]
        + 0.13 * x[:, 4]
        + 0.12 * x[:, 5]
        + RNG.normal(0, noise, size=n)
    )
    save_synthetic(
        "synthetic_nonmonotone_marginals",
        x,
        score,
        {
            "marginal_shapes": {
                "g1": "inverted_u",
                "g2": "u_shaped",
                "g3": "monotone_increasing_linear",
                "g4": "monotone_increasing_linear",
                "g5": "monotone_increasing_linear",
                "g6": "monotone_increasing_linear",
            },
            "interactions": [],
        },
        manifest_rows,
    )

    x = RNG.uniform(0, 1, size=(n, m))
    base = x @ np.array([0.18, 0.16, 0.18, 0.16, 0.18, 0.14])
    positive_interaction = 0.35 * x[:, 0] * x[:, 1]
    negative_interaction = -0.28 * x[:, 2] * x[:, 3]
    score = base + positive_interaction + negative_interaction + RNG.normal(0, noise, size=n)
    save_synthetic(
        "synthetic_sparse_interactions",
        x,
        score,
        {
            "marginal_shapes": {f"g{i + 1}": "monotone_increasing_linear" for i in range(m)},
            "interactions": [
                {"criteria": ["g1", "g2"], "type": "positive", "coefficient": 0.35},
                {"criteria": ["g3", "g4"], "type": "negative", "coefficient": -0.28},
            ],
        },
        manifest_rows,
    )

    x = RNG.uniform(0, 1, size=(n, m))
    g1_peak = 1 - 4 * (x[:, 0] - 0.5) ** 2
    base = 0.23 * g1_peak + 0.18 * x[:, 1] + 0.14 * x[:, 2] + 0.12 * x[:, 3] + 0.11 * x[:, 4] + 0.10 * x[:, 5]
    score = base + 0.26 * x[:, 1] * x[:, 4] - 0.22 * x[:, 2] * x[:, 5] + RNG.normal(0, noise, size=n)
    save_synthetic(
        "synthetic_mixed_structure",
        x,
        score,
        {
            "marginal_shapes": {
                "g1": "inverted_u",
                "g2": "monotone_increasing_linear",
                "g3": "monotone_increasing_linear",
                "g4": "monotone_increasing_linear",
                "g5": "monotone_increasing_linear",
                "g6": "monotone_increasing_linear",
            },
            "interactions": [
                {"criteria": ["g2", "g5"], "type": "positive", "coefficient": 0.26},
                {"criteria": ["g3", "g6"], "type": "negative", "coefficient": -0.22},
            ],
        },
        manifest_rows,
    )


def write_metadata(manifest_rows: list[dict[str, object]]) -> None:
    manifest = pd.DataFrame(manifest_rows).sort_values(["group", "dataset_id"])
    manifest_csv = METADATA / "bench_manifest.csv"
    manifest_json = METADATA / "bench_manifest.json"
    manifest.to_csv(manifest_csv, index=False, encoding="utf-8")
    manifest_json.write_text(
        json.dumps(manifest_rows, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    summary = (
        manifest.groupby("group")
        .agg(
            datasets=("dataset_id", "count"),
            total_alternatives=("n_alternatives", "sum"),
            min_criteria=("n_criteria", "min"),
            max_criteria=("n_criteria", "max"),
        )
        .reset_index()
    )
    summary.to_csv(METADATA / "bench_summary_by_group.csv", index=False, encoding="utf-8")

    quality_rows = []
    for _, row in manifest.iterrows():
        path = ROOT / row["processed_path"]
        df = pd.read_csv(path)
        criteria_cols = [c for c in df.columns if c.startswith("g") and c[1:].isdigit()]
        model_cols = criteria_cols + ["class_index"]
        quality_rows.append(
            {
                "dataset_id": row["dataset_id"],
                "rows": len(df),
                "criteria": len(criteria_cols),
                "classes": int(df["class_index"].nunique()),
                "missing_model_cells": int(df[model_cols].isna().sum().sum()),
                "class_min": int(df["class_index"].min()),
                "class_max": int(df["class_index"].max()),
            }
        )
    quality = pd.DataFrame(quality_rows)
    quality.to_csv(METADATA / "bench_quality_report.csv", index=False, encoding="utf-8")

    quality_md = [
        "# Bench Quality Report",
        "",
        "Generated by `scripts/prepare_bench_data.py`.",
        "",
        "All processed datasets use `class_index` with larger values indicating more preferred classes.",
        "",
        "| dataset_id | rows | criteria | classes | missing_model_cells | class_min | class_max |",
        "|---|---:|---:|---:|---:|---:|---:|",
    ]
    for record in quality_rows:
        quality_md.append(
            "| {dataset_id} | {rows} | {criteria} | {classes} | {missing_model_cells} | {class_min} | {class_max} |".format(
                **record
            )
        )
    quality_md.extend(
        [
            "",
            "Notes:",
            "",
            "- QS processed files may contain fewer than 500 rows because rows missing any selected criterion are dropped.",
            "- Polish research unit summary counts include both the all-units file and subset files; they are benchmark variants, not unique alternatives.",
            "- Synthetic datasets are balanced by latent-score quantiles and include `latent_score` for structure-recovery diagnostics.",
            "- Student Performance includes no-prior and with-prior variants; these are task variants, not independent raw sources.",
            "- TOC-UCO processing includes only original ordinal-classification datasets (`is_oc=True`), not discretized regression tasks.",
        ]
    )
    (METADATA / "bench_quality_report.md").write_text("\n".join(quality_md) + "\n", encoding="utf-8")

    readme = """# Bench Data Prepared for Adaptive Preference-Structure Learning

This folder contains a first reproducible data base for the adaptive MCDA/MADM preference-structure project.

## Layout

- `data/raw/`: unchanged source files downloaded or copied from local literature assets.
- `data/processed/`: normalized CSV files with a common convention.
- `data/metadata/bench_manifest.csv`: source, size, criteria, label, and benchmark-role metadata.
- `data/metadata/bench_summary_by_group.csv`: group-level counts.
- `data/metadata/bench_quality_report.md`: row/criteria/class counts and missing-value checks.

## Processed CSV convention

- `alternative_id`: row identifier.
- `dataset_id`: processed dataset identifier.
- `g1`, `g2`, ...: numeric criteria for modeling.
- `class_index`: ordered class integer; larger means more preferred.
- `class_label`: `Cl1`, `Cl2`, ...

Some application datasets keep additional descriptive columns such as `subset`, `rank`, `wine_type`, or `original_quality`.

## Benchmark roles

1. `synthetic_structure_recovery`: generated data with known latent structures. Use this layer to test whether a method recovers monotonicity, non-monotonicity, and sparse interactions.
2. `monotone_classification`: public IJOC ordered-class benchmarks with gain-type normalized criteria. Use this layer to test whether a method avoids unnecessary complexity on monotone data.
3. `polish_research_units`: official ordered labels for Polish research units. Use as the main MCDA-like real application benchmark.
4. `qs_university_rankings`: QS ranks converted into five ordered classes. Use as an external-ranking application benchmark, not as objective ground truth.
5. `education_evaluation`: UCI student-performance datasets and higher-education performance evaluation. Use as education-oriented ordered evaluation benchmarks.
6. `health_risk_evaluation`: UCI Maternal Health Risk. Use as a risk-stratification benchmark with interpretable clinical measurements.
7. `wine_quality`: UCI wine quality ordered labels. Use as a likely non-linear/non-monotonic ordered-class benchmark.
8. `toc_uco_ordinal_classification`: original ordinal-classification datasets from TOC-UCO. Use as a broad generalization layer rather than a MCDA-specific evidence layer.

## Regeneration

First prepare raw data:

```powershell
.\\scripts\\download_bench_raw_data.ps1
```

Then regenerate processed data and metadata:

```powershell
& 'C:\\Users\\22433\\.cache\\codex-runtimes\\codex-primary-runtime\\dependencies\\python\\python.exe' -s .\\scripts\\prepare_bench_data.py
```
"""
    (ROOT / "data" / "README.md").write_text(readme, encoding="utf-8")


def main() -> None:
    ensure_dirs()
    manifest_rows: list[dict[str, object]] = []
    process_monotone_classification(manifest_rows)
    process_polish_research_units(manifest_rows)
    process_education_evaluation(manifest_rows)
    process_health_risk_evaluation(manifest_rows)
    process_wine_quality(manifest_rows)
    process_qs_rankings(manifest_rows)
    process_toc_uco_ordinal_classification(manifest_rows)
    process_synthetic_structure_recovery(manifest_rows)
    write_metadata(manifest_rows)

    print(f"Prepared {len(manifest_rows)} datasets.")
    print(f"Manifest: {METADATA / 'bench_manifest.csv'}")


if __name__ == "__main__":
    main()
