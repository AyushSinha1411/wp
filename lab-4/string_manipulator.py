# Class with methods to get and print a string in uppercase
class StringManipulator:
    def __init__(self):
        self.string = ""

    def get_string(self):
        self.string = input("Enter a string: ")

    def print_string(self):
        print(self.string.upper())

if __name__ == "__main__":
    manipulator = StringManipulator()
    manipulator.get_string()
    manipulator.print_string()
