# -*- coding: utf-8 -*-

"""
晒工资（计算个税）
"""


def income_tax(wage):
    """
    :param wage: 到手的月收入

    个税速算：全月应纳税所得额(Taxable Income) × 适用税率(Tax Rate) - 速算扣除数(Quick Deduction)

    #       Ti     Tr    Qd
    -----------------------
    1      ~1500   3%     0
    2  1500~4500  10%   105
    3  4500~9000  20%   555
    4  9000~35000 25%  1005
    5 35000~55000 30%  2755
    6 55000~80000 35%  5505
    7 80000~      45% 13505
    """
    quick_deductions = (
        (0.00000, 0.03, 0.00000),  # 1
        (1500.00, 0.10, 105.000),  # 2
        (4500.00, 0.20, 555.000),  # 3
        (9000.00, 0.25, 1005.00),  # 4
        (35000.0, 0.30, 2755.00),  # 5
        (55000.0, 0.35, 5505.00),  # 6
        (80000.0, 0.45, 13505.0),  # 7
    )
    threshold = 3500  # 起征点
    taxable_income = wage - threshold  # 应缴税工资
    if taxable_income <= 0:
        return 0
    level = 6
    for index, i in enumerate(quick_deductions):
        if taxable_income < i[0]:
            level = index - 1
            break
    return taxable_income * quick_deductions[level][1] - quick_deductions[level][2]


MEAL_ALLOWANCE_PER_DAY = 15
# 扣款项
INSURANCE = 291
# RETIREMENT_INSURANCE 养老保险
# MEDICAL_INSURANCE 医疗保险
# UNEMPLOYMENT_INSURANCE 失业保险
HOUSING_FUND = 200
LOVE_FUND = 100


def money(basic_wage=6000, overtime_pay=0, work_days=23, leave_days=0):
    """ 计算最终所得工资

    :param basic_wage: 基本工资
    :param overtime_pay: 加班工资
    :param work_days: 工作天数
    :param leave_days: 请假天数
    :return:
    """
    # 工资
    wage = basic_wage + overtime_pay

    # 补贴
    meal_allowance = work_days * MEAL_ALLOWANCE_PER_DAY  # 餐补
    wage += meal_allowance

    wage -= INSURANCE + HOUSING_FUND
    tax = income_tax(wage)
    wage -= tax + LOVE_FUND

    return {
        'base wage': basic_wage,
        'overtime pay': overtime_pay,
        'leave deduction': 0,
        'meal allowance': meal_allowance,
        'insurance': INSURANCE,
        'housing fund': HOUSING_FUND,
        'income tax': tax,
        'love fund': LOVE_FUND,
        'final wage': wage,
    }


def test():
    print income_tax(-1)
    print income_tax(0)
    print income_tax(3500)
    print income_tax(4000)
    print income_tax(5854)
    print income_tax(103500)


def cli():
    import argparse

    parser = argparse.ArgumentParser(description='按照工资计算公式计算最终能领到的工资。')
    parser.add_argument('wage', type=int, help='基本工资，默认 6000', default=6000)
    parser.add_argument('--work', metavar='work_days', type=int, help='工作天数，默认 23', default=23)
    parser.add_argument('--leave', metavar='leave_days', type=int, help='请假天数，默认 0（暂不支持）', default=0)
    args = parser.parse_args()

    rst = money(args.wage, work_days=args.work, leave_days=args.leave)

    print '\n　您的工资清单如下：\n'
    print '　　　　　　基本工资：＋%9.2f 元' % rst['base wage']
    print '　　　　　　加班工资：＋%9.2f 元' % rst['overtime pay']
    print '　　　　　　　　餐补：＋%9.2f 元' % rst['meal allowance']
    print '　　　　　　　　保险：－%9.2f 元' % rst['insurance']
    print '　　　　　租房公积金：－%9.2f 元' % rst['housing fund']
    print '　　　　　　请假扣除：－%9.2f 元' % rst['leave deduction']
    print '　　　缴纳个人所得税：－%9.2f 元' % rst['income tax']
    print '　　　　家庭爱心基金：－%9.2f 元' % rst['love fund']
    print '-' * 50
    print '　　　　　　税后收入：　%9.2f 元' % rst['final wage']


if __name__ == '__main__':
    # test()
    # print money()
    cli()
