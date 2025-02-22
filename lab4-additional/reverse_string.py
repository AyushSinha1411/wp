# Class to reverse a string word by word
class StringReverser:
    def __init__(self, string):
        self.string = string

    def reverse_words(self):
        words = self.string.split()
        return ' '.join(reversed(words))

if __name__ == "__main__":
    input_string = input("Enter a string: ")
    reverser = StringReverser(input_string)
    print("Reversed string:", reverser.reverse_words())
