from filter import Filter
from processing import Processing  
from display import Display

input_text = """Processing an array of mixed types: 101, "hello", 2023-12-25, @#$, 45.67, world, 12/25/2023, !!!, array, 20/02/2021, 02/1/2991, 3-2-2029."""

filtered = Filter.create(input_text).date().number().result()
process = Processing.create(filtered)

tokens = process.split().unique(space=True, count=True).sort(by="alpha", reverse=False).result()
print("Scenario 1 - Token base:")
Display.table(tokens, count=True)

print("\n" + "="*50 + "\n")

tokens = process.split().unique(space=True, count=True).stem(auto_detect=True).sort(by="alpha", reverse=False).result()
print("Scenario 3 - With stemming:")
Display.table(tokens, count=True)

print("\n" + "="*50 + "\n")

tokens = process.split().unique(space=True, count=True).tag().sort(by="alpha", reverse=False).result()
print("Scenario 4 - With POS tagging:")
Display.table(tokens, count=True, tags=True)







