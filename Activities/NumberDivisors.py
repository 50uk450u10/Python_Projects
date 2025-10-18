#Function for finding all divisors of a number
def findDivisors(n):
    #"i for i in range" is shorthand code for a for loop that makes a list.
    #The loop will go through all numbers up to the n number, then check if those numbers are cleanly divisible
    return [i for i in range(1, n + 1) if n % i == 0]

#Function for building the dictionary of user input numbers
def buildDictionary():
    #n: is the key for the dictionary. This function will use the findDivisors for each integer in a range of 10 input by the user
    return {n: findDivisors(n) for n in [int(input(f"Enter integer #{i + 1}: ")) for i in range(10)]}

#Assignment of "d" and output
d = buildDictionary()
print("The dictionary is : d = ", d)