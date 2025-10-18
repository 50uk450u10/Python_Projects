num1 = 0
num2 = 0
product = 0
sum = 0

num1 = int(input("Enter the first integer: \n"))
num2 = int(input("Enter the second integer: \n"))

product = num1 * num2

if product <= 1000:
    print(f"The product of {num1} and {num2} is {product}\n")
else:
    sum = num1 + num2
    print(f"Product greater than 1000, sum of {num1} and {num2} is {sum}\n")