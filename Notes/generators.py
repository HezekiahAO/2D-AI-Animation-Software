print(5)

def value():
    yield 9


gen = value()
print(next(gen))


# Yes! In Python, generators are a type of iterable that allow you to iterate over a sequence of values lazily. This means they generate values one at a time as needed, rather than storing the entire sequence in memory at once. This can be very useful when working with large data sets




print(5)

def value():
    yield 9

for v in value():
    print(v)
