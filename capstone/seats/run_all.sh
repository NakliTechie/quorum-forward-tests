#!/bin/zsh
# Rebuilds every result from the files in downloads/. Run from this folder.
# Usage: zsh run_all.sh [python-with-numpy-and-pandas]   (python3 must have beautifulsoup4)
set -eu
PY=${1:-python3}
python3 -I parse_2026_page.py downloads/wiki2026_house_20261101.html wiki2026_rows.json
python3 -I parse_history_pages.py downloads wiki_hist_rows.json 2014 2016 2018 2020 2022 2024
$PY -I build_panel.py downloads/medsl_house_1976_2024.csv wiki_hist_rows.json panel_2014_2024.csv
$PY -I build_baseline_2026.py wiki2026_rows.json downloads/pres2024_by_cd_2024lines.csv district_baseline.csv
$PY -I check_past_pvi.py panel_2014_2024.csv downloads
$PY -I backtest.py panel_2014_2024.csv official_seats.json backtest_all_variants.csv
$PY -I turnout_check.py panel_2014_2024.csv
$PY -I diagnostics.py panel_2014_2024.csv official_seats.json
$PY -I run_curve.py panel_2014_2024.csv district_baseline.csv .
