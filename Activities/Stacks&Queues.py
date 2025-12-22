from collections import deque

def reverse_string(s):
    #Create an empty stack
    stack = deque()

    #Push all characters of the string onto the stack
    for char in s:
        stack.append(char)

    #Pop characters and rebuild the string
    reversed_chars = []
    while stack:
        reversed_chars.append(stack.pop())

    #Join the characters into a single string
    return ''.join(reversed_chars)

text = "Reverse me"
print(reverse_string(text))