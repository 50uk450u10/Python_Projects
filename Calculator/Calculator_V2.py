import sys

class Calculator:

    #Constructor
    def __init__(self):
        #Variables
        self.num1 = 0
        self.num2 = 0
        self.select = 0

    #Function to condense error handling
    def get_num(self, prompt):
        while True:
            try:
                return float(input(prompt))
            except ValueError: #If an input is non-numeric, ValueError exception will throw
                print("Error: Please enter numbers only.\n")

    #Functions for operations
    def add(self):
        self.num1 = self.get_num("Please enter the first number to add:\n")
        self.num2 = self.get_num("Now enter the second number to add:\n")
        print("Sum:", self.num1 + self.num2, "\n")

    def subtract(self):
        self.num1 = self.get_num("Please enter the first number to subtract:\n")
        self.num2 = self.get_num("Now enter the second number to subtract:\n")
        print("Difference:", self.num1 - self.num2, "\n")

    def multiply(self):
        self.num1 = self.get_num("Please enter the first number to multiply:\n")
        self.num2 = self.get_num("Now enter the second number to multiply:\n")
        print("Product:", self.num1 * self.num2, "\n")

    def divide(self):
        self.num1 = self.get_num("Please enter the first number to divide:\n")
        self.num2 = self.get_num("Now enter the second number to divide:\n")
        if self.num2 == 0: #Check divisor for zero and handle edge case
            print("Quotient:", self.num1 / self.num2, "\n")
            return
        print("Cannot divide by zero.\n")

    def run(self):
        #Welcome message
        print("Welcome to your calculator!\nPlease select from the following menu with the corresponding number:")

        #Enter while loop
        while self.select != 5:
            try:
                self.select = int(input("1. Addition\n2. Subtraction\n3. Multiplication\n4. Division\n5. Exit\n"))
            except ValueError:
                print("Error: Please enter numbers only.\n")
                continue

            if self.select == 1:
                self.add()
            elif self.select == 2:
                self.subtract()
            elif self.select == 3:
                self.multiply()
            elif self.select == 4:
                self.divide()
            elif self.select == 5:
                sys.exit("Terminating program.\n")
            else:
                print("Invalid input, please try again\n")

calc = Calculator() #Creates object
calc.run() #Enters the program