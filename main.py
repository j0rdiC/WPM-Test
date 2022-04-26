#!/bin/python3

import curses
from curses import wrapper
import time
import random

        # SCREEN: stdout(terminal) -> using wrapper
def start_screen(scr):
    # clear terminal
    scr.clear()
    # add text to the screen
    scr.addstr("Welcome to the Speed Typing Program")
    scr.addstr("\nPress any key to begin")
    scr.refresh()
    scr.getkey()

def display_text(scr, target, current, wpm=0):
    scr.addstr(target)
    scr.addstr(f"\nWPM: {wpm}")
    # overide target text w/ current text
    for index, letter in enumerate(current):
        correct_letter = target[index]
        color = curses.color_pair(1)
        if letter != correct_letter:
            color = curses.color_pair(2)

        scr.addstr(0, index, letter, color)

def load_text():
    with open("text.txt", "r") as f:
        lines = f.readlines() #returns list
        return random.choice(lines).strip()

def wpm_test(scr):
    target_text = load_text()
    current_text = []
    wpm = 0
    start_time = time.time()
    #scr.nodelay(True)

    while True:
                    # use max() to avoid 0 division error + add safety
        time_elapsed = max(time.time() - start_time, 1)
        wpm = round((len(current_text) / (time_elapsed/60)) / 5) # assuming avg word has 5 letters
        
        scr.clear()
        display_text(scr, target_text, current_text, wpm)
        scr.refresh()

        # check finish
        if "".join(current_text) == target_text:
            break

        # fix wpm decrease if not typing
        try:
            key = scr.getkey()
        except:
            continue # if no key, go to the start of the loop, ignore bottom

        # fix DELETE key (for all OS) + fix finish targed
        if key in ("KEY_BACKSPACE", '\b', '\x7f'):
            if len(current_text) > 0:
                current_text.pop()
        elif len(current_text) < len(target_text):
            current_text.append(key)

        # exit program (every key has a numeric ASCII or UNICODE repr (ordinal repr), in this case ESC is key 27)
        if key == '`':
           break


def main(scr):
    # overide text color
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_WHITE, curses.COLOR_BLACK)

    start_screen(scr)
    while True:
        wpm_test(scr)
        scr.addstr(2, 0, "Text complete! Press any key to continue...")
        key = scr.getkey()
        if key == '`':
           break

# call func inside func
wrapper(main)