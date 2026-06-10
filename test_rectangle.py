from custom_shapes.rectangle import Rectangle

# Create a rectangle instance
rect = Rectangle(10, 5)

# Test iteration
print("Iterating over Rectangle instance:")
for item in rect:
    print(item)

# Expected output:
# {'length': 10}
# {'width': 5}
