# Find a pair of elements whose sum equals a specific target number
class PairFinder:
    def __init__(self, numbers):
        self.numbers = numbers

    def find_pair(self, target):
        num_map = {}
        for index, number in enumerate(self.numbers):
            complement = target - number
            if complement in num_map:
                return num_map[complement], index
            num_map[number] = index
        return None

if __name__ == "__main__":
    numbers = list(map(int, input("Enter numbers separated by space: ").split()))
    target = int(input("Enter the target sum: "))
    finder = PairFinder(numbers)
    result = finder.find_pair(target)
    if result:
        print(f"Pair found at indices(0 based indexing ): {result[0]}, {result[1]}")
    else:
        print("No pair found.")
