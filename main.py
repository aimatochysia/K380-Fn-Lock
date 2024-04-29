import keyboard
import hid

# Constants for Logitech K380 keyboard
K380_SEQ_FKEYS_ON = bytes([0x10, 0xff, 0x0b, 0x1e, 0x00, 0x00, 0x00])
K380_SEQ_FKEYS_OFF = bytes([0x10, 0xff, 0x0b, 0x1e, 0x01, 0x00, 0x00])
K380_VID = 0x46d
K380_PID = 0xb342
SEQ_LEN = 7

bool_val = False
# Global variable to track the state of function keys
function_keys_enabled = False
# Function to control K380 keyboard based on Ctrl + Shift + Alt key combination

def control_keyboard(event):
    global function_keys_enabled
    global K380_SEQ_FKEYS_OFF
    global K380_SEQ_FKEYS_ON
    if function_keys_enabled:
        print("fn key off")
        toggle_function_keys(K380_SEQ_FKEYS_OFF)
    else:
        print("fn key on")
        toggle_function_keys(K380_SEQ_FKEYS_ON)
    function_keys_enabled = not function_keys_enabled

# Function to toggle function keys
def toggle_function_keys(seq):
    # Initialize the hidapi library
    global K380_VID
    global K380_PID
    global SEQ_LEN
    print("Init toggle")
    handle = None
    try:
        # Enumerate connected HID devices
        devs = hid.enumerate(K380_VID, K380_PID)
        for cur_dev in devs:
            if cur_dev.usage == 1 and cur_dev.usage_page == 65280:  # Check for K380 keyboard
                handle = hid.device()
                handle.open_path(cur_dev['path'])
                # Send the sequence to toggle function keys
                if handle.write(seq) != SEQ_LEN:
                    print("Error: Failed to toggle function keys")
                break
    except Exception as e:
        print("Exception:", e)
    finally:
        if handle:
            handle.close()

def test_toggle():
    global bool_val
    if bool_val == True:
        print("bool is True, changing to false")
        bool_val = False
    elif bool_val == False:
        print("bool is: False, changing to true")
        bool_val = True
    
# toggle_function_keys(K380_SEQ_FKEYS_ON)

# pyautogui.hotkey('ctrl', 'shift', 'alt', onPress=control_keyboard)
# keyboard.add_hotkey('ctrl', get_shift)

keyboard.add_hotkey('ctrl + shift + alt',test_toggle) 
keyboard.wait()
print("Done Running")
