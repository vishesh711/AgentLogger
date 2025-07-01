def divide_numbers(a, b):
    result = a / b  # This will crash with division by zero!
    return result

# Test the function
print(divide_numbers(10, 0))  # This will cause ZeroDivisionError

