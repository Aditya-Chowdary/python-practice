l1 = [1,3,2,3,4]
l2 = [2,4,5]

l3 = l1 + l2
l3 = sorted(l3)
length = len(l3)

if length % 2 != 0:
    median = l3[length // 2]
else:
    middle1 = l3[(length // 2) - 1]
    middle2 = l3[length // 2]
    median = (middle1 + middle2) / 2

print("Median is:", median)
