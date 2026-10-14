# PLACEHOLDER: a simple example so main.Rmd runs from the start.
# The analysis owner replaces this with the real statistical analysis.

#' Compare the scores of the two groups with a t-test
#'
#' @param data Data frame with columns group and score.
#' @return The result of t.test().
analyse_data <- function(data) {
  required_columns <- c("group", "score")
  missing_columns <- setdiff(required_columns, names(data))
  if (length(missing_columns) > 0) {
    stop("data is missing column(s): ",
         paste(missing_columns, collapse = ", "))
  }

  t.test(score ~ group, data = data)
}
