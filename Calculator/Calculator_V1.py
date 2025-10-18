import sys

#Variables
num1 = 0
num2 = 0
select = 0

#Welcome message
print("Welcome to your calculator!\nPlease select from the following menu with the corresponding number:")

#Enter while loop
while(select != 5):

    #try/catch statements to account for non-numeric inputs
    try:
        #Variable "select" will only accept integer input
        select = int(input("1. Addition\n2. Subtraction\n3. Multiplication\n4. Division\n5. Exit\n"))
    except ValueError: #If an input is non-numeric, ValueError exception will throw
        print("Error: Please enter numbers only.\n") #Notify user of the error
        continue #Return to beginning of loop

    try:
        #if statement logic for inputs on select
        if select == 1:
            try:
                num1 = float(input("Please enter the first number to add:\n")) #num1 set to accept only numeric input as a float so decimals can be used
                num2 = float(input("Now enter the second number to add:\n")) #num2 set to accept only numeric input as a float
                print("Sum:", num1 + num2, "\n") #Results of provided problem are displayed
            except ValueError:
                print("Error: Please enter numbers only.\n")
                continue
        elif select == 2:
            try:
                num1 = float(input("Please enter the first number to subtract:\n"))
                num2 = float(input("Now enter the second number to subtract:\n"))
                print("Difference:", num1 - num2, "\n")
            except ValueError:
                print("Error: Please enter numbers only.\n")
                continue
        elif select == 3:
            try:
                num1 = float(input("Please enter the first number to multiply:\n"))
                num2 = float(input("Now enter the second number to multiply:\n"))
                print("Product:", num1 * num2, "\n")
            except ValueError:
                print("Error: Please enter numbers only.\n")
                continue
        elif select == 4:
            try:
                num1 = float(input("Please enter the first number to divide:\n"))
                num2 = float(input("Now enter the second number to divide:\n"))
                if num1 == 0 or num2 == 0: #Protection from zero division, returns to beginning of loop
                    print("Cannot divide by zero.\n")
                    continue
                print("Quotient:", num1 / num2, "\n")
            except ValueError:
                print("Error: Please enter numbers only.\n")
                continue
        elif select == 5:
            sys.exit("Terminating program.\n") #Exit program function with message
        else:
            print("Invalid input, please try again.\n") #Simple error handling to account for out of bounds numeric entries
    except ValueError:
        print("Error: Please enter numbers only.\n")
        continue