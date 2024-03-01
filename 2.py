intp = input().split(' ')

str = intp[0]
n = int(intp[1])

res = ""
bucket = [0 for _ in range(128)]

for i in range(len(str)):
    if bucket[ord(str[i])] >= 1:
        res += '-'
    else:
        res += str[i]

    bucket[ord(str[i])] += 1
    if i >= n:
        bucket[ord(str[i-n])] -= 1

print(res)