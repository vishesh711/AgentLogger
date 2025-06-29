def divide_numbers(a, b):
    # Bug: No check for division by zero
    return a / b

def main():
    # This will cause a ZeroDivisionError
    result = divide_numbers(10, 0)
    print(f"Result: {result}")

if __name__ == "__main__":
    main() 