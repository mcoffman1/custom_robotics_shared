import keyboard

def on_key_event(event):
    if event.name == 'up':
        print('Up arrow key pressed')
    elif event.name == 'down':
        print('Down arrow key pressed')
    elif event.name == 'left':
        print('Left arrow key pressed')
    elif event.name == 'right':
        print('Right arrow key pressed')

keyboard.on_press(on_key_event)

print("Press arrow keys or Ctrl+C to stop.")
keyboard.wait('esc')  # Use the escape key to exit the program
