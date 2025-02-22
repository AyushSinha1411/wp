# Select the smallest element from a list in linear time
def find_smallest_element():
    numbers = list(map(int, input("Enter numbers separated by space: ").split()))
    smallest = min(numbers)  # Using built-in min function for linear time complexity
    print("The smallest element is:", smallest)

if __name__ == "__main__":
    find_smallest_element()
