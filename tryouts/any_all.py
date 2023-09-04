
l = ['1.5', '1.5-4', '1.5-4-1', '1.5-4-1-7']
l1 = ['1.5', None, '1.5-4-1', '1.5-4-1-7']
rn = any([True, False])
ra = all([True, False])

rl = all(l1)


print(rl)
