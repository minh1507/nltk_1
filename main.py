from filter import Filter
from processing import Processing  
from display import Display

input_text = """Processing an array of mixed types: 101, "hello", 2023-12-25, @#$, 45.67, world, 12/25/2023, !!!, array, 20/02/2021, 02/1/2991, 3-2-2029."""

filtered = Filter.create(input_text).date().number().result()
process = Processing.create(filtered)

# Scenario 1: token base
tokens = process.split().unique(space=True, count=True).sort(by="alpha", reverse=False).result()

print("Tokens base:")
Display.table(tokens, count=False)

print("\n" + "="*40 + "\n")

# Scenario 2: token base with count
tokens = process.split().unique(space=True, count=True).sort(by="alpha", reverse=False).result()

print("Tokens with count:")
Display.table(tokens, count=True)

print("\n" + "="*40 + "\n")

# Scenario 3: token base with count and stemmer
tokens = process.split().stem(auto_detect=True).unique(space=True, count=True).sort(by="alpha", reverse=False).result()

print("Tokens with count:")
Display.table(tokens, count=True)




