# UART-Connection

This repository serves as the source of the GUI for the embedded state machine repository on my github, featured here: https://github.com/jonahgaudet/Embedded-State-Machine

Commands are send over a UART Connection, and cna give 3 instructions:<br>
0: reset to default state (determined by device)<br>
1: go back one state<br>
2: go forward one state

Libraries that will need to be imported are tkinter, turtle, threading and serial (can be done using pip install).

The GUI features a small visual elements, buttons to send commands, and labels that reflect the current state. It is created using tkinter for the GUI and turtle for the visual element.

Threading is also required to allow the program to both transmit and receive commands
