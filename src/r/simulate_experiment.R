# Simulate data for the misinformation experiment.
#
# The simulated files have exactly the same format as the files Elinor's
# experiment will save (see "Misinformation Experiment Specification",
# section "Data output"). This lets us build and test the analysis before
# real data exists, and later run a power analysis.
#
# How responses are simulated: every statement gives a participant some
# "evidence that it is true" (a normal distribution with SD 1). High
# evidence leads to a high response (6 = certain true), low evidence to a
# low response (1 = certain false). Misinformed participants get extra
# evidence for the misinformation statements: that is the effect.

# Settings ----------------------------------------------------------------

# Mean evidence per statement type (standard normal scale).
EVIDENCE_TRUE <- 1.0
EVIDENCE_FOIL <- -1.0
EVIDENCE_MISINFORMATION <- -0.6

# Cut-offs that turn evidence into the 1-6 response scale.
RESPONSE_CUTOFFS <- c(-Inf, -1.5, -0.75, 0, 0.75, 1.5, Inf)

# How much participants differ in their general tendency to answer "true".
PARTICIPANT_BIAS_SD <- 0.3

# Proportion of participants who pass the attention check.
ATTENTION_PASS_RATE <- 0.95

# Power we aim for and significance level of the test.
TARGET_POWER <- 0.80
ALPHA <- 0.05


#' Build the table of the 24 test statements
#'
#' Same item_id, item_type and detail as the "Memory test" table in the
#' specification.
#'
#' @return A data frame with 24 rows and columns item_id, item_type, detail.
make_test_items <- function() {
  data.frame(
    item_id = 1:24,
    item_type = c(
      rep("true", 8), rep("misinformation", 8),
      rep("true", 4), rep("foil", 4)
    ),
    detail = c(paste0("C", 1:8), paste0("C", 1:8), rep("other", 8))
  )
}


#' Simulate the data of one participant
#'
#' @param participant_number Whole number; odd = misinformation, even =
#'   control (same rule as the experiment).
#' @param effect_size Extra evidence for the misinformation statements in
#'   the misinformation condition (on the evidence scale, not Cohen's d).
#' @param items Table of test statements, see make_test_items().
#' @return A data frame with 24 rows in the format of the specification.
simulate_participant <- function(participant_number, effect_size = 0.5,
                                 items = make_test_items()) {
  if (!is.numeric(participant_number) || participant_number < 1) {
    stop("participant_number must be a whole number of at least 1")
  }
  if (!is.numeric(effect_size) || length(effect_size) != 1) {
    stop("effect_size must be a single number")
  }

  condition <- ifelse(participant_number %% 2 == 1, "misinformation", "control")
  n_items <- nrow(items)

  # Mean evidence for each statement, depending on its type
  evidence_mean <- ifelse(
    items$item_type == "true", EVIDENCE_TRUE,
    ifelse(items$item_type == "foil", EVIDENCE_FOIL, EVIDENCE_MISINFORMATION)
  )

  # The misinformation effect
  if (condition == "misinformation") {
    is_misinformation <- items$item_type == "misinformation"
    evidence_mean[is_misinformation] <-
      evidence_mean[is_misinformation] + effect_size
  }

  participant_bias <- rnorm(1, mean = 0, sd = PARTICIPANT_BIAS_SD)
  evidence <- rnorm(n_items, mean = evidence_mean + participant_bias, sd = 1)
  response <- cut(evidence, breaks = RESPONSE_CUTOFFS, labels = FALSE)

  # Statements are shown in a new random order for every participant
  shown_order <- sample(n_items)
  shown_items <- items[shown_order, ]

  filler1_answered <- max(0, round(rnorm(1, mean = 30, sd = 5)))
  filler2_answered <- max(0, round(rnorm(1, mean = 18, sd = 3)))
  start_time <- as.POSIXct("2026-10-21 10:00:00") + participant_number * 900

  data.frame(
    participant_id = sprintf("S%02d", participant_number),
    condition = condition,
    age = sample(18:30, 1),
    attention_correct = rbinom(1, 1, ATTENTION_PASS_RATE),
    filler1_answered = filler1_answered,
    filler1_correct = filler1_answered - rbinom(1, filler1_answered, 0.05),
    filler2_answered = filler2_answered,
    filler2_correct = filler2_answered - rbinom(1, filler2_answered, 0.05),
    trial = seq_len(n_items),
    item_id = shown_items$item_id,
    item_type = shown_items$item_type,
    detail = shown_items$detail,
    response = response[shown_order],
    rt_ms = round(rlnorm(n_items, meanlog = log(2500), sdlog = 0.4)),
    timestamp = format(start_time, "%Y-%m-%dT%H:%M:%S")
  )
}


#' Simulate a whole study
#'
#' @param n_per_group Number of participants per condition.
#' @param effect_size See simulate_participant().
#' @param seed Random seed, so the same data come out every time. Use NULL
#'   for a different random study on every call (needed for power analysis).
#' @return One data frame with the rows of all participants.
simulate_study <- function(n_per_group = 20, effect_size = 0.5, seed = 2026) {
  if (!is.numeric(n_per_group) || n_per_group < 1) {
    stop("n_per_group must be a number of at least 1")
  }

  if (!is.null(seed)) {
    set.seed(seed)
  }
  participants <- list()
  for (number in seq_len(2 * n_per_group)) {
    participants[[number]] <- simulate_participant(number, effect_size)
  }
  do.call(rbind, participants)
}


#' Save simulated data as one CSV file per participant
#'
#' File names follow the specification:
#' participant_<ID>_<YYYYMMDD-HHMMSS>.csv
#'
#' @param study_data Data frame from simulate_study().
#' @param folder Folder to save into, relative to the project folder.
#' @return The folder, invisibly.
save_simulated_study <- function(study_data, folder = "data/simulated") {
  dir.create(folder, recursive = TRUE, showWarnings = FALSE)

  for (id in unique(study_data$participant_id)) {
    participant_rows <- study_data[study_data$participant_id == id, ]
    start_time <- as.POSIXct(participant_rows$timestamp[1],
                             format = "%Y-%m-%dT%H:%M:%S")
    file_name <- paste0("participant_", id, "_",
                        format(start_time, "%Y%m%d-%H%M%S"), ".csv")
    write.csv(participant_rows, file.path(folder, file_name), row.names = FALSE)
  }

  invisible(folder)
}


# Power analysis ----------------------------------------------------------
#
# Idea: simulate the study many times, run the test each time, and count how
# often the effect is significant. That proportion is the power: the chance
# that a study of this size finds the effect if it really exists.


#' Proportion of misinformation statements each participant called "true"
#'
#' Participants who failed the attention check are left out. A response of
#' 4-6 counts as "true".
#'
#' @param study_data Data frame in the format of the specification.
#' @return A data frame with one row per participant and columns
#'   participant_id, condition and endorsed (proportion 0-1).
summarise_endorsement <- function(study_data) {
  passed <- study_data[study_data$attention_correct == 1, ]
  misinformation_rows <- passed[passed$item_type == "misinformation", ]
  misinformation_rows$endorsed <- misinformation_rows$response >= 4

  aggregate(endorsed ~ participant_id + condition,
            data = misinformation_rows, FUN = mean)
}


#' p-value of the misinformation effect in one study
#'
#' Welch t-test comparing the endorsement of misinformation statements
#' between the two conditions.
#'
#' @param study_data Data frame in the format of the specification.
#' @return The p-value, or NA if the test could not be run.
test_misinformation_effect <- function(study_data) {
  per_participant <- summarise_endorsement(study_data)
  tryCatch(
    t.test(endorsed ~ condition, data = per_participant)$p.value,
    error = function(e) NA
  )
}


#' Estimate the power for one group size
#'
#' @param n_per_group Number of participants per condition.
#' @param effect_size See simulate_participant().
#' @param n_simulations How many studies to simulate. More = more precise,
#'   but slower.
#' @param alpha Significance level.
#' @return Proportion of simulated studies with p < alpha.
estimate_power <- function(n_per_group, effect_size = 0.5,
                           n_simulations = 200, alpha = ALPHA) {
  if (n_per_group < 5) {
    stop("n_per_group must be at least 5 for a meaningful t-test")
  }

  p_values <- numeric(n_simulations)
  for (i in seq_len(n_simulations)) {
    study <- simulate_study(n_per_group, effect_size, seed = NULL)
    p_values[i] <- test_misinformation_effect(study)
  }
  mean(p_values < alpha, na.rm = TRUE)
}


#' Estimate the power for several group sizes
#'
#' @param group_sizes Numbers of participants per condition to try.
#' @param effect_size See simulate_participant().
#' @param n_simulations Simulated studies per group size.
#' @param seed Random seed, so the curve is the same every time.
#' @return A data frame with columns n_per_group and power.
power_curve <- function(group_sizes = c(5, 10, 15, 20, 30, 40),
                        effect_size = 0.5, n_simulations = 200,
                        seed = 2026) {
  set.seed(seed)
  power <- numeric(length(group_sizes))
  for (i in seq_along(group_sizes)) {
    power[i] <- estimate_power(group_sizes[i], effect_size, n_simulations)
  }
  data.frame(n_per_group = group_sizes, power = power)
}


#' Plot a power curve
#'
#' @param curve Data frame from power_curve().
#' @param target_power Power we aim for, drawn as a dashed line.
#' @return A ggplot object.
plot_power_curve <- function(curve, target_power = TARGET_POWER) {
  ggplot2::ggplot(curve, ggplot2::aes(x = n_per_group, y = power)) +
    ggplot2::geom_hline(yintercept = target_power, linetype = "dashed",
                        colour = "grey50") +
    ggplot2::geom_line(colour = "steelblue") +
    ggplot2::geom_point(colour = "steelblue", size = 2.5) +
    ggplot2::scale_y_continuous(
      limits = c(0, 1),
      labels = function(x) paste0(round(x * 100), "%")
    ) +
    ggplot2::labs(
      x = "Participants per condition",
      y = "Power",
      title = "How many participants do we need?",
      subtitle = paste0("Dashed line: ", round(target_power * 100),
                        "% power")
    ) +
    ggplot2::theme_minimal()
}
