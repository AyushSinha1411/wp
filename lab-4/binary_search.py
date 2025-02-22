# Implement binary search with recursion
def binary_search(arr, target):
    def search(low, high):
        if low > high:
            return -1
        mid = (low + high) // 2
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            return search(mid + 1, high)
        else:
            return search(low, mid - 1)

    return search(0, len(arr) - 1)

if __name__ == "__main__":
    numbers = list(map(int, input("Enter sorted numbers separated by space: ").split()))
    target = int(input("Enter the target number: "))
    result = binary_search(numbers, target)
    if result != -1:
        print(f"Target found at index: {result}")
    else:
        print("Target not found.")
