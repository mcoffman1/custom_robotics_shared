# to import the functions
import class_fun_ex as cfe
# to import the class
from class_fun_ex import Greeter


try:
    # the only change is we have to tell it where the function lives
    name = cfe.ask_for_name()
    greeter = Greeter(name)
    greeter.greet()
except KeyboardInterrupt:
    print("\nProgram interrupted by user. Exiting gracefully.")
except Exception as e:
    print(f"An unexpected error occurred: {e}")