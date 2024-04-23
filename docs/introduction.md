# ACAT Introduction

The code base has two parts: the UI part, written in PyQT, and the backend part doing the actual score judging, which is
adapted from Magdalena's research code.

## UI

The application entry point can be found under `src/acat/main.py`. The program starts by finding `ffmpeg`, a utility
tool for audio file processing, and then it launches the application UI with the `start_application` function. You can
check the in-code docs for more details for each part of the application.

## Backend

The backend part is located in the `src/acat/backend`. It has a `judge_score.py` file, containing the entry point for
judging the score. The actual implementation for the score judging is located in `praat_score_judging_japanese.py`. As
suggested by its name, it currently only contains a japanese score judging model. The original research and modeling of
the score judging method is contained under `src/acat/backend/support`, a git submodule pointing the original research
repository.  