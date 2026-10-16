# How we work together

## Workflow

1. **Start from the latest `main`.** In the RStudio Git tab, switch to
   `main` and click **Pull** before you create a new branch.
2. **Work on your own branch**, never directly on `main`:

   | Branch | Who | What |
   |---|---|---|
   | `simulation` | @luisalapp0103-a11y | Simulation and power analysis (merged) |
   | `main-deliverable` | @luisalapp0103-a11y | `main.Rmd`, README, project structure |
   | `analysis` | @nisepardun | Analysis and plots |
   | `experiment` | @ElinorZYX | Python experiment |

3. **Commit often** with a message that says what changed, e.g.
   "Add power analysis to simulation".
4. **Push** your branch and open a **pull request** into `main`.
5. **Review:** the pull request is reviewed and merged by someone else,
   following the rotation below. Never merge your own pull request.

| Author of the pull request | Reviewer |
|---|---|
| @luisalapp0103-a11y | @nisepardun |
| @nisepardun | @ElinorZYX |
| @ElinorZYX | @luisalapp0103-a11y |

If a push is rejected because someone else pushed first: in the Git tab,
click the arrow next to **Pull**, choose **Pull with Rebase**, then push
again.

## Data format

The experiment and the simulation save exactly the same format, so the
analysis works on both. Do not change column names or values without
telling the group.

- **Real data:** `data/raw/participant_<ID>_<YYYYMMDD-HHMMSS>.csv`
- **Simulated data:** `data/simulated/participant_<ID>_<YYYYMMDD-HHMMSS>.csv`
- One file per participant, 24 rows (one per test statement), comma
  separated, one header row.

| Column | Values | Meaning |
|---|---|---|
| `participant_id` | e.g. `P07` | Participant ID |
| `condition` | `misinformation`, `control` | Which account was read |
| `age` | e.g. `23` | Age in years |
| `attention_correct` | `1` = correct, `0` = wrong | Attention check |
| `filler1_answered` | e.g. `31` | Sums answered in filler task 1 |
| `filler1_correct` | e.g. `29` | Sums correct in filler task 1 |
| `filler2_answered` | e.g. `18` | Sums answered in filler task 2 |
| `filler2_correct` | e.g. `18` | Sums correct in filler task 2 |
| `trial` | `1`–`24` | Position in the memory test |
| `item_id` | `1`–`24` | Statement number |
| `item_type` | `true`, `misinformation`, `foil` | Type of statement |
| `detail` | `C1`–`C8`, `other` | Critical detail the statement is about |
| `response` | `1`–`6` | 1 = certain false … 6 = certain true |
| `rt_ms` | e.g. `2350` | Response time in milliseconds |
| `timestamp` | e.g. `2026-10-21T14:15:02` | Start of the session |

## Code style

- Follow the tidyverse style guide: https://style.tidyverse.org/
- snake_case names, `<-` for assignment, double quotes, one assignment per
  line, lines of at most 80 characters.
- Settings that users may want to change are function arguments, or
  constants in SCREAMING_SNAKE_CASE at the top of a script.
- Every function gets a short comment block: what it does, its inputs and
  its output.
- Paths are always relative to the project folder (`"data/raw"`). Never use
  `setwd()` or a personal path such as `/Users/...`.
- Use `set.seed()` for anything random, so results are reproducible.
- Before a pull request, run `styler::style_file("your_file.R")` and
  `lintr::lint("your_file.R")`.
- New R packages go in `REQUIRED_PACKAGES` in `src/r/setup_packages.R`.
- Before you merge, check that `main.Rmd` still knits without errors.
