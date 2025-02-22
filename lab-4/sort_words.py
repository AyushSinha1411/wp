# Sort words in alphabetical order
def sort_words():
    words = input("Enter words separated by space: ").split()
    sorted_words = sorted(words)
    print("Sorted words:", sorted_words)

if __name__ == "__main__":
    sort_words()
