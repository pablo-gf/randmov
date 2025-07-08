# Loading feature

import sys
import time

def spinner(message, stop_spinner):
    while not stop_spinner.is_set():
        for char in "|/-\\":
            sys.stdout.write(f'\r{message} {char}')
            sys.stdout.flush()
            time.sleep(0.2)