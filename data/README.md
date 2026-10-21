# Data

This folder holds the project's data files. Real and simulated data have
exactly the same format (see `CONTRIBUTING.md`), so the analysis in
`main.Rmd` works on both.

| Folder | Created by | Description |
|---|---|---|
| `simulated/` | `main.Rmd`, section 3 | Simulated participants, one CSV file each |
| `raw/` | `src/py/experiment.py` | Real participants, one CSV file each |

`main.Rmd` analyses the files in `raw/` if there are any, and otherwise
the files in `simulated/`.