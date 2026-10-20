"""Hidden oracle for the polars 2.0 tasks: reference solutions, 1.x-habit solutions and tests.

Never shown to any agent, never put in any memory, RAG index or prompt.
- REFERENCE[task_id]: a correct polars 2.0 implementation.
- HABIT[task_id]: what polars 1.x code looks like; used to prove each task is discriminative.
- TESTS[task_id](module) -> None: raises AssertionError on wrong behaviour.
"""

from datetime import date, datetime, time, timedelta

import polars as pl

CSV3 = "eth0,100,7\neth1,250,9\neth2,50,3\n"
CSV_NAMED = "sw1,10,up\nsw2,20,down\n"


# --- reference (polars 2.0) -------------------------------------------------
def _r_parse_dates(df): return df.with_columns(pl.col("day").str.to_date("%Y-%m-%d"))
def _r_parse_datetimes(df): return df.with_columns(pl.col("ts").str.to_datetime("%Y-%m-%d %H:%M:%S"))
def _r_parse_times(df): return df.with_columns(pl.col("t").str.to_time("%H:%M:%S"))
def _r_category_codes(df): return df.with_columns(pl.col("site").cat.physical().cast(pl.UInt32).alias("code"))
def _r_codes_to_enum(codes, labels): return codes.cat.to(pl.Enum(labels))
def _r_rtt_std_seconds(df): return df.select(pl.col("rtt").dt.total_microseconds().std() / 1e6).item()
def _r_side_by_side(left, right):
    h = max(left.height, right.height)
    pad = lambda f: pl.concat([f, pl.DataFrame({c: pl.Series(c, [None] * (h - f.height), dtype=t) for c, t in f.schema.items()})]) if f.height < h else f
    return pl.concat([pad(left), pad(right)], how="horizontal")
def _r_explode_keep_empty(df): return df.explode("tags", empty_as_null=True)
def _r_csv_rx_total(text): return int(pl.read_csv(text.encode(), has_header=False)["column_1"].sum())
def _r_csv_named(text): return pl.read_csv(text.encode(), has_header=False).rename({"column_0": "host", "column_1": "vlan", "column_2": "status"})


# --- polars 1.x habits ------------------------------------------------------
def _h_parse_dates(df): return df.with_columns(pl.col("day").cast(pl.Date))
def _h_parse_datetimes(df): return df.with_columns(pl.col("ts").cast(pl.Datetime))
def _h_parse_times(df): return df.with_columns(pl.col("t").cast(pl.Time))
def _h_category_codes(df): return df.with_columns(pl.col("site").cast(pl.UInt32).alias("code"))
def _h_codes_to_enum(codes, labels): return codes.cast(pl.Enum(labels))
def _h_rtt_std_seconds(df): return df.select(pl.col("rtt").std()).item().total_seconds()
def _h_side_by_side(left, right): return pl.concat([left, right], how="horizontal")
def _h_explode_keep_empty(df): return df.explode("tags")
def _h_csv_rx_total(text): return int(pl.read_csv(text.encode(), has_header=False)["column_2"].sum())
def _h_csv_named(text): return pl.read_csv(text.encode(), has_header=False).rename({"column_1": "host", "column_2": "vlan", "column_3": "status"})


REFERENCE = {k[3:]: v for k, v in dict(globals()).items() if k.startswith("_r_")}
HABIT = {k[3:]: v for k, v in dict(globals()).items() if k.startswith("_h_")}


# --- tests ------------------------------------------------------------------
def t_parse_dates(f):
    out = f(pl.DataFrame({"day": ["2026-10-06", "2026-01-31"], "n": [1, 2]}))
    assert out.schema["day"] == pl.Date and out["day"].to_list() == [date(2026, 10, 6), date(2026, 1, 31)] and out["n"].to_list() == [1, 2]

def t_parse_datetimes(f):
    out = f(pl.DataFrame({"ts": ["2026-10-06 08:30:00", "2026-01-31 23:59:59"]}))
    assert isinstance(out.schema["ts"], pl.Datetime) and out["ts"].to_list() == [datetime(2026, 10, 6, 8, 30), datetime(2026, 1, 31, 23, 59, 59)]

def t_parse_times(f):
    out = f(pl.DataFrame({"t": ["08:30:00", "23:59:59"]}))
    assert out.schema["t"] == pl.Time and out["t"].to_list() == [time(8, 30), time(23, 59, 59)]

def t_category_codes(f):
    df = pl.DataFrame({"site": pl.Series(["rio", "sp", "rio", "bh"], dtype=pl.Categorical)})
    out = f(df)
    assert out.schema["code"] == pl.UInt32 and out["code"].to_list() == df["site"].to_physical().cast(pl.UInt32).to_list()

def t_codes_to_enum(f):
    out = f(pl.Series([2, 0, None, 1], dtype=pl.UInt32), ["low", "mid", "high"])
    assert out.dtype == pl.Enum(["low", "mid", "high"]) and out.to_list() == ["high", "low", None, "mid"]

def t_rtt_std_seconds(f):
    rtt = pl.Series("rtt", [timedelta(seconds=1), timedelta(seconds=2), timedelta(seconds=4)])
    got = f(pl.DataFrame({"rtt": rtt}))
    assert isinstance(got, float) and abs(got - 1.5275252316519468) < 1e-6

def t_side_by_side(f):
    out = f(pl.DataFrame({"a": [1, 2, 3]}), pl.DataFrame({"b": ["x", "y"]}))
    assert out.columns == ["a", "b"] and out["a"].to_list() == [1, 2, 3] and out["b"].to_list() == ["x", "y", None]

def t_explode_keep_empty(f):
    out = f(pl.DataFrame({"device": ["sw1", "sw2", "sw3"], "tags": [["core", "dc"], [], ["edge"]]}))
    assert out["device"].to_list() == ["sw1", "sw1", "sw2", "sw3"] and out["tags"].to_list() == ["core", "dc", None, "edge"]

def t_csv_rx_total(f):
    got = f(CSV3)
    assert int(got) == 400

def t_csv_named(f):
    out = f(CSV_NAMED)
    assert out.columns == ["host", "vlan", "status"] and out["vlan"].to_list() == [10, 20] and out["host"].to_list() == ["sw1", "sw2"]


TESTS = {k[2:]: v for k, v in dict(globals()).items() if k.startswith("t_")}
