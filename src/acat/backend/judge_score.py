import io
import math
import pathlib
from pathlib import Path
from typing import Tuple

import numpy as np
import pandas as pd
import parselmouth
from praatio import textgrid

from acat.ui.audio_file import PraatScore

_SUPPORT_PATH = Path(__file__).parent / "support"
_SUPPORT_FUNC_PATH = _SUPPORT_PATH / "functions"

_ANALYSIS_PRAAT_SCRIPT = _SUPPORT_FUNC_PATH / "SyllableNucleiv3.praat"
_ANALYSIS_PRAAT_SCRIPT_STR = str(_ANALYSIS_PRAAT_SCRIPT.absolute())

print(_ANALYSIS_PRAAT_SCRIPT_STR, _ANALYSIS_PRAAT_SCRIPT.exists())


def _run_praat_script(audio_file_path: Path) -> Tuple[pd.DataFrame, pd.DataFrame]:
    audio_file_path_str = str(audio_file_path.absolute())
    tab1 = parselmouth.praat.run_file(
        _ANALYSIS_PRAAT_SCRIPT_STR,
        audio_file_path_str,
        "None",
        -25,
        2,
        0.4,
        True,
        "English",
        1,
        "Table",
        "OverWriteData",
        True,
    )

    tab2 = parselmouth.praat.run_file(
        _ANALYSIS_PRAAT_SCRIPT_STR,
        audio_file_path_str,
        "None",
        -25,
        2,
        0.4,
        True,
        "English",
        1,
        "Table",
        "OverWriteData",
        False,
    )

    return pd.read_table(
        io.StringIO(parselmouth.praat.call(tab1[2], "List", False))
    ), pd.read_table(io.StringIO(parselmouth.praat.call(tab2[0], "List", False)))


def _analysis_from_praat_script(
    audio_file_path: Path
) -> Tuple[pd.DataFrame, pd.DataFrame]:
    true_data, false_data = _run_praat_script(audio_file_path)

    selected_cols = ["type", "F0", "F1", "F2", "F3"]
    true_data = true_data[selected_cols]

    true_data = true_data[true_data["type"] == "syll"]
    true_data.replace("--undefined--", np.nan, inplace=True)
    true_data = true_data.astype({"F0": float, "F1": float, "F2": float, "F3": float})

    true_data_sub = pd.DataFrame(
        {
            "meanf0": true_data["F0"].mean(skipna=True),
            "meanf1": true_data["F1"].mean(skipna=True),
            "meanf2": true_data["F2"].mean(skipna=True),
            "meanf3": true_data["F3"].mean(skipna=True),
            "sdf0": true_data["F0"].std(skipna=True),
            "sdf1": true_data["F1"].std(skipna=True),
            "sdf2": true_data["F2"].std(skipna=True),
            "sdf3": true_data["F3"].std(skipna=True),
            "minf0": true_data["F0"].min(skipna=True),
            "maxf0": true_data["F0"].max(skipna=True),
        },
        index=[0],
    )

    true_data_sub["rangef0"] = true_data_sub["maxf0"] - true_data_sub["minf0"]
    true_data_sub["coeff1"] = math.log10(
        true_data_sub["sdf1"] / true_data_sub["meanf1"]
    )
    true_data_sub["coeff2"] = math.log10(
        true_data_sub["sdf2"] / true_data_sub["meanf2"]
    )
    true_data_sub["coeff3"] = math.log10(
        true_data_sub["sdf3"] / true_data_sub["meanf3"]
    )
    true_data_sub = true_data_sub[["rangef0", "coeff1", "coeff2", "coeff3"]]

    false_data.columns = false_data.columns.str.strip()
    false_data = false_data.rename(columns={"speechrate(nsyll/dur)": "speechrate"})
    false_data["pauses"] = false_data["npause"] + false_data["nrFP"]
    false_data = false_data[["speechrate", "pauses"]]

    return true_data_sub, false_data


def _analyze_text_grid(text_grid_path: pathlib.Path) -> pd.DataFrame:
    text_grid_path_str = str(text_grid_path.absolute())
    tg = textgrid.openTextgrid(text_grid_path_str, includeEmptyIntervals=False)
    tier = tg.getTier(tg.tierNames[2])

    start_times = []
    end_times = []
    labels = []

    for interval in tier.entries:
        start_times.append(interval[0])
        end_times.append(interval[1])
        labels.append(interval[2])

    textgrid_df = pd.DataFrame(
        np.column_stack(
            [start_times, end_times, labels, np.subtract(end_times, start_times)]
        ),
        columns=["start", "stop", "type", "diff"],
    )
    textgrid_df = textgrid_df.astype({"start": float, "stop": float, "diff": float})
    textgrid_df = textgrid_df[textgrid_df["type"] == "syll"]
    textgrid_df.replace("--undefined--", np.nan, inplace=True)

    df_sub = pd.DataFrame(
        {"sdsylldur": math.log10(textgrid_df["diff"].std(skipna=True))}, index=[0]
    )

    return df_sub


def generate_praat_score(
    audio_file_path: pathlib.Path, text_grid_path: pathlib.Path
) -> PraatScore:
    df1, df2 = _analysis_from_praat_script(audio_file_path)
    df3 = _analyze_text_grid(text_grid_path)
    final = pd.concat([df2, df3, df1], axis=1)

    comp_avg = (
        2.138
        + (2.701 * final["speechrate"])
        + (0.015 * final["pauses"])
        + (-0.020 * final["rangef0"])
        + (3.821 * final["sdsylldur"])
        + (-1.414 * final["coeff1"])
        + (-5.549 * final["coeff2"])
        + (3.228 * final["coeff3"])
    )
    comp_score = comp_avg.iloc[0]

    native_avg = (
        -0.537
        + (2.654 * final["speechrate"])
        + (-0.001 * final["pauses"])
        + (-0.019 * final["rangef0"])
        + (3.170 * final["sdsylldur"])
        + (-0.622 * final["coeff1"])
        + (-8.016 * final["coeff2"])
        + (3.575 * final["coeff3"])
    )
    native_score = native_avg.iloc[0]

    return PraatScore(comp_score, native_score)
