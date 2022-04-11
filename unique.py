a, b = [int(i) for i in input().split()]
s = 1
for i in range(a):
    s *= a
    if s > b:
        s %= b
print(s)
