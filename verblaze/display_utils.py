# display_utils.py

import os
import sys
import time

def colored_custom(text, r, g, b):
    """
    Returns text colored with the specified RGB values.
    """
    return f"\033[38;2;{r};{g};{b}m{text}\033[0m"

def print_ascii_art():
    """
    Prints the ASCII art logo of Verblaze.
    """
    os.system('clear')
    ascii_art = [
        "                    _      _                        ___   __   _____ ",
        " /\\   /\\ ___  _ __ | |__  | |  __ _  ____ ___      / __\\ / /   \\_   \\",
        " \\ \\ / // _ \\| '__|| '_ \\ | | / _` ||_  // _ \\    / /   / /     / /\\/ ",
        "  \\ V /|  __/| |   | |_) || || (_| | / /|  __/   / /___/ /___/\\/ /_  ",
        "   \\_/  \\___||_|   |_.__/ |_| \\__,_|/___|\\___|   \\____/\\____/\\____/  ",
        "                                                                     "
    ]
    for line in ascii_art:
        print(colored_custom(line, 79, 70, 229))

def loading_animation():
    """
    Displays a simple loading animation in the console.
    """
    loading = "Strings are being extracted: [----------]"
    for i in range(10):
        progress = loading[:29] + "=" * i + "-" * (10 - i) + "]"
        sys.stdout.write('\r' + progress)
        sys.stdout.flush()
        time.sleep(0.5)
    sys.stdout.write('\n')