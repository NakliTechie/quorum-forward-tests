#!/bin/zsh
# Downloads every input. All 2026-cycle pages come through archive.org snapshots dated before the election.
# Usage: zsh fetch_data.sh <downloads_dir>
set -eu
D=$1; mkdir -p "$D"; cd "$D"
A=https://web.archive.org/web
W=https://en.wikipedia.org/wiki
# The Wayback Machine can redirect a dated request to a later capture, so each file is checked by the
# revision date inside it. A revision edited after 2026-11-02 is removed unread and the script stops.
get() {
  curl -sS -m 180 -L -H 'Accept-Encoding: identity' "$1" -o "$2"
  if file -b "$2" | grep -q gzip; then mv "$2" "$2.gz"; gunzip "$2.gz"; fi
  m=$(grep -oE '"dateModified":"[^"]*"' "$2" | head -1 | cut -d'"' -f4)
  if [[ -z "$m" || ! "$m" < "2026-11-03" ]]; then rm -f "$2"; echo "refused $2: revision date '$m'"; exit 1; fi
}
get "$A/20261101162621id_/$W/2026_United_States_House_of_Representatives_elections" wiki2026_house_20261101.html
get "$A/20261020173341id_/$W/2025%E2%80%932026_United_States_redistricting" wiki_redistricting_20261020.html
get "$A/20261026103106id_/$W/2024_United_States_House_of_Representatives_elections" wiki_house_2024.html
get "$A/20261019000033id_/$W/2022_United_States_House_of_Representatives_elections" wiki_house_2022.html
get "$A/20261019000016id_/$W/2020_United_States_House_of_Representatives_elections" wiki_house_2020.html
get "$A/20260915052622id_/$W/2018_United_States_House_of_Representatives_elections" wiki_house_2018.html
get "$A/20261022030118id_/$W/2016_United_States_House_of_Representatives_elections" wiki_house_2016.html
get "$A/20261018035113id_/$W/2014_United_States_House_of_Representatives_elections" wiki_house_2014.html
# MEDSL returns: byte-identical public copy; the checksum below is the one Harvard Dataverse publishes.
curl -sS -m 180 -L https://raw.githubusercontent.com/aydon14/CRProject/HEAD/public/data/jsoncsv/mit-1976-2024-house.csv -o medsl_house_1976_2024.csv
test "$(md5 -q medsl_house_1976_2024.csv)" = a9566ac393913a1af343284e837c17bb
curl -sS -m 60 -L "https://raw.githubusercontent.com/jaytimm/PresElectionResults/HEAD/data-raw/2024%20Pres%20by%20CD%20-%20Main.csv" -o pres2024_by_cd_2024lines.csv
for y in 2018 2020; do curl -sS -m 60 -L https://raw.githubusercontent.com/fivethirtyeight/data/master/partisan-lean/$y/fivethirtyeight_partisan_lean_DISTRICTS.csv -o lean538_$y.csv; done
curl -sS -m 60 -L https://raw.githubusercontent.com/fivethirtyeight/data/master/partisan-lean/fivethirtyeight_partisan_lean_DISTRICTS.csv -o lean538_2022.csv
