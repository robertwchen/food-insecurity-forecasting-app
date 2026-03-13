# pyright: reportArgumentType=false, reportAttributeAccessIssue=false, reportCallIssue=false
from dataclasses import dataclass

import pandas as pd

from food_forecast.config import DEFAULT_POPULATION_YEAR
from food_forecast.data_loading import RawDatasets


@dataclass
class PreparedDatasets:
    food_bank: pd.DataFrame
    poverty: pd.DataFrame
    snap: pd.DataFrame
    unemployment: pd.DataFrame
    population_long: pd.DataFrame


def _normalize_columns(df: pd.DataFrame) -> pd.DataFrame:
    normalized = df.copy()
    normalized.columns = (
        normalized.columns.str.strip()
        .str.lower()
        .str.replace("\n", "_", regex=False)
        .str.replace(" ", "_", regex=False)
        .str.replace("(", "", regex=False)
        .str.replace(")", "", regex=False)
    )
    return normalized


def _rename_first_match(
    df: pd.DataFrame, canonical_name: str, candidate_names: list[str]
) -> pd.DataFrame:
    renamed = df.copy()
    for candidate in candidate_names:
        if candidate in renamed.columns:
            return renamed.rename(columns={candidate: canonical_name})
    return renamed


def _to_county_fips(series: pd.Series) -> pd.Series:
    cleaned = (
        series.astype(str)
        .str.strip()
        .str.replace(".0", "", regex=False)
        .str.zfill(3)
    )
    return "51" + cleaned


def _to_five_digit_fips(series: pd.Series) -> pd.Series:
    return (
        series.astype(str)
        .str.strip()
        .str.replace(".0", "", regex=False)
        .str.zfill(5)
    )


def prepare_food_bank(food_bank: pd.DataFrame) -> pd.DataFrame:
    prepared = _normalize_columns(food_bank)

    if "food_distributed_pounds" not in prepared.columns:
        if "pounds_of_food_distributed" not in prepared.columns:
            raise KeyError("Food bank data is missing pounds of food distributed.")
        prepared = prepared.rename(
            columns={"pounds_of_food_distributed": "food_distributed_pounds"}
        )

    required_columns = ["year", "month", "fips", "locality", "food_distributed_pounds"]
    prepared = prepared.dropna(subset=required_columns).copy()
    prepared["date"] = pd.to_datetime(
        prepared["year"].astype(str) + " " + prepared["month"].astype(str),
        format="%Y %B",
        errors="coerce",
    )
    prepared["fips"] = _to_county_fips(prepared["fips"])
    prepared["food_distributed_pounds"] = pd.to_numeric(
        prepared["food_distributed_pounds"], errors="coerce"
    )
    prepared = prepared.dropna(subset=["date", "food_distributed_pounds"])
    return prepared


def prepare_poverty(poverty: pd.DataFrame) -> pd.DataFrame:
    prepared = _normalize_columns(poverty)
    required_columns = ["county", "fips", "people_below_poverty"]
    prepared = prepared.dropna(subset=required_columns).copy()
    prepared["fips"] = _to_five_digit_fips(prepared["fips"])
    prepared["people_below_poverty"] = pd.to_numeric(
        prepared["people_below_poverty"], errors="coerce"
    )
    prepared = prepared.dropna(subset=["people_below_poverty"])
    return prepared


def prepare_snap(snap: pd.DataFrame) -> pd.DataFrame:
    prepared = _normalize_columns(snap)
    prepared = _rename_first_match(
        prepared,
        canonical_name="persons_total",
        candidate_names=["persons_total", "persons__total"],
    )
    if "persons_total" not in prepared.columns:
        raise KeyError("SNAP data is missing the persons_total column.")

    required_columns = ["locality", "fips", "persons_total", "date"]
    prepared = prepared.dropna(subset=required_columns).copy()
    prepared["fips"] = _to_county_fips(prepared["fips"])
    prepared["date"] = pd.to_datetime(
        prepared["date"], format="%m/%d/%y", errors="coerce"
    )
    prepared["persons_total"] = pd.to_numeric(prepared["persons_total"], errors="coerce")
    prepared["locality_clean"] = prepared["locality"].str.lower().str.strip()
    prepared = prepared.dropna(subset=["date", "persons_total"])
    return prepared


def prepare_unemployment(unemployment: pd.DataFrame) -> pd.DataFrame:
    prepared = _normalize_columns(unemployment)
    required_columns = ["statecode", "countycode", "year", "period", "unemployment"]
    prepared = prepared.dropna(subset=required_columns).copy()

    prepared["month"] = prepared["period"].str.extract(r"M(\d+)", expand=False)
    prepared["month"] = pd.to_numeric(prepared["month"], errors="coerce")
    prepared = prepared.dropna(subset=["year", "month"])

    prepared["year"] = prepared["year"].astype(int)
    prepared["month"] = prepared["month"].astype(int)
    prepared = prepared[(prepared["month"] >= 1) & (prepared["month"] <= 12)]

    prepared["date"] = pd.to_datetime(
        prepared["year"].astype(str)
        + "-"
        + prepared["month"].astype(str).str.zfill(2)
        + "-01",
        errors="coerce",
    )
    prepared["fips"] = (
        prepared["statecode"].astype(str).str.strip()
        + prepared["countycode"].astype(str).str.replace(".0", "", regex=False).str.zfill(3)
    )
    prepared["unemployment"] = pd.to_numeric(prepared["unemployment"], errors="coerce")
    prepared = prepared.dropna(subset=["date", "unemployment"])
    return prepared


def prepare_population(population: pd.DataFrame, snap: pd.DataFrame) -> pd.DataFrame:
    prepared = population.copy()
    prepared["County"] = prepared["County"].str.lstrip(".").str.strip()
    prepared["County"] = prepared["County"].str.split(",").str[0].str.strip()
    prepared = prepared.dropna().copy()

    prepared["county_clean"] = prepared["County"].str.lower().str.strip()
    locality_to_fips = (
        snap.drop_duplicates(subset="locality_clean")[["locality_clean", "fips"]]
        .set_index("locality_clean")["fips"]
        .to_dict()
    )
    prepared["fips"] = prepared["county_clean"].map(locality_to_fips)

    valid_years = [str(year) for year in range(2010, 2025) if str(year) in prepared.columns]
    population_long = prepared.melt(
        id_vars=["County", "fips"],
        value_vars=valid_years,
        var_name="year",
        value_name="population",
    )
    population_long["population"] = (
        population_long["population"]
        .astype(str)
        .str.replace(",", "", regex=False)
        .str.strip()
    )
    population_long["population"] = pd.to_numeric(
        population_long["population"], errors="coerce"
    )
    population_long["year"] = population_long["year"].astype(int)
    population_long["fips"] = _to_five_digit_fips(population_long["fips"])
    population_long = population_long.dropna(subset=["fips", "population"])
    return population_long


def prepare_datasets(raw_datasets: RawDatasets) -> PreparedDatasets:
    food_bank = prepare_food_bank(raw_datasets.food_bank)
    poverty = prepare_poverty(raw_datasets.poverty)
    snap = prepare_snap(raw_datasets.snap)
    unemployment = prepare_unemployment(raw_datasets.unemployment)
    population_long = prepare_population(raw_datasets.population, snap)

    return PreparedDatasets(
        food_bank=food_bank,
        poverty=poverty,
        snap=snap,
        unemployment=unemployment,
        population_long=population_long,
    )


def build_model_dataframe(
    prepared: PreparedDatasets, population_year: int = DEFAULT_POPULATION_YEAR
) -> pd.DataFrame:
    food_bank = prepared.food_bank.copy()
    snap = prepared.snap.copy()
    unemployment = prepared.unemployment.copy()

    food_bank["month"] = food_bank["date"].dt.month
    snap["month"] = snap["date"].dt.month
    unemployment["month"] = unemployment["date"].dt.month

    monthly_food = (
        food_bank.groupby("month")["food_distributed_pounds"].mean().reset_index()
    )
    monthly_snap = snap.groupby("month")["persons_total"].mean().reset_index()
    monthly_unemployment = (
        unemployment.groupby("month")["unemployment"].mean().reset_index()
    )

    avg_population = prepared.population_long[
        prepared.population_long["year"] == population_year
    ]["population"].mean()
    avg_poverty = prepared.poverty["people_below_poverty"].mean()

    model_df = monthly_food.merge(monthly_snap, on="month", how="inner")
    model_df = model_df.merge(monthly_unemployment, on="month", how="inner")

    model_df["population"] = avg_population
    model_df["poverty"] = avg_poverty
    model_df["snap_per_capita"] = model_df["persons_total"] / model_df["population"]
    model_df["unemp_per_capita"] = model_df["unemployment"] / model_df["population"]
    model_df["poverty_per_capita"] = model_df["poverty"] / model_df["population"]

    model_df = model_df.sort_values("month").reset_index(drop=True)
    model_df["prev_food"] = model_df["food_distributed_pounds"].shift(1)
    model_df["prev_food"] = model_df["prev_food"].fillna(
        model_df["food_distributed_pounds"].mean()
    )
    return model_df
