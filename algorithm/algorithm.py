'''
假设你手上有面值1块，2块，5块各若干张纸币，你现在需要支付给商家6元钱，请问你有多少种组合，列出每一种组合？
'''


def find_bills(bills, target, bigger, solution=[]):
    if sum(solution) == target:
        print('solution: ', solution)
        yield solution
        return

    if sum(solution) > target:
        return

    for bill in bills:
        if bill < bigger:
            continue
        ways = solution[:]
        ways.append(bill)
        yield from find_bills(bills, target, bill, ways)


# find_bills([1, 2, 5], 6, 1)

solutions = list(find_bills([1, 2, 5], 6, 1))
print('solutions:', solutions)

# 最少组合
# least_way = sorted(solutions, key=lambda x:len(x))[0]
# print('least_way:', least_way)
