# # l1 = [9,9,9,9,9,9,9]
# # l2 = [9,9,9,9]

# # result = []
# # extra_num = 0

# # for a, b in zip(l1, l2):
# #     total = a + b + extra_num
# #     result.append(total % 10)
# #     extra_num = total // 10

# # if extra_num:
# #     result.append(extra_num)

# # print(result)  
# l1 = [1,2,3,4,3]
# l2 = list([1,2,3,4,3])
# l3 = set(l1 )& set(l2)
# if l3 not in l1
# print(l3)

def romanValues(s: str) -> int:
    values = {"I":1,"V":5,"X":10,"L":50,"C":100,"D":500,"M":1000}
    total = 0
    for i in range(len(s)):
        if i+1 < len(s) and values[s[i]]<values[s[i+1]]:
            total -= values[s[i]]
        else:
            total += values[s[i]]

    return total

# Test
s = 'L'
print(romanValues(s))


def addTwoNumbers(l1,l2):
        result=[]
        extra=0
        print(l1)
        length = max(len(l1),len(l2))
        l1=l1+[0]*(length - len(l1))
        l2=l2+[0]*(length - len(l2))

        for x,y in zip(l1,l2):
            total = x+y+extra
            result.append(total%10)
            extra = total//10
        if extra:
            result.append(extra)
        return result

l1 = [9,9,9,9,9,9,9]
l2 = [9,9,9,9]
print(addTwoNumbers(l1,l2))
