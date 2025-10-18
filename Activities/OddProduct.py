#Variables
seq_nums = []
user_input = ''
product = 0
odd_product = False

user_input = input("Enter desired numbers separated by a space.\n") #User input
seq_nums = list(map(int, user_input.split())) #Split() and parse user input from string to int and assign them a position in the list using map()

for i in range(len(seq_nums)): #Inital for loop to grab first number
    for j in range(i + 1, len(seq_nums)): #For loop to grab second number
        a = seq_nums[i]
        b = seq_nums[j]
        if a == b: #Check for unique pair of numbers
            continue #If pair is not unique, continue to next step
        product = a * b
        if product % 2 == 1: #Check if product is odd
            print(f"Odd product found: {a} * {b} = {product}\n")
            odd_product = True #Set odd_product to true if a distinct pair of numbers results in an odd product
if not odd_product: #If odd_product is still false, print to the user that no distinct pair is odd or all products are even
    print("No distinct pair of numbers results in odd product or all products are even.\n")