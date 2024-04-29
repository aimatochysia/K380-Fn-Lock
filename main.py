import keyboard
import hid

# Constants for Logitech K380 keyboard
K380_SEQ_FKEYS_ON = bytes([0x10, 0xff, 0x0b, 0x1e, 0x00, 0x00, 0x00])
K380_SEQ_FKEYS_OFF = bytes([0x10, 0xff, 0x0b, 0x1e, 0x01, 0x00, 0x00])
K380_VID = 0x46d
K380_PID = 0xb342
SEQ_LEN = 7

# Global variable to track the state of function keys
function_keys_enabled = False

# Function to control K380 keyboard based on Ctrl + Shift + Alt key combination


def control_keyboard(event):
    global function_keys_enabled
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


keyboard.add_hotkey("ctrl+shift+alt", control_keyboard,
                    trigger_on_release=True)

keyboard.wait()  # Wait indefinitely without specifying any key
print("Done Running")
