# -*- coding: utf-8 -*-

"""
等额本息还款法:
每月月供额=〔贷款本金×月利率×(1＋月利率)＾还款月数〕÷〔(1＋月利率)＾还款月数-1〕
每月应还利息=贷款本金×月利率×〔(1+月利率)^还款月数-(1+月利率)^(还款月序号-1)〕÷〔(1+月利率)^还款月数-1〕
每月应还本金=贷款本金×月利率×(1+月利率)^(还款月序号-1)÷〔(1+月利率)^还款月数-1〕
总利息=还款月数×每月月供额-贷款本金

等额本金还款法:
每月月供额=(贷款本金÷还款月数)+(贷款本金-已归还本金累计额)×月利率
每月应还本金=贷款本金÷还款月数
每月应还利息=剩余本金×月利率=(贷款本金-已归还本金累计额)×月利率
每月月供递减额=每月应还本金×月利率=贷款本金÷还款月数×月利率
总利息=还款月数×(总贷款额×月利率-月利率×(总贷款额÷还款月数)*(还款月数-1)÷2+总贷款额÷还款月数)
月利率=年利率÷12
"""

from decimal import Decimal, getcontext

getcontext().prec = 33

add = lambda a, b: Decimal(a) + Decimal(b)
sub = lambda a, b: Decimal(a) - Decimal(b)
mul = lambda a, b: Decimal(a) * Decimal(b)
div = lambda a, b: Decimal(a) / Decimal(b)
pow = lambda a, b: Decimal(a) ** Decimal(b)

AVERAGE_CAPITAL_PLUS_INTEREST = 0  # 等额本息
AVERAGE_CAPITAL = 1  # 等额本金

amount_of_loan = 232000  # 贷款金额
repayment_years = 30  # 贷款年数
interest_rate = 0.0375  # 利率

amount_of_loan = Decimal(amount_of_loan)
repayment_years = Decimal(repayment_years)
interest_rate = Decimal(interest_rate)
stage_number = repayment_years * 12  # 还款期数

retain_cent = lambda num: Decimal('%.2f' % num)  # 四舍五入
calculate_interest = lambda amount, rate: retain_cent(Decimal(amount) * Decimal(rate) / 12)
p = lambda num, width: (('%d' if isinstance(num, int) else '%.2f') % num).rjust(width)

# 等额本息

multiple = 1 + interest_rate / 12
multiple_x = multiple ** stage_number
interest_first_month = amount_of_loan * interest_rate / 12


def refund_capital_monthly(n):
    return retain_cent(interest_first_month * (multiple ** (n - 1)) / (multiple_x - 1))


repayment_plan = [refund_capital_monthly(_) for _ in range(1, stage_number + 1)]
repayment_plan[-1] += amount_of_loan - sum(repayment_plan)
repayment_monthly = retain_cent(interest_first_month * multiple_x / (multiple_x - 1))


def refund_interest_monthly(n):
    return repayment_monthly - repayment_plan[n - 1]


def get_debt(n):
    """ 第 n 个月欠款 """
    # return retain_cent(amount_of_loan * multiple ** n - repayment_monthly * (multiple ** n - 1) * 12 / interest_rate)
    return amount_of_loan - repayment_plan[n - 1]

debt = amount_of_loan
for i in range(stage_number):
    interest = debt * interest_rate / 12
    repayment = repayment_plan[i] + interest
    debt -= repayment_plan[i]
    print "%s. %s(%s + %s) %s" % (
        p(i, 3),
        p(repayment_plan[i] + interest, 8),
        p(repayment_plan[i], 8),
        p(interest, 5),
        p(debt, 10)
    )


exit('hello world')

# 等额本金
refund_capital_monthly = retain_cent(amount_of_loan / float(stage_number))  # 每月归还本金
# 被舍去的分之后的小数累计起来会形成误差，所以以下算法并不可靠
# (1 + stage_number) * stage_number / 2 * calculate_interest(refund_capital_monthly, interest_rate)
repayment_plan = [refund_capital_monthly for _ in range(stage_number)]  # 还款计划
repayment_plan[-1] += amount_of_loan - refund_capital_monthly * stage_number

total_repayment = 0.0
total_interest = 0.0
debt = amount_of_loan
for i in range(stage_number):
    interest = calculate_interest(debt, interest_rate)
    repayment = repayment_plan[i] + interest
    total_repayment += repayment
    total_interest += interest
    debt -= repayment_plan[i]
    print "%s. %s(%s + %s) %s" % (
        p(i + 1, 3),
        p(repayment, 8),
        p(repayment_plan[i], 8),
        p(interest, 5),
        p(debt, 10)
    )

print calculate_interest(refund_capital_monthly, interest_rate)
print amount_of_loan, total_repayment, total_interest

