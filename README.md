# Does Misleading Information Change What We Remember?

This repository studies the **misinformation effect**: people who receive
false information after an event often remember those false details as
true. It contains three parts that work together:

1. **A simulation and power analysis in R** that shows how many
   participants a study needs to detect the effect, based on the effect
   size reported by Sievwright et al. (2021).
2. **A short experiment in Python** in which participants read a story,
   read an eyewitness account with or without false details, and take a
   memory test.
3. **An analysis and visualisation in R** that tests whether misinformed
   participants accept more false details as true.

Everything comes together in `main.Rmd`, which runs from top to bottom and
explains each step. It uses real data when they exist and simulated data
otherwise, so it always runs.

We created this project for the group assignment of the course Programming
in Psychological Science (PIPS), Research Master Psychology, University of
Amsterdam.

## Getting started

### Requirements

- R 4.4 or newer, and RStudio (recommended)
- Python 3.10 or newer (only needed to run the experiment)

### 1. Clone the repository

```
git clone https://github.com/luisalapp0103-a11y/pips-group-project.git
```

Or in RStudio: *File → New Project → Version Control → Git*, then paste the
repository URL.

### 2. Run the main document (R)

Install the packages needed to knit R Markdown:

```r
install.packages(c("knitr", "rmarkdown"))
```

Open `pips-group-project.Rproj`, then open `main.Rmd` and click **Knit**.
All other R packages (dplyr, ggplot2) are installed automatically by
`src/r/setup_packages.R`.

The first knit takes a few minutes, because the effect-size calibration
and power analysis simulate thousands of studies. The results are cached,
so later knits are fast.

### 3. Run the experiment (Python, optional)

The experiment uses only Tkinter, which comes with Python, so nothing extra
needs to be installed. From the project folder, in a terminal:

```
python3 src/py/experiment.py
```

Each participant's responses are saved as one CSV file in `data/raw/`.
Knit `main.Rmd` again to analyse them.

## Repository structure

```
pips-group-project/
├── data/
│   ├── simulated/          # simulated participants (created by main.Rmd)
│   └── raw/                # real participants (created by the experiment)
├── materials/              # story, accounts and test statements
├── src/
│   ├── py/
│   │   └── experiment.py       # the experiment
│   └── r/
│       ├── setup_packages.R    # installs and loads R packages
│       ├── simulate_experiment.R  # simulation, calibration, power analysis
│       ├── analyse_data.R      # statistical analysis
│       └── plot_results.R      # plots
├── main.Rmd                # main deliverable: run this file
├── references.bib          # references cited in main.Rmd
├── CONTRIBUTING.md         # how we work together, data format
└── README.md
```

## Data format

Every participant produces one CSV file with 24 rows (one per test
statement). The simulated files use exactly the same columns, so the
analysis works on both. The full column list is in `CONTRIBUTING.md`.

## Dependencies

- **R:** dplyr (data manipulation), ggplot2 (plots), knitr and rmarkdown
  (knitting `main.Rmd`)
- **Python:** Tkinter and the standard library only

## References

Loftus, E. F. (2005). Planting misinformation in the human mind: A 30-year
investigation of the malleability of memory. *Learning & Memory, 12*(4),
361–366. https://doi.org/10.1101/lm.94705

Loftus, E. F., Miller, D. G., & Burns, H. J. (1978). Semantic integration
of verbal information into a visual memory. *Journal of Experimental
Psychology: Human Learning and Memory, 4*(1), 19–31.
https://doi.org/10.1037/0278-7393.4.1.19

Sievwright, O., Philipp, M., Drummond, A., Knapp, K., & Ross, K. (2021).
Misinformation effects in an online sample: results of an experimental
study with a five day retention interval. *PeerJ, 9*, e12299.
https://doi.org/10.7717/peerj.12299

## Team

| Responsibility | GitHub |
|---|---|
| Project structure, main deliverable, simulation and power analysis | @luisalapp0103-a11y |
| Experiment (Python) | @ElinorZYX |
| Statistical analysis and visualisation | @nisepardun |
