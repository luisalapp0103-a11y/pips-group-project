# Project title

<!-- TODO: replace the title and every line marked TODO once the topic is chosen. -->

TODO: two or three sentences on what this project does and why it is useful
for psychology researchers or students. For example: "This repository
simulates ... to show ...".

We created this project for the group assignment of the course Programming in
Psychological Science (PIPS), Research Master Psychology, University of
Amsterdam.

## Citation

TODO: add the citation for this repository.

## Getting started

This project requires R 4.4 or newer. RStudio is recommended.

1. Clone the repository:

   ```
   git clone https://github.com/TODO-USERNAME/TODO-REPOSITORY.git
   ```

   Or in RStudio: *File → New Project → Version Control → Git*, then paste the
   repository URL.

2. Install the packages needed to knit an R Markdown document:

   ```r
   install.packages(c("knitr", "rmarkdown"))
   ```

   All other packages are installed automatically the first time you run
   `main.Rmd` (see `src/r/setup_packages.R`).

3. Open `main.Rmd` and run the chunks from top to bottom, or click **Knit**.

## Repository structure

```
pips-group-project/
├── data/                   # data files (created by main.Rmd)
├── src/
│   └── r/
│       ├── setup_packages.R   # installs and loads all packages
│       ├── simulate_data.R    # data simulation
│       ├── analyse_data.R     # statistical analysis
│       └── plot_results.R     # plots
├── main.Rmd                # main deliverable: run this file
├── references.bib          # references cited in main.Rmd
├── CONTRIBUTING.md         # how we work together
└── README.md
```

## Using the project

`main.Rmd` walks you through the following steps:

1. TODO: simulate the data / load the data.
2. TODO: run the statistical analysis.
3. TODO: visualise the results.
4. TODO: (if applicable) explore the results in the Shiny app.

## Dependencies

The project uses dplyr for data manipulation and ggplot2 for plots.
TODO: add any other packages and what they are used for. `knitr` and
`rmarkdown` are needed to knit the main document.

## References

TODO: list the references used, in APA style. The same references go in
`references.bib`, so they are cited automatically in `main.Rmd`.

## Team

| Responsibility | Group member |
|---|---|
| Project structure, README and main deliverable | TODO |
| Data simulation / app | TODO |
| Statistical analyses and visualisations | TODO |
