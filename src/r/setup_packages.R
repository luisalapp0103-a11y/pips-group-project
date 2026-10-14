# Packages used in this project. Add new packages here, so every group member
# and the graders get the same setup automatically.
REQUIRED_PACKAGES <- c("dplyr", "ggplot2")

#' Install missing packages and load all project packages
#'
#' @param packages Character vector of package names.
#' @return Nothing; called for its side effect of loading packages.
install_and_load <- function(packages = REQUIRED_PACKAGES) {
  for (package in packages) {
    if (!requireNamespace(package, quietly = TRUE)) {
      install.packages(package, repos = "https://cloud.r-project.org")
    }
    library(package, character.only = TRUE)
  }
}
