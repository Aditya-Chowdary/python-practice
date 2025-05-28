#Tuples are immutable, meaning you cannot change, 
# add, or remove items after the tuple is created.

t = (1, 2, 3, 2, 4, 2)
print(t.count(2))  # Output: 3

t = (10, 20, 30, 40)
print(t.index(30))  # Output: 2

t = (1, 2, 3)
print(len(t))  # Output: 3

t = ('a', 'b', 'c')
print('a' in t)  # Output: True
print('z' not in t)  # Output: True

t = (10, 20, 30)
print(t[0])  # Output: 10
print(t[-1])  # Output: 30

t = (1, 2, 3, 4, 5)
print(t[1:4])  # Output: (2, 3, 4)

a = (1, 2)
b = (3, 4)
print(a + b)  # Output: (1, 2, 3, 4)

t = (1, 2)
print(t * 3)  # Output: (1, 2, 1, 2, 1, 2)

t = ('a', 'b', 'c')
for item in t:
    print(item)


t = (1, 2, 3)
a, b, c = t
print(a, b, c)  # Output: 1 2 3

t = (1, (2, 3), 4)
print(t[1][0])  # Output: 2

t = ('a', 'b', 'c')
for index, value in enumerate(t):
    print(index, value)

t = (1, 2, 3)
print(max(t))    # 3
print(min(t))    # 1
print(sum(t))    # 6
print(sorted(t)) # [1, 2, 3]
