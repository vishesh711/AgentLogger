def divide_numbers(a, b):
    # Fixed: Added check for division by zero
    if b == 0:
        raise ValueError("Cannot divide by zero")
    return a / b

def main():
    # This will now handle the division by zero case
    try:
        result = divide_numbers(10, 0)
        print(f"Result: {result}")
    except ValueError as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main() 