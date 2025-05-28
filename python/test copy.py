l1 = [9,9,9,9,9,9,9]
l2 = [9,9,9,9]

result = []
extra_num = 0

for a, b in zip(l1, l2):
    total = a + b + extra_num
    result.append(total % 10)
    extra_num = total // 10

if extra_num:
    result.append(extra_num)

print(result)  
