#Write a Python program that will make the most efficient change (the fewest number of coins ; quarters, dimes, nickels, pennies).

#Variables
quarter = 0
dime = 0
nickel = 0
penny = 0
change = 0
cost = 0
paid = 0
x = 0

#User input in float values
cost = float(input("Enter the total cost in dollar value. (i.e. 1.50)\n"))
paid = float(input("Enter the amount paid in dollar value. (i.e. 1.50)\n"))

#Calculating change and rounding to the nearest hundredth
change = paid - cost
change = round(change, 2)

#If statement logic for dividing change amount into coins
if change >= .01:#As long as there is a penny able to be calculated, continue statement
    quarter = int(change / .25)#Divide change into integer amount of quarters
    x = round(change - (quarter * .25), 2)#Grab quarter value from quarter amount and subtract from change, then put in variable x to continue statement
    if x >= .01:#Repeat process with x
        dime = int(x / .10)
        x = round(x - (dime * .10), 2)
        if x >= .01:
            nickel = int(x / .05)
            x = round(x - (nickel * .05), 2)
            if x >= .01:
                penny = int(x / .01)
                x = round(x - (penny * .01), 2)

#Print with f literal strings
print(f"Your charge: {cost}\nYou paid: {paid}\nYour change is: {change}\nQuarters: {quarter}\nDimes: {dime}\nNickels: {nickel}\nPennies: {penny}")