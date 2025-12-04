
# class example

class Greeter:
    def __init__(self, name):
        self.name = name

    # method example
    def greet(self):
        print(f"Hello, {self.name}! Welcome to the Python demo.")

# function example
def ask_for_name():
    return input("Enter your name: ")

# Main logic with exception handling works the same if you import
if __name__ == "__main__":
    try:
        name = ask_for_name()
        greeter = Greeter(name)
        greeter.greet()
    except KeyboardInterrupt:
        print("\nProgram interrupted by user. Exiting gracefully.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
