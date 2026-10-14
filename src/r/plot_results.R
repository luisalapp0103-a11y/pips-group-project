# PLACEHOLDER: a simple example so main.Rmd runs from the start.
# The analysis owner replaces this with the real, informative plot.

#' Plot individual scores and the group means
#'
#' @param data Data frame with columns group and score.
#' @return A ggplot object.
plot_results <- function(data) {
  ggplot(data, aes(x = group, y = score)) +
    geom_jitter(width = 0.1, alpha = 0.5) +
    stat_summary(fun = mean, geom = "point", size = 4, colour = "darkred") +
    labs(
      x = "Group",
      y = "Score",
      title = "Scores per group (placeholder plot)"
    ) +
    theme_minimal()
}
