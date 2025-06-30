from filter import Filter
from processing import Processing  

input_text = """Processing an array of mixed types: 101, "hello", 2023-12-25, @#$, 45.67, world, 12/25/2023, !!!, array, 20/02/2021, 02/1/2991, 3-2-2029."""

filtered = Filter.create(input_text).date().number().result()
tokens = Processing.create(filtered).split().unique(space=True, count=True).result()

print("Tokens:", tokens)
