# Implement bubble sort
def bubble_sort():
    numbers = list(map(int, input("Enter numbers separated by space: ").split()))
    n = len(numbers)
    for i in range(n):
        for j in range(0, n-i-1):
            if numbers[j] > numbers[j+1]:
                numbers[j], numbers[j+1] = numbers[j+1], numbers[j]
    print("Sorted numbers:", numbers)

if __name__ == "__main__":
    bubble_sort()
