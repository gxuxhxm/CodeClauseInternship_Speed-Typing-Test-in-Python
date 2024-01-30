import string
import random
import time
from tkinter import Tk, Label, Text, Button
from tkinter import font

BG = "#222831"
FG = "#00ADB5"
FG2 = "#AA96DA"
ERROR_RESULT_COLOR = "#EEEEEE"

FONT_FAMILY1 = 'Calibri'
FONT_FAMILY2 = 'Bebas Neue'  # Change to your preferred urban font
FONT_SIZE1 = 14
FONT_SIZE2 = 18
FONT_SIZE3 = 24
FONT_STYLE1 = 'normal'
FONT_STYLE2 = 'italic'

PARA_FONT = (FONT_FAMILY1, FONT_SIZE1, FONT_STYLE1)
PARA_FONT2 = (FONT_FAMILY1, 12, FONT_STYLE2)
HEAD_FONT = (FONT_FAMILY2, FONT_SIZE3, FONT_STYLE1)  # Using urban font for the heading
HEAD2_FONT = (FONT_FAMILY2, FONT_SIZE2, FONT_STYLE1)  # Using urban font for the second heading

class TypingSpeedApp:
    def __init__(self):
        self.window = Tk()
        self.window.title('Welcome to Typing Speed Calculator!')
        self.window.config(bg=BG, pady=10, padx=50)

        self.sentences = [line.strip() for line in open('sentences.txt', 'r')]

        self.prev_line = ""
        self.user_line = ""
        self.end_of_typing = False
        self.starting_time = 0
        self.beginning_time = 0
        self.all_speeds = []
        self.reset_timer = None

        self.create_ui()

    def create_ui(self):
        heading_text = "GET YOUR TYPING SPEED TESTED"
        instructions_text = "1. The test starts the moment you enter your first letter.\n" \
                            "2. You can have a pause of only 5 seconds at max."

        self.heading = Label(text=heading_text, font=HEAD_FONT, bg=BG, fg=FG, padx=10, pady=10)
        self.sentence = Label(text=self.assign_a_line(), font=HEAD2_FONT, bg=BG, fg=FG2, pady=10, padx=10, wraplength=800)
        self.instruction = Label(text=instructions_text, font=PARA_FONT2, fg=FG, bg=BG)
        self.typing_area = Text(font=PARA_FONT, bg=BG, fg=FG, width=80, height=10, wrap='w',
                                highlightcolor=FG, highlightthickness=4, highlightbackground=FG,
                                padx=5, pady=5)
        self.typing_area.bind('<KeyPress>', self.start_calculating)

        self.reset_button = Button(text='Reset Application', fg=FG, bg=BG, font=PARA_FONT,
                                   highlightbackground=FG, highlightcolor=FG, highlightthickness=0, border=3,
                                   command=self.reset_app)
        self.overall_button = Button(text='Show Average Speed', fg=FG, bg=BG, font=PARA_FONT,
                                     highlightbackground=FG, highlightcolor=FG, highlightthickness=0, border=3,
                                     command=self.show_overall_speed)

        self.place_ui_components()

    def place_ui_components(self):
        self.heading.grid(row=0, column=0, columnspan=2)
        self.sentence.grid(row=1, column=0, columnspan=2)
        self.instruction.grid(row=2, column=0, columnspan=2)
        self.typing_area.grid(row=3, column=0, columnspan=2)
        self.reset_button.grid(row=4, column=0, sticky='ew')
        self.overall_button.grid(row=4, column=1, sticky='ew')

        self.window.mainloop()

    def assign_a_line(self):
        line = random.choice(self.sentences)
        while line == self.prev_line:
            line = random.choice(self.sentences)
        self.prev_line = line
        return line

    def start_calculating(self, event):
        if self.end_of_typing:
            print('Cannot Type Further')
            return

        if self.starting_time == 0:
            self.starting_time = time.time()

        if self.beginning_time == 0:
            self.beginning_time = time.time()

        if event.keysym == "BackSpace":
            self.user_line = self.user_line[:-1]
            self.starting_time = time.time()
            return
        else:
            self.user_line += event.char
            end_time = time.time()
            gap = end_time - self.starting_time

            if gap > 5:
                ending_msg = 'You took too long. End of typing period. Click on Reset button to start again'
                self.show_result(False, 0)
                self.end_of_typing = True
                self.display_result_message(ending_msg, ERROR_RESULT_COLOR)
                return

            text_len = len(self.user_line)
            if text_len == len(self.sentence.cget("text")):
                self.end_of_typing = True
                is_accu = self.check_accuracy(self.user_line, self.sentence.cget("text"))
                seconds_elapsed = end_time - self.beginning_time
                chars_per_second = round(text_len / seconds_elapsed)
                words_per_minute = chars_per_second * (60 / 5)
                self.show_result(is_accu, words_per_minute)
                self.all_speeds.append(words_per_minute)
                self.reset_timer = self.window.after(2000, self.reset_app)

        self.starting_time = time.time()

    def check_accuracy(self, user_line_, app_line):
        return user_line_ == app_line

    def show_result(self, boolean, wpm):
        color = 'green' if boolean else 'red'
        self.typing_area.config(highlightcolor=color, highlightbackground=color)
        error_status = "WITHOUT ERRORS" if boolean else "WITH ERRORS"
        self.sentence.config(text=f" Speed: {wpm} wpm {error_status}", fg=color)

    def reset_app(self):
        if self.reset_timer:
            self.window.after_cancel(self.reset_timer)

        self.starting_time = 0
        self.beginning_time = 0
        self.reset_timer = None
        self.end_of_typing = False
        self.user_line = ""
        self.prev_line = ""
        self.sentence.config(text=self.assign_a_line(), fg=FG2)
        self.typing_area.delete('1.0', 'end')
        self.typing_area.config(highlightcolor=FG, highlightbackground=FG)

    def show_overall_speed(self):
        if self.reset_timer:
            self.window.after_cancel(self.reset_timer)

        if self.all_speeds:
            avg_speed = sum(self.all_speeds) / len(self.all_speeds)
            self.sentence.config(text=f"{int(avg_speed)} wpm", fg=ERROR_RESULT_COLOR)
        else:
            self.sentence.config(text="Nothing to Show yet", fg=ERROR_RESULT_COLOR)

if __name__ == "__main__":
    TypingSpeedApp()
