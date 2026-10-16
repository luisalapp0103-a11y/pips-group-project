# Analyse data from the misinformation effect experiment

#' Load and combine participant data
#'
#' @param folder Folder containing participant CSV files.
#' @return A data frame containing all participant data.
load_data <- function(folder) {
  files <- list.files(
    path = folder,
    pattern = "\\.csv$",
    full.names = TRUE
  )
  
  data_list <- lapply(files, read.csv)
  combined_data <- dplyr::bind_rows(data_list)
  
  return(combined_data)
}


#' Analyse participant responses from the misinformation experiment
#'
#' @param data Data frame containing the experiment responses.
#' @return Participant-level misinformation acceptance scores and t-test results.

analyse_data <- function(data) {
  
  # Exclude participants who failed the attention check
  clean_data <- data[data$attention_correct == 1, ]
  
  # Keep only misinformation statements
  misinformation_data <- clean_data[
    clean_data$item_type == "misinformation",
  ]
  
  # Code whether each misinformation statement was accepted as true
  misinformation_data$accepted <- misinformation_data$response >= 4
  
  # Calculate the proportion of misinformation statements accepted by each participant
  participant_data <- misinformation_data |>
    dplyr::group_by(participant_id, condition) |>
    dplyr::summarise(
      misinfo_proportion = mean(accepted),
      .groups = "drop"
    )
  # Compare misinformation acceptance between conditions
  test_result <- t.test(
    misinfo_proportion ~ condition,
    data = participant_data
  )
  return(list(
    participant_data = participant_data,
    t_test = test_result
  ))
}
