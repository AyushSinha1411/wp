# Assignment Solutions

# 1. Reverse the content of a file and store it in another file
def reverse_file_content(input_file, output_file):
    with open(input_file, 'r') as file:
        content = file.read()
    with open(output_file, 'w') as file:
        file.write(content[::-1])

# 2. Implement binary search with recursion
def binary_search(arr, target, low, high):
    if low > high:
        return -1
    mid = (low + high) // 2
    if arr[mid] == target:
        return mid
    elif arr[mid] < target:
        return binary_search(arr, target, mid + 1, high)
    else:
        return binary_search(arr, target, low, mid - 1)

# 3. Sort words in alphabetical order
def sort_words(words):
    return sorted(words)

# 4. Get all possible unique subsets from a set of distinct integers
class UniqueSubsets:
    def __init__(self, nums):
        self.nums = nums

    def get_subsets(self):
        result = []
        self._backtrack([], 0, result)
        return result

    def _backtrack(self, current, index, result):
        result.append(current[:])
        for i in range(index, len(self.nums)):
            current.append(self.nums[i])
            self._backtrack(current, i + 1, result)
            current.pop()

# 5. Find a pair of elements whose sum equals a specific target number
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

# 6. Implement pow(x, n)
class Power:
    def pow(self, x, n):
        if n < 0:
            return 1 / self.pow(x, -n)
        if n == 0:
            return 1
        return x * self.pow(x, n - 1)

# 7. Class with methods to get and print a string in uppercase
class StringManipulator:
    def __init__(self):
        self.string = ""

    def get_string(self):
        self.string = input("Enter a string: ")

    def print_string(self):
        print(self.string.upper())
