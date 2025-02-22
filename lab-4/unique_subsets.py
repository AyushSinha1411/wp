# Get all possible unique subsets from a set of distinct integers
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

if __name__ == "__main__":
    nums = list(map(int, input("Enter distinct integers separated by space: ").split()))
    subsets = UniqueSubsets(nums)
    print("Unique subsets:", subsets.get_subsets())
