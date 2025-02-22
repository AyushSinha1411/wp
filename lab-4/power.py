# Implement pow(x, n)
class Power:
    def pow(self, x, n):
        if n < 0:
            return 1 / self.pow(x, -n)
        if n == 0:
            return 1
        return x * self.pow(x, n - 1)

if __name__ == "__main__":
    x = float(input("Enter the base (x): "))
    n = int(input("Enter the exponent (n): "))
    power_calculator = Power()
    result = power_calculator.pow(x, n)
    print(f"{x} raised to the power of {n} is: {result}")
