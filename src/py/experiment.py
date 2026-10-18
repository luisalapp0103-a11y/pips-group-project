#Experiment

#General information:
#Research Objective:
#

from psychopy import visual, core, event, gui
import csv
from pathlib import Path
from datetime import datetime
import random

# ----- Experiment materials -----
welcome_text = (
    "Welcome to the misinformation effect experiment!\n\n"
    "This is a study about memory for everyday events.\nIt takes about 15 min.\nYour participation will be anonymous.\n\n"
    "Please indicate you consent to join the experiment."
)
instruction_text = ("You will now read a short story, one sentence at a time.\nPlease pay attention.")

stories = [
    "It is a rainy Tuesday morning at Café Linde, a small café on a busy street.",
    "A young woman in a red scarf sits at a table by the window, working on her laptop with a cup of tea.",
    "Next to her laptop lie her phone and a black leather wallet.",
    "A tall man in a green jacket comes in and orders a coffee at the counter.",
    "The barista, an older man with glasses, tells him the price: 3 euros 50.",
    "The man pays with coins and sits down at the table next to the woman.",
    "The woman gets up to go to the toilet and leaves her things on the table.",
    "The man looks around, then slips the woman's wallet into his jacket pocket.",
    "He leaves his coffee untouched, walks out of the café and turns left.",
    "A few minutes later, the woman comes back and sees that her wallet is gone.",
    "She tells the barista, who calls the police.",
    "Two police officers arrive and write down the woman's description of the man."
]
attention_check_question = "What was the name of the café?"
option_text = ["AAAA", "BBBB", "Linde", "DDDD"]
option_position = [(0, 0.20), (0, 0.05), (0, -0.10), (0, -0.25)]

filler_instruction = "Please complete the following arithmetic problems.\nType your answers and press enter to proceed to the next question."

# ----- Experiment parameters -----
story_time = 8
filler1_time = 300

# ----- General setting -----
# data folders
project_folder = Path(__file__).resolve().parents[2]
data_folder = project_folder / "data" / "raw"
data_folder.mkdir(parents=True, exist_ok=True)

# participant info
participant_info = {
    "Participant_id": "",
    "Age": "", 
    "Gender": ""
}

dialog = gui.DlgFromDict(
    dictionary = participant_info,
    title = "Participant information",
    sortKeys = False
)

if not dialog.OK:
    core.quit()

# creating data csv file & temporary data storage
data_file = data_folder / "data.csv"
participant_row = {
    "Participant_id": participant_info["Participant_id"],
    "Age": participant_info["Age"],
    "Gender": participant_info["Gender"],
    "Time of experiment": datetime.now().isoformat(timespec="seconds")
}

# main window
win = visual.Window(
    size = (800, 600),
    fullscr = False,
    color = "gray",
    units = "height"
)
# end experiment with escape 
def esc_quit():
    if event.getKeys(keyList=["escape"]):
        win.close()
        core.quit()
# !!change to full screen before running

# ----- Functions -----
# creating clicking buttons
def create_button(pos, text, win = win):
    label = visual.TextStim(
            win = win,
            text = text,
            height = 0.035,
            color = "white",
            pos = pos
        )
    text_width = label.boundingBox[0] / win.size[1]
    button = visual.Rect(
        win = win,
        width = text_width + 0.08,
        height = 0.10,
        pos = pos,
        fillColor = "black",
        lineColor = "white"
    )
    return button, label

def text_display(pos, text = "", win = win):
    screen = visual.TextStim(
        win = win,
        text = text,
        color = "white",
        height = 0.05,
        pos = pos
    )
    return screen

# ----- Welcome screen -----

# welcome text
welcome_screen = text_display((0, 0.15), welcome_text)

# Consent button
consent_button, consent_label = create_button((0, -0.30), "I consent to joining the experiment.")

# click goes to next screen
mouse = event.Mouse(win=win)
mouse.setVisible(True)
while True:
    esc_quit()
    welcome_screen.draw()
    consent_button.draw()
    consent_label.draw()
    win.flip()
    if mouse.isPressedIn(consent_button, buttons=[0]):
        break


# ----- Instruction screen -----
# instruction text
instruction_screen = text_display((0, 0.15), instruction_text)

# Start button
start_button, start_button_label = create_button((0, -0.25), "Start")

# click goes to next screen
mouse = event.Mouse(win=win)
mouse.setVisible(True)
while True:
    esc_quit()
    instruction_screen.draw()
    start_button.draw()
    start_button_label.draw()
    win.flip()
    if mouse.isPressedIn(start_button, buttons = [0]):
        break

# ----- Story reading-----
story_clock = core.Clock()
story_screen = text_display((0, 0))

# show one sentence every 8s
for i in stories:
    story_screen.text = i
    story_screen.draw()
    win.flip()

    story_clock.reset()
    while story_clock.getTime() < story_time:
        esc_quit()
        core.wait(0.01)

# ----- Attention check -----
attention_check = text_display((0, 0.35), attention_check_question)
option_buttons = [create_button(pos, text) for pos, text in zip(option_position, option_text)]
selected = None
mouse = event.Mouse(win=win)
mouse.setVisible(True)
while selected is None:
    esc_quit()
    attention_check.draw()
    for button, label in option_buttons:
        button.draw()
        label.draw()
    win.flip()
    for index, (button, label) in enumerate(option_buttons):
        if mouse.isPressedIn(button, buttons=[0]):
            selected = index
            break

# storing attention check results
participant_row["attention_response"] = selected == 2


# ----- Filler Task1 -----
filler_instruction_screen = text_display((0, 0.15), filler_instruction)
filler_timer = core.Clock()
calculation = ["+", "-", "*"]
arithmetic_question = text_display((0, 0))
answer_text = text_display((0, -0.15))
while filler_timer.getTime() < filler1_time:
    # create question
    number_A, number_B = random.randint(0, 100), random.randint(0, 100)
    operator = random.choice(calculation)
    arithmetic_question.text = f"{number_A} {operator} {number_B}= ?"
    
    #collect answer
    typed_answer = ""
    event.clearEvents(eventType="keyboard")
    
    #execute
    while filler_timer.getTime() < filler1_time:
        filler_instruction_screen.draw()
        arithmetic_question.draw()
        answer_text.text = f"Your answer: {typed_answer}"
        answer_text.draw()
        win.flip()

        keys = event.getKeys()

        for key in keys:
            if key == "escape":
                win.close()
                core.quit()
            elif key == "backspace":
                typed_answer = typed_answer[:-1]
            elif key == "minus" and typed_answer == "":
                typed_answer = "-"
            elif key in "0123456789" and len(key) == 1:
                typed_answer += key
            elif key == "return" and typed_answer not in ("", "-"):
                break
        else:
            continue

        break

# ----- Exporting saved data to csv -----
write_header = not data_file.exists() or data_file.stat().st_size == 0
with data_file.open("a", newline="", encoding="utf-8") as file:
    writer = csv.DictWriter(
        file,
        fieldnames=list(participant_row.keys())
    )
    if write_header:
        writer.writeheader()
    writer.writerow(participant_row)

# ----- Experiment end -----
win.close()
core.quit()