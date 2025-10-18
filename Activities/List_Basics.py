'''
Lists are one of the most versatile data structures in Python. They allow you to store multiple values, index them, and slice sublists.

Your task: Write a function `list_basics(nums)` that returns:
    The first and last element.
    A list of all even numbers.
    The middle three elements (or fewer if the list is short).
    A sorted list of unique values.
'''

def list_basics(nums):
    if not nums: return None, None, [], [], [] #Handles empty list edge cases
    evens = [n for n in nums if isinstance(n, int) and n % 2 == 0] #Calculates all even integers
    mid = len(nums) // 2 #Floor division always returns a whole number
    middle = nums[:] if len(nums) <= 3 else nums[mid - 1 : mid + 2] #Finds the middle 3 elements
    return nums[0], nums[-1], evens, middle, sorted(set(nums))#Return first and last element, all even numbers, the three middle elements, and uniquely sorted values

print(list_basics([10, 3, 5, 8, 2, 9]))