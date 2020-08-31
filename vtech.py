import RPi.GPIO as GPIO
import time
import uinput
import keyboard
import threading

GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)


# The original matrix layout - map to know which key is which
# ['ENTER', 'n', 'm', 'ANSWER', 'HELP', 'PLAYER B', 'None'],
# ['Arrow', 'h', 'j', 'k', 'l', 'ERASE', 'None'],
# ['Arrow', 'y', 'u', 'i', 'o', 'p', 'None'],
# ['REPEAT', 'b', 'v', 'c', 'x', 'z', 'PLAYER A'],
# ['CHOOSE LEVEL', 'g', 'f', 'd', 's', 'a', 'PLAYER'],
# ['Arrow', 't', 'r', 'e', 'w', 'q', 'None'],
# ['OFF', '5', '4', '3', '2', '1', 'ACTIVITY'],
# ['Arrow', '6', '7', '8', '9', '0', 'None'] ]
# Set up value matrix
value_matrix = [ ['ENTER', 'n', 'm', 'space', 'HELP', 'PLAYER B', 'None'],
                 ['right', 'h', 'j', 'k', 'l', 'Backspace', 'None'],
                 ['left', 'y', 'u', 'i', 'o', 'p', 'None'],
                 ['REPEAT', 'b', 'v', 'c', 'x', 'z', 'ctrl'],
                 ['CHOOSE LEVEL', 'g', 'f', 'd', 's', 'a', 'shift'],
                 ['down', 't', 'r', 'e', 'w', 'q', 'None'],
                 ['OFF', '5', '4', '3', '2', '1', 'esc'],
                 ['up', '6', '7', '8', '9', '0', 'None'] ]

# Establish pins for rows and columns
rows = [3,5,7,8,10,11,12,13]
columns = [15,16,18,19,21,22,23]

# Setup gpio
for j in range(7):
    GPIO.setup(columns[j], GPIO.OUT)
    GPIO.output(columns[j], 1)
    
for i in range(8):
    GPIO.setup(rows[i], GPIO.IN, pull_up_down = GPIO.PUD_UP)
    
def press_key(key):
    # If user clicks ctrl, it will toggle the ctrl function: The user may click ctrl once,
    # then click any other letter and the case statement below will simulate the hot keys
    # ex. User click 'ctrl', then clicks 's' : simulate 'ctrl+s' hotkey press 
    if key == 'ctrl' or key == 'shift':
        keyboard.press(key)
    else:
        keyboard.press_and_release(key)
        keyboard.release('ctrl')
        keyboard.release('shift')

    
try:
    while True:
        for j in range(7):
            GPIO.output(columns[j], 0) # Set output pins LOW one at a time
            
            # Check for inputs
            for i in range(8):
                if GPIO.input(rows[i]) == 0:
                    time.sleep(.4)
                    print(value_matrix[i][j])

                    t1 = threading.Thread(target=press_key, args=(value_matrix[i][j],))
                    t1.start()
#                     while GPIO.input(rows[i]) == 0: # Disallows button holding
#                         pass
            
            
            GPIO.output(columns[j], 1) # Set output pins HIGH one at a time
            
        
except KeyboardInterrupt:
    GPIO.cleanup()
    
    


 
        
        
        