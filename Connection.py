import threading
from turtle import Canvas
from tkinter import *
import serial

# The desired port may be different, can be seen by going to
# Devices->Ports and selecting the port connected to the UART
BAUD_RATE = 9600
COM_PORT = 'COM4'
INITIAL_STATE = '0'

# Prepares and stars the GUI for the user
def start():
    window = Tk()
    window.title("SYSC 3310 Final Project: State toggling")
    window.geometry('325x150')

    # Creates the buttons
    backwards = Button(window, text="Move Backwards", command=lambda: sendCommand('1'))
    forwards = Button(window, text="Move Forwards", command=lambda: sendCommand('2'))
    reset = Button(window, text="Reset Board", command=lambda: sendCommand('0'))

    backwards.grid(column=0, row=0, padx=5, pady=2)
    forwards.grid(column=1, row=0, padx=5, pady=2)
    reset.grid(column=2, row=0, padx=5, pady=2)

    # Creates the boxes to display the current state
    global lbl
    lbl = Label(window, text="Just initialized")
    currState = Label(window, text="Current State: ")

    lbl.grid(column=1, row=1)
    currState.grid(column=0, row=1)

    # Creates the canvas, rectangle used for the UI display
    global canvas
    canvas = Canvas(window)
    canvas = Canvas(width=75, height=100)
    canvas.grid(column=0, row=4)

    global rectangle1
    global rectangle2
    rectangle1 = canvas.create_rectangle(5, 25, 25, 45, fill='black')
    rectangle2 = canvas.create_rectangle(30, 25, 50, 45, fill='black')

    canvas.create_text(15, 10, fill="black", font="Times 8 bold", text="P1.0")
    canvas.create_text(40, 10, fill="black", font="Times 8 bold", text="P2.0")

    # Sets up the receive thread
    receiveThread = threading.Thread(target=receiveState)
    receiveThread.daemon = True
    receiveThread.start()

    # Returns the board to its base state (state 1)
    # Optional
    sendCommand(INITIAL_STATE)

    window.mainloop()

# Runs a forever loop and updates the display when
# information has been received
def receiveState():
    while True:
        out = ser.read().decode()
        if out:
            lbl.configure(text=out)
            updateDisplay(out)

# Sends a command, called in the lambda of the buttons
def sendCommand(message):
    ser.write(message.encode())

# Updates the rectangle display based on the current state
def updateDisplay(state):
    if state == '1':
        canvas.itemconfig(rectangle1, fill='black')
        canvas.itemconfig(rectangle2, fill='black')
    if state == '2':
        canvas.itemconfig(rectangle1, fill='red')
        canvas.itemconfig(rectangle2, fill='black')
    elif state == '3':
        canvas.itemconfig(rectangle1, fill='black')
        canvas.itemconfig(rectangle2, fill='red')
    elif state == '4':
        canvas.itemconfig(rectangle1, fill='red')
        canvas.itemconfig(rectangle2, fill='red')


if __name__ == '__main__':
    comPort = input("Which port is the device connected to (ex. COM3, COM4, etc)\n"
                    "You can view the various ports in use by following the part Start->Device Manager->Ports\n"
                    "Input the port name here, will default to %s: " % COM_PORT).upper()

    if isinstance(comPort, str) != "":
        print("Using user-provided port (%s), window will open if successful: " % comPort)
        ser = serial.Serial(port=comPort)
    else:
        print("Invalid input, using default port (COM4), window will open if successful: ")
        ser = serial.Serial(port=COM_PORT)
    ser.isOpen()
    start()
