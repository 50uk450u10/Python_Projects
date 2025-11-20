import hashlib

#==========PYTHON FUNCTIONS==========

#1
def Greet(name):
    print(f"Welcome, {name}! Hope you're having a great day!\n")

#2
Greet("Darlene")
Greet("Dagon")
Greet("Ty")

#3
def add_numbers(num1, num2):
    sum = int(num1 + num2)
    print(f"The sum of {num1} and {num2} is {sum}.\n")

#4
add_numbers(2, 5)
add_numbers(34, 76)
add_numbers(18, 22)

#5
def square(num):
    return num * num

for i in range(1, 6):
    print(i, square(i))
print()

#6
def check_even_odd(nums):
    if nums % 2 == 0:
        print(f"{nums} is even.\n")
    else:
        print(f"{nums} is odd.\n")

numbers = [1, 5, 8, 27, 54]
for num in numbers:
    check_even_odd(num)

#7
def multiplication_table(num):
    for i in range(1, 13):
        print(f"{num} x {i} = {num * i}")

multiplication_table(6)
print()
multiplication_table(8)
print()

#==========CYBERSECURITY FUNCTIONS==========

#8
def check_password_strength(password):
    score = 0
    if len(password) >= 8:
        score += 1
    if any(c.isupper() for c in password):
        score += 1
    if any(c.islower() for c in password):
        score += 1
    if any(c.isdigit() for c in password):
        score += 1
    if any(c in "!@#$%^&*()-_=+[]{};:'\",.<>?/|" for c in password):
        score += 1

    if score <= 2:
        return "Weak"
    elif score == 3 or score == 4:
        return "Medium"
    else:
        return "Strong"
    
#9
passwords = ["cat123", "Password1", "Ab(d3fGh1J", "abcdEFGH", "qwerty"]

for p in passwords:
    print(p, check_password_strength(p))
print()

#10
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

#11
for p in passwords:
    print(p, hash_password(p))
print()

#12
def brute_force(target, guesses):
    for g in guesses:
        if g == target:
            return f"Password found: {g}"
    return "Password not found."

result = brute_force("Password1", passwords)
print(result)
print()

#13
def dictionary_attack(hashTarget, guesses):
    for g in guesses:
        if hash_password(g) == hashTarget:
            return f"Password found: {g}"
    return "Password not found."

target = hash_password("Ab(d3fGh1J")
result = dictionary_attack(target, passwords)
print(result)
print()

#Challenge
def analyze_password(password):
    return check_password_strength(password), hash_password(password)

print(analyze_password("Ab(d3fGh1J"))
