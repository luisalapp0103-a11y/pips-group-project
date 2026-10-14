# How we work together

## Workflow

1. **Pull first.** Before you start, click **Pull** in the RStudio Git tab, so
   you work on the latest version.
2. **Work on your own branch**, never directly on `main`. In the RStudio Git
   tab, click the branch icon and name it after your task, e.g.
   `simulation` or `analysis`.
3. **Commit often** with a short message that says what changed, e.g.
   "Add power simulation function".
4. **Push** your branch and open a **pull request** on GitHub.
5. **Review rotation:** the pull request is reviewed and merged by the next
   person in the list below.

| Author of the pull request | Reviewer |
|---|---|
| TODO (structure & main deliverable) | TODO (simulation / app) |
| TODO (simulation / app) | TODO (analyses & plots) |
| TODO (analyses & plots) | TODO (structure & main deliverable) |

## Agreements between our parts

`main.Rmd` connects everyone's code, so these names must stay the same.
If you need to change one, tell the group and update this table.

| What | Agreed name |
|---|---|
| Simulation function | `simulate_data()` in `src/r/simulate_data.R` |
| Data file | `data/simulated_data.csv` |
| Data columns | `participant`, `group`, `score` (TODO: update) |
| Analysis function | `analyse_data()` in `src/r/analyse_data.R` |
| Plot function | `plot_results()` in `src/r/plot_results.R` |

## Code style

- Follow the tidyverse style guide: https://style.tidyverse.org/
- snake_case names, `<-` for assignment, double quotes, one assignment per
  line, lines of at most 80 characters.
- Fixed values that users may want to change are function arguments, or
  constants in SCREAMING_SNAKE_CASE at the top of a script.
- Every function gets a short comment block: what it does, its inputs and
  its output (see the existing scripts).
- Paths are always relative to the project folder (`"data/file.csv"`).
  Never use `setwd()`.
- Use `set.seed()` for anything random, so results are reproducible.
- Before a pull request, run `styler::style_file("your_file.R")` and
  `lintr::lint("your_file.R")`.
- New packages go in `REQUIRED_PACKAGES` in `src/r/setup_packages.R`.
- Before you merge, check that `main.Rmd` still knits without errors.
