'''
Sometimes lists are not efficient for large numeric datasets. Python’s `array` provides more compact storage.
Your task: Convert a list of integers into an array and return its length, total sum, and average.
'''

from array import array

def array_stats(ints):
    arr = array("i", ints) #Convert list to array of integers
    return len(arr), sum(arr), sum(arr) / len(arr) if arr else 0 #Return length, sum, and average

print(array_stats([1, 2, 3, 4, 5]))