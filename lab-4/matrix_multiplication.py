# Multiply two matrices
def multiply_matrices():
    rows_a = int(input("Enter the number of rows for the first matrix: "))
    cols_a = int(input("Enter the number of columns for the first matrix: "))
    print("Enter the elements of the first matrix:")
    matrix_a = [list(map(int, input().split())) for _ in range(rows_a)]

    rows_b = int(input("Enter the number of rows for the second matrix: "))
    cols_b = int(input("Enter the number of columns for the second matrix: "))
    print("Enter the elements of the second matrix:")
    matrix_b = [list(map(int, input().split())) for _ in range(rows_b)]

    if cols_a != rows_b:
        print("Matrix multiplication is not possible.")
        return

    result = [[0 for _ in range(cols_b)] for _ in range(rows_a)]
    for i in range(rows_a):
        for j in range(cols_b):
            for k in range(cols_a):
                result[i][j] += matrix_a[i][k] * matrix_b[k][j]

    print("Resultant matrix:")
    for row in result:
        print(" ".join(map(str, row)))

if __name__ == "__main__":
    multiply_matrices()
