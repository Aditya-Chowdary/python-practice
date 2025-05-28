# sets_in_python.py
# Author: OpenAI ChatGPT
# Description: Complete demonstration of Python sets and all their methods

print("🔷 Python Sets - A Complete Guide 🔷\n")

# ✅ 1. Creating Sets
set1 = {1, 2, 3, 4}
set2 = set([3, 4, 5, 6])
set3 = set()  # Empty set, NOT {}

print("Set 1:", set1)
print("Set 2:", set2)
print("Empty Set:", set3)
print()

# ✅ 2. Set is Unordered and Has Unique Elements
dupes = {1, 2, 2, 3}
print("Set removes duplicates:", dupes)
print()

# ✅ 3. Adding Elements
set1.add(10)
print("After adding 10:", set1)

# ✅ 4. Update (Add multiple elements)
set1.update([20, 30])
print("After update with [20, 30]:", set1)
print()

# ✅ 5. Removing Elements
set1.remove(10)  # Raises KeyError if not found
print("After remove(10):", set1)

set1.discard(100)  # No error if 100 not found
print("After discard(100):", set1)

removed = set1.pop()  # Removes a random element
print(f"Pop removed {removed}: {set1}")

set1.clear()
print("After clear():", set1)
print()

# ✅ 6. Set Operations
a = {1, 2, 3, 4}
b = {3, 4, 5, 6}

print("Set A:", a)
print("Set B:", b)
print("Union (a | b):", a | b)
print("Intersection (a & b):", a & b)
print("Difference (a - b):", a - b)
print("Symmetric Difference (a ^ b):", a ^ b)
print()

# ✅ 7. Using Methods for Set Operations
print("union():", a.union(b))
print("intersection():", a.intersection(b))
print("difference():", a.difference(b))
print("symmetric_difference():", a.symmetric_difference(b))
print()

# ✅ 8. Set Comparisons
print("a == b:", a == b)
print("a != b:", a != b)
print("a > b (is superset):", a > b)
print("a < b (is subset):", a < b)
print("a.issubset(b):", a.issubset(b))
print("a.issuperset(b):", a.issuperset(b))
print("a.isdisjoint(b):", a.isdisjoint(b))
print()

# ✅ 9. Frozen Sets (Immutable sets)
frozen = frozenset([1, 2, 3])
print("Frozen Set:", frozen)

# frozen.add(4)  # ❌ AttributeError: can't modify frozenset
print()

# ✅ 10. Other Useful Functions
print("Length of set a:", len(a))
print("3 in a:", 3 in a)
print("Convert list to set:", set([1, 1, 2, 3, 4, 4]))
print()

# ✅ 11. Looping through a set
print("Looping over set a:")
for item in a:
    print(item)

# ✅ 12. Set Comprehension
squared = {x**2 for x in range(5)}
print("Set comprehension:", squared)
