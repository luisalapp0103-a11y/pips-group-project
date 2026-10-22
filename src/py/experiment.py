#Misinformation effect experiment

from psychopy import visual, core, event, gui
from pathlib import Path
from datetime import datetime
import random
import pandas as pd



# ===========================
# ----- General setting -----
# ===========================

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

try:
    participant_id = int(participant_info["Participant_id"])
except ValueError:
    error_dialog = gui.Dlg(title="Invalid participant ID")
    error_dialog.addText("Participant ID must be a whole number.")
    error_dialog.show()
    core.quit()

# creating data csv file & temporary data storage
data_file = data_folder / f"Subject {participant_info['Participant_id']}.csv"

if data_file.exists():
    error_dialog = gui.Dlg(title="Participant file already exists")
    error_dialog.addText(
        f"A file already exists for this participant:\n{data_file}\n\n"
        "Check the participant ID before restarting."
    )
    error_dialog.show()
    core.quit()

data_record = pd.DataFrame([{
    "participant_id": participant_info["Participant_id"],
    "age": participant_info["Age"],
    "gender": participant_info["Gender"],
    "timestamp": datetime.now().isoformat(timespec="seconds")
}])

# main window
win = visual.Window(
    size = (800, 600),
    fullscr = True,
    color = "gray",
    units = "height"
)

# conditions
if int(participant_info["Participant_id"]) % 2 == 0:
    data_record["condition"] = "control"
elif int(participant_info["Participant_id"]) % 2 == 1:
    data_record["condition"] = "misinformation"





# ================================
# ----- Experiment materials -----
# ================================

welcome_text = (
    "Welcome to the misinformation effect experiment!\n\n"
    "This is a study about memory for everyday events.\nIt takes about 15 min.\nYour participation will be anonymous.\n\n"
    "Please indicate you consent to join the experiment."
)

instruction_text = ("You will now read a short story, one sentence at a time.\nPlease pay attention.")

stories = [
    "It is a rainy Tuesday morning at Cafe Linde, a small cafe on a busy street.",
    "A young woman in a red scarf sits at a table by the window, working on her laptop with a cup of tea.",
    "Next to her laptop lie her phone and a black leather wallet.",
    "A tall man in a green jacket comes in and orders a coffee at the counter.",
    "The barista, an older man with glasses, tells him the price: 3 euros 50.",
    "The man pays with coins and sits down at the table next to the woman.",
    "The woman gets up to go to the toilet and leaves her things on the table.",
    "The man looks around, then slips the woman's wallet into his jacket pocket.",
    "He leaves his coffee untouched, walks out of the cafe and turns left.",
    "A few minutes later, the woman comes back and sees that her wallet is gone.",
    "She tells the barista, who calls the police.",
    "Two police officers arrive and write down the woman's description of the man."
]

attention_check_question = "What was the name of the cafe?"
option_text = ["Cafe Roma", "Cafe Linde", "Cafe Central", "Cafe Noord"]
option_position = [(0, 0.20), (0, 0.05), (0, -0.10), (0, -0.25)]

filler_instruction = "Please complete the following arithmetic problems.\nType your answers and press enter to proceed to the next question."

eye_witness_instruction = "Another customer who was in the cafe wrote down what happened.\nPlease read their account carefully."

control_text = "I was sitting in the corner of Cafe Linde that Tuesday morning, reading the newspaper. A young woman by the window was working on her laptop and having a drink. Next to her laptop were her phone and a leather wallet. Then a tall man in a jacket came in and ordered a coffee from the barista, an older man. The man paid and sat down right next to the woman. When she went to the toilet, he looked around and took her wallet. He walked out without touching his coffee and left. When the woman came back and saw that her wallet was missing, she was very upset. The barista called the police, and two officers arrived soon after to take her statement."
misinformation_text = "I was sitting in the corner of Cafe Linde that sunny Tuesday morning, reading the newspaper. A young woman by the window was working on her laptop and drinking a cappuccino. Next to her laptop were her phone and a brown leather wallet. Then a tall man in a blue jacket came in and ordered a coffee from the barista, an older man with a grey beard. The man paid by card and sat down right next to the woman. When she went to the toilet, he looked around and slipped her wallet into his backpack. He walked out without touching his coffee and turned right at the door. When the woman came back and saw that her wallet was missing, she was very upset. The barista called the police, and two officers arrived soon after to take her statement."

memory_test_instruction = "You will now see 24 statements about the story you read at the start, one at a time. They will appear below in blue. For each statement, indicate how sure you are that it is true or false for the story (not the account).\nAnswer with the keys 1 to 6. There are no time limits, but please answer with your first impression."
scale_labels = [
    "Certain\nfalse",
    "Probably\nfalse",
    "Maybe\nfalse",
    "Maybe\ntrue",
    "Probably\ntrue",
    "Certain\ntrue"
]

memory_test_items = pd.read_csv(project_folder / "src" / "py" / "memory_test_items.csv")

debrief_text = "Thank you for your partcipation!"
# Need revising





# =================================
# ----- Experiment parameters -----
# =================================
story_time = 8
filler1_time = 300
filler2_time = 180





#======================
# ----- Functions -----
#======================

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

# creating text stimuli
def text_display(pos, text = "", win = win, color = "white"):
    screen = visual.TextStim(
        win = win,
        text = text,
        color = color,
        height = 0.04,
        pos = pos
    )
    return screen

# data saving checkpoint
def save_checkpoint():
    data_record.to_csv(
        data_file,
        mode="w",
        header=True,
        index=False,
        encoding="utf-8",
        )

# end experiment with escape 
def esc_quit():
    save_checkpoint()
    if event.getKeys(keyList=["escape"]):
        win.close()
        core.quit()




# ----- Experiment begins -----
#===========================
# ----- Welcome screen -----
#===========================

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



#===============================
# ----- Instruction screen -----
#===============================

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



# ========================
# ----- Story reading-----
# ========================

# set timer and text screen
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



# ===========================
# ----- Attention check -----
# ===========================

# create multiple choice screen
attention_check = text_display((0, 0.35), attention_check_question)
option_buttons = [create_button(pos, text) for pos, text in zip(option_position, option_text)]

# get chosen option from participants
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
data_record["attention_correct"] = selected == 1
save_checkpoint()



# ========================
# ----- Filler Task1 -----
# ========================

# create filler task screen
filler_instruction_screen = text_display((0, 0.15), filler_instruction)
arithmetic_question = text_display((0, 0))
answer_text = text_display((0, -0.15))

# countdown timer
timer = text_display((win.size[0] / win.size[1]/2 - 0.15, 0.35), color = "blue")
countdown = core.CountdownTimer(filler1_time)

# task procedure
count = 0
correct_count = 0
while countdown.getTime() >= 0:
    # create question
    number_A, number_B = random.randint(10, 99), random.randint(10, 99)
    correct_sum = number_A + number_B
    arithmetic_question.text = f"{number_A} + {number_B}= ?"
    
    #collect answer
    typed_answer = ""
    event.clearEvents(eventType="keyboard")
    
    while countdown.getTime() >= 0:
        # update timer
        remaining_seconds = max(0, int(countdown.getTime() + 0.999))
        minutes, seconds = divmod(remaining_seconds, 60)
        timer.text = f"Time left\n{minutes:02d}:{seconds:02d}"
                
        # diplay all elements
        filler_instruction_screen.draw()
        arithmetic_question.draw()
        answer_text.text = f"Your answer: {typed_answer}"
        answer_text.draw()
        timer.draw()
        win.flip()

        # get typed answers
        keys = event.getKeys()
        for key in keys:
            if key == "escape":
                win.close()
                core.quit()
            elif key == "backspace":
                typed_answer = typed_answer[:-1]
            elif key in "0123456789" and len(key) == 1:
                typed_answer += key
            elif key == "return" and typed_answer != "":
                break
        else:
            continue

        # calculate answered and correct questions
        if countdown.getTime() <= 0:
            break
        ans = int(typed_answer)
        count += 1
        if ans == correct_sum:
            correct_count += 1
        break

# record filler task 1 data
data_record["filler1_answered"] = count
data_record["filler1_correct"] = correct_count
save_checkpoint()



# =========================================================
# ----- Eye witness account verification instructions -----
# =========================================================

# create verification instruction screen
eye_witness_screen = text_display((0, 0), eye_witness_instruction)
continue_button, continue_label = create_button((0, -0.25), "Continue")

# click goes to next screen
mouse = event.Mouse(win=win)
mouse.setVisible(True)
while True:
    esc_quit()
    eye_witness_screen.draw()
    continue_button.draw()
    continue_label.draw()
    win.flip()
    if mouse.isPressedIn(continue_button, buttons = [0]):
        break



# ============================================
# ----- Eye witness account verification -----
# ============================================

# set timer and create verification task screen
reading_time = core.Clock()
control_screen = text_display((0, 0), control_text)
misinformation_screen = text_display((0, 0), misinformation_text)
continue_button, continue_label = create_button((win.size[0] / win.size[1]/2 - 0.15, -0.40), "Continue")
mouse = event.Mouse(win=win)
mouse.setVisible(True)

# Start timing when the first frame appears
win.callOnFlip(reading_time.reset)

while True:
    esc_quit()

    # display based on condition
    if data_record.loc[0, "condition"] == "control":
        control_screen.draw()
    elif data_record.loc[0, "condition"] == "misinformation":
        misinformation_screen.draw()
    else:
        raise ValueError("Unknown experiment condition")

    # show continue button after 60s
    if reading_time.getTime() >= 60:
        continue_button.draw()
        continue_label.draw()
    win.flip()

    # go to next screen after clicking continue
    if reading_time.getTime() >= 60 and mouse.isPressedIn(continue_button, buttons = [0]):
        break



# ========================
# ----- Filler Task2 -----
# ========================

# create filler task screen
filler_instruction_screen = text_display((0, 0.15), filler_instruction)
arithmetic_question = text_display((0, 0))
answer_text = text_display((0, -0.15))

# countdown timer
timer = text_display((win.size[0] / win.size[1]/2 - 0.15, 0.35), color = "blue")
countdown = core.CountdownTimer(filler2_time)

# task procedure
count = 0
correct_count = 0
while countdown.getTime() >= 0:
    # create question
    number_A, number_B = random.randint(10, 99), random.randint(10, 99)
    correct_sum = number_A + number_B
    arithmetic_question.text = f"{number_A} + {number_B}= ?"
    
    #collect answer
    typed_answer = ""
    event.clearEvents(eventType="keyboard")
    
    while countdown.getTime() >= 0:
        # update timer
        remaining_seconds = max(0, int(countdown.getTime() + 0.999))
        minutes, seconds = divmod(remaining_seconds, 60)
        timer.text = f"Time left\n{minutes:02d}:{seconds:02d}"
                
        # diplay all elements
        filler_instruction_screen.draw()
        arithmetic_question.draw()
        answer_text.text = f"Your answer: {typed_answer}"
        answer_text.draw()
        timer.draw()
        win.flip()

        # get typed answers
        keys = event.getKeys()

        for key in keys:
            if key == "escape":
                win.close()
                core.quit()
            elif key == "backspace":
                typed_answer = typed_answer[:-1]
            elif key in "0123456789" and len(key) == 1:
                typed_answer += key
            elif key == "return" and typed_answer != "":
                break
        else:
            continue

        # calculate answered and correct questions
        if countdown.getTime() <= 0:
            break
        ans = int(typed_answer)
        count += 1
        if ans == correct_sum:
            correct_count += 1
        break

# record filler task 2 data
data_record["filler2_answered"] = count
data_record["filler2_correct"] = correct_count
save_checkpoint()
core.wait(0.5)



# =======================
# ----- Memory test -----
# =======================

# create rating scale
scale = visual.Slider(
    win=win,
    ticks = [1, 2, 3, 4, 5, 6],
    labels = scale_labels,
    granularity = 1,
    style = "rating",
    pos = (0, -0.30),
    size = (0.8, 0.08),
    units = "height",
    labelHeight = 0.025
)

# memory test insructions
mem_test_instruction = text_display((0, 0.20), memory_test_instruction)

# randomize questions and collect answers
trial = 0
shuffled_items = memory_test_items.sample(frac=1).reset_index(drop=True)

for row_index, item in shuffled_items.iterrows():
    # record statement item information
    data_record.loc[row_index, "trial"] = row_index + 1
    data_record.loc[row_index, "item_id"] = item["item_id"]
    data_record.loc[row_index, "item_type"] = item["item_type"]
    data_record.loc[row_index, "detail"] = item["detail"]
    data_record.loc[row_index, "statement"] = item["Statement"]
    data_record.loc[row_index, "correct_answer"] = item["Correct answer"]

    # show stimuli for each trial
    scale.reset()
    mem_test = text_display((0, -0.1), item["Statement"], color = "blue")
    response_clock = core.Clock()

    event.clearEvents(eventType="keyboard")

    mem_test_instruction.draw()
    mem_test.draw()
    scale.draw()
    win.callOnFlip(response_clock.reset)
    win.flip()

    # get keyboard response
    while True:
        esc_quit()
        keys = event.getKeys(
            keyList = ["1", "2", "3", "4", "5", "6"],
            timeStamped = response_clock
        )

        if keys:
            key, response_time = keys[0]
            rating = int(key)
            reaction_time_ms = response_time * 1000
            break

        core.wait(0.001)

    # Save the response in this trial's row
    data_record.loc[row_index, "response"] = rating
    data_record.loc[row_index, "rt_ms"] = reaction_time_ms
    save_checkpoint()



# ========================
# ----- Debrief page -----
# ========================

debrief = text_display((0, 0), debrief_text)
finish_button, finish_label = create_button((0, -0.35), "Finish")
debrief.draw()
finish_button.draw()
finish_label.draw()
win.flip()

mouse = event.Mouse(win=win)
mouse.setVisible(True)
while True:
    esc_quit()
    if mouse.isPressedIn(finish_button, buttons = [0]):
        break
    core.wait(0.01)

blank_screen = text_display((0, 0))
blank_screen.draw()
win.flip()





# ==========================
# ----- Experiment end -----
# ==========================
save_checkpoint()
win.close()
core.quit()