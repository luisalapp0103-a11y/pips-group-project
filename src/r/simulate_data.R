# PLACEHOLDER: a simple example so main.Rmd runs from the start.
# The simulation owner replaces these functions with the real simulation.
# Keep the output columns agreed in CONTRIBUTING.md, or update them there.

#' Simulate scores for a control and a treatment group
#'
#' @param n_per_group Number of participants per group.
#' @param mean_difference Difference between the group means, in SD units.
#' @param seed Random seed, so results are reproducible.
#' @return A data frame with columns participant, group and score.
simulate_data <- function(n_per_group = 50, mean_difference = 0.5,
                          seed = 2026) {
  if (!is.numeric(n_per_group) || n_per_group < 2) {
    stop("n_per_group must be a number of at least 2")
  }

  set.seed(seed)
  data.frame(
    participant = seq_len(2 * n_per_group),
    group = rep(c("control", "treatment"), each = n_per_group),
    score = c(
      rnorm(n_per_group, mean = 0, sd = 1),
      rnorm(n_per_group, mean = mean_difference, sd = 1)
    )
  )
}

#' Save a data frame as a CSV file
#'
#' @param data Data frame to save.
#' @param file Path relative to the project folder, e.g. "data/file.csv".
#' @return The file path, invisibly.
save_data <- function(data, file) {
  write.csv(data, file, row.names = FALSE)
  invisible(file)
}
