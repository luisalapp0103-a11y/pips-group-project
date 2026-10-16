# Plot results from the misinformation effect experiment

#' Plot individual misinformation acceptance scores and group means
#'
#' @param data Participant-level data containing condition and misinfo_proportion.
#' @return A ggplot object.

plot_results <- function(data) {
  ggplot2::ggplot(
    data,
    ggplot2::aes(x = condition, y = misinfo_proportion)
  ) +
    ggplot2::geom_jitter(
      width = 0.1,
      alpha = 0.5
    ) +
    ggplot2::stat_summary(
      fun = mean,
      geom = "point",
      size = 4
    ) +
    ggplot2::stat_summary(
      fun.data = ggplot2::mean_cl_normal,
      geom = "errorbar",
      width = 0.1
    ) +
    ggplot2::labs(
      x = "Condition",
      y = "Misinformation acceptance proportion",
      title = "Misinformation acceptance by condition"
    ) +
    ggplot2::theme_minimal()
}
