def capitalize_words(words):
    # Base case: if the list is empty, return an empty list
    if len(words) == 0:
        return []
    
    # Capitalize the first word and recurse on the rest
    return [words[0].upper()] + capitalize_words(words[1:])

print(capitalize_words(['foo', 'bar', 'world', 'hello']))
# Output: ['FOO', 'BAR', 'WORLD', 'HELLO']