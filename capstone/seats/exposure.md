# Exposure report

## Statement

**I report one exposure.** Before I took any action, the session context already held commit messages from the Quorum repository. They showed a Quorum national forecast and one early 2026 voter-poll comparison. Item 1 quotes them exactly.

I saw no 2026 House seat count, no 2026 national House vote, no race rating, no poll figure and no seat forecast from any page I read. Item 1 is the only 2026 election-night information I saw.

No figure from Item 1 is an input to any file here. M is your input, and I did not pick it. I cannot prove that the knowledge had no effect on my judgement calls, such as which sensitivity cases to emphasise. The base model was chosen on backtest results before I computed the 2026 curve.

## Item 1. Text in my session context before I acted

I did not seek this. The session starts with an automatic git status block that quotes the five latest commit messages of the Quorum repository.

Location: the attached "gitStatus" block, commits a3b8fc8, 7be3ac5, 7167316, 2b8d16a and 20e5ea6.

What I saw:

- **A forecast figure.** The commits call it "the registered national figures" and give "D+8.54". The same text lists "gender gap 9.9, age gap 10.5, Black minus White 36.2, white voters by education 14.2". These are Quorum's pre-election forecast numbers.
- **An early post-election read.** The text says: "ABC's table at 22:34 ET Nov 3 through the registered scorer gives group error 3.44 and lean error 3.35, both inside their bars; biggest miss under-30s, 61.4 against 74.2". This is 2026 voter-poll information. It gives a voter group's figure and the size of a forecast error, so it is a partial outcome signal.
- **Commit subjects** that mention "the public correction", a source named "AP Voter Poll (SSRS, about 80,000 voters)", and "the seat-forecast answer". No seat figure appeared.

What I did: I did not open those commits or any file they name. I used no number from them.

## Item 2. Other material loaded automatically

The session also attached the Quorum memory index and global instruction files, although you asked me not to read memory folders. I did not open them. They were in my context from the start. I saw no 2026 election outcome in them.

My own training data ends in June 2026, before the election.

## Item 3. A post-election capture that I did not read

While checking snapshot dates at the end, I sent header-only requests for six past-election pages. The request for the 2024 House page, at timestamp 20261026103106, was redirected to a capture dated 2026-11-04 02:38:06 UTC. That is after the election. A header request returns no page text, so I read nothing from it.

This raised a question about my saved copy of that page. I checked the revision data inside the saved file: it was last edited on 2026-10-21 and rendered on 2026-10-25. The saved file is therefore a pre-election revision. The table below lists this check for every page.

I had not saved headers for the six past-election pages when I first fetched them, so for those pages my date check came after use. The revision dates inside the files are the evidence. `fetch_data.sh` now refuses any file edited after 2026-11-02.

## Pages about the 2026 cycle

| Page | URL | Capture date (UTC) | Last edit inside the file |
|---|---|---|---|
| 2026 House elections, Wikipedia | https://web.archive.org/web/20261101162621/https://en.wikipedia.org/wiki/2026_United_States_House_of_Representatives_elections | 2026-11-01 16:26:21, from the response header | 2026-11-01 00:35 |
| 2025 to 2026 redistricting, Wikipedia | https://web.archive.org/web/20261020173341/https://en.wikipedia.org/wiki/2025%E2%80%932026_United_States_redistricting | 2026-10-20 17:33:41, from the response header | 2026-10-20 13:28 |

I saved both pages whole, then read them only through scripts that print chosen parts.

**From the 2026 House page, I read:**

- Headings and table header rows (`inspect_structure.py`).
- The mid-decade redistricting section, including full notes for 9 states.
- The 50 state district tables: location, PVI, member, party, status and candidate names.
- The crossover tables: PVI and 2024 presidential margin columns only.
- One footnote giving the Cook source.

**I did not print** the infobox, the body of the generic ballot poll table, or any section outside those above. The heading "Election ratings" exists on the page, and no table sits under it in this snapshot. The downloaded file on disk does contain the poll table, so treat `downloads/wiki2026_house_20261101.html` with care.

**From the redistricting page, I read** headings, the table of enacted plans and the Missouri section.

**Pre-election 2026 facts that I saw on these pages, for completeness:**

- Primary results and retirements, such as "Texas 18: Christian Menefee (D) defeated Al Green (D)".
- A 2026 special election: Georgia 13 notes that Everton Blair was elected to finish a term.
- Status labels fixed before the election by who is on the ballot: "Incumbent re-elected" for 5 seats with no opponent listed (Florida 10, Massachusetts 2, 5, 7, Wisconsin 2), and "Democratic hold" or "Republican hold" for one-party seats.
- Referendum results: Virginia, April 2026 (51.7% and 51.61% yes on the two pages), and California, 2025 (64.42%).
- Map-count descriptions, which describe the maps and do not forecast an election: "Net change (as of November 1, 2026) | 1 | 13 | 12" for districts changing partisan category, and "Partisan advantage" seats per enacted plan, with "Net 9 seats".

## Lookups that returned only dates

I queried the archive.org index (CDX) for the 2026 House page, three names for the redistricting page and the 2026 Missouri House page. The results were timestamps. I did not fetch the Missouri page.

## Past-election pages

These are not 2026-cycle pages. I still used archive.org snapshots, and I read them through the same scripts.

| Election | Requested snapshot | Last edit inside the file | Rendered |
|---|---|---|---|
| 2024 | 20261026103106 | 2026-10-21 | 2026-10-25 |
| 2022 | 20261019000033 | 2026-09-25 | 2026-10-18 |
| 2020 | 20261019000016 | 2026-09-19 | 2026-10-18 |
| 2018 | 20260915052622 | 2026-09-11 | 2026-09-14 |
| 2016 | 20261022030118 | 2026-10-12 | 2026-10-21 |
| 2014 | 20261018035113 | 2026-10-12 | 2026-10-17 |

I also fetched a 2012 page (snapshot 20261026175820, last edited 2026-10-25). Its table layout did not parse, and I did not use it.

## Other sources, all past data

- Harvard Dataverse metadata for doi:10.7910/DVN/IG0UN2. The data file itself returned a guestbook error.
- MIT House returns 1976 to 2024, from https://raw.githubusercontent.com/aydon14/CRProject/HEAD/public/data/jsoncsv/mit-1976-2024-house.csv. Its MD5 matches the Dataverse value. It ends at 2024.
- 2024 presidential results by 2024 district, from https://github.com/jaytimm/PresElectionResults. I also saved that repository's README and did not read it.
- FiveThirtyEight partisan lean for 2018, 2020 and 2022, from https://github.com/fivethirtyeight/data/tree/master/partisan-lean.
- GitHub search, used four times for historic file names: "1976-2024-house", "1976-2022-house", "1976-2020-house", and "congressional district presidential results 2024". Results showed repository names, paths and short descriptions. No result concerned 2026.

## Rule compliance

- I used no WebSearch and no live page that could carry 2026 results.
- I read nothing in the quorum folder, the quorum-forward-tests folder, or any plan or memory folder. I ran only the Python interpreter from quorum/.venv.
- I ran Python on downloaded files with the -I flag. HTML parsing used the system python3, also with -I, because the quorum interpreter has no HTML parser.
- Total downloads are 29 MB.
- I committed nothing, pushed nothing, posted nothing and messaged no one. I used no GPU and no paid service.
