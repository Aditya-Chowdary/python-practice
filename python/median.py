l1 = [1, 2, 3]
l2 = [3, 4, 5]

combined = l1 + l2
combined = sorted(combined)
length = len(combined)

if length % 2 == 1:
    median = combined[length // 2]
else:
    mid1 = combined[length // 2 - 1]
    mid2 = combined[length // 2]
    median = (mid1 + mid2) / 2

print(median)
