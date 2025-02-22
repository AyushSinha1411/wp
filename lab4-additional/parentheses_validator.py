# Class to find validity of a string of parentheses
class ParenthesesValidator:
    def __init__(self, string):
        self.string = string

    def is_valid(self):
        stack = []
        mapping = {')': '(', '}': '{', ']': '['}
        for char in self.string:
            if char in mapping:
                top_element = stack.pop() if stack else '#'
                if mapping[char] != top_element:
                    return False
            else:
                stack.append(char)
        return not stack

if __name__ == "__main__":
    input_string = input("Enter a string of parentheses: ")
    validator = ParenthesesValidator(input_string)
    if validator.is_valid():
        print("The string of parentheses is valid.")
    else:
        print("The string of parentheses is invalid.")
