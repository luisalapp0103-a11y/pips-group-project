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
#' @param seed Random seed, so the same data come out every time.
#' @return One data frame with the rows of all participants.
simulate_study <- function(n_per_group = 20, effect_size = 0.5, seed = 2026) {
  if (!is.numeric(n_per_group) || n_per_group < 1) {
    stop("n_per_group must be a number of at least 1")
  }

  set.seed(seed)
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
