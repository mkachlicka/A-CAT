import pathlib
from typing import Literal

from acat.backend.praat_score_judging_japanese import generate_praat_score_japanese_impl
from acat.ui.audio_file import PraatScore


def generate_praat_score(
    audio_file_path: pathlib.Path, model: Literal["japanese"] = "japanese"
) -> PraatScore:
    if model == "japanese":
        return generate_praat_score_japanese_impl(audio_file_path)
    else:
        raise ValueError("Unknown Language Model")
