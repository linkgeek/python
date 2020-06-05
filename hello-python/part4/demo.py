# 货币兑换服务系统
service_menu = {'1': '人民币转换美元', '2': '美元转换人民币', '3': '人民币转换欧元', '0': '结束程序'}
lst = ['1', '2', '3', '0']
your_money = 100

print("*******欢迎货币兑换的服务系统*******")
for k in lst:
    print(k, ".", service_menu[k])
    if k != '0':
        print("欢迎使用", service_menu[k], "服务")
        if k == '1':
            print("您需要转换的人民币为：", your_money, "元")
            print("兑换成美元为：", your_money/7.14, "$")
        elif k == '2':
            print("您需要转换的美元为：", your_money, "$")
            print("兑换成人民币为：", your_money*7.14, "元")
        elif k == '3':
            print("您需要转换的人民币为：", your_money, "元")
            print("兑换成欧元为：", your_money * 0.12, "€")
    else:
        print("感谢您的使用，祝您生活愉快，再见！")
    print("＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝")
