'''
Practice modifying a list in place using append, insert, pop, and element replacement.

Your task: Modify a list of strings so that:
    Add 'START' at the beginning.
    Add 'END' at the end, then remove the last two elements.
    Replace every 'N/A' with 'Unknown'
'''
def clean_strings(items):
    items.insert(0, "START"); items.append("END"); items.pop(); items.pop() #Add START to the beginning of the string and END to the end, then remove last two elements.
    for i, v in enumerate(items): #Replace N/A with Unknown
        if v == "N/A" : items[i] = "Unknown"
    return items

print(clean_strings(["apple", "N/A", "banana"]))