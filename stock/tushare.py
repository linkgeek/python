import tushare as ts
import datetime
import time
#from pandas import Dataframe

# ts.set_token('80194d02ee891b04d3e406067531fc592199faa59e1e0c310b125845')
# ts.set_token('be3dddcd0ebf47cb8586afe0428666a1547ae0fc999682d245e8ee1c')
# pro = ts.pro_api()
# df = pro.daily_basic(ts_code='000725', trade_date='20210426', fields='ts_code,trade_date,turnover_rate,volume_ratio,pe,pb')
# print(df)
# 实时监测函数，code为6位数字代码字符串组成的数组,监测在10分钟内跌幅大于5%和实时跌幅较开盘价大于10%时，发送邮件通知
# time_mins为跌速时间，change_mins_max为跌速深度，change_max为较开盘跌幅
def monitor(code, time_mins=10, change_mins_max=5, change_max=10):
    data_today = []  # 储存采集回来的数据
    n = 1  # 记录从循环次数
    while 1:
        try:
            # now_time为记录当前时间，由于从Tushare取回的实时分笔数据只有时间，
            # 没有日期，所以用上面的操作把现在的时间的日期换成1900:1:1日，方便计算时间差
            now_time = datetime.datetime.strptime(datetime.datetime.strftime(datetime.datetime.now(), '%H:%M:%S'),
                                                  '%H:%M:%S')

            # 计算当前时间和中午11:30休市时间的差值
            rest_time = now_time - datetime.datetime.strptime('11:30:00', '%H:%M:%S')
            print(now_time, rest_time, rest_time.days, rest_time.seconds)

            # 11:30~13:00为中午休市时间，时长5400 seconds
            if rest_time.days == 0 and rest_time.seconds > 0 and rest_time.seconds < 5400:
                print('中午休市时间')
                while rest_time.days == 0 and rest_time.seconds > 0 and rest_time.seconds < 5400:
                    now_time = datetime.datetime.strptime(
                        datetime.datetime.strftime(datetime.datetime.now(), '%H:%M:%S'), '%H:%M:%S')
                    rest_time = now_time - datetime.datetime.strptime('11:30:00', '%H:%M:%S')
                    # 循环等待中午休市时间的结束
                    time.sleep(2)
            # 下午15:00结束交易，与11:30的时间差为12600 seconds，关闭程序
            if rest_time.days == 0 and rest_time.seconds > 12600:
                print('交易时间已结束!')
                break

            flag = 0  # 旗帜，flag==1则说明出现预警
            print('第%s次抓取数据' % n)
            n += 1  # 每循环一次+1
            change_max = change_max
            realtime_qutoes = ts.get_realtime_quotes(code)  # 从tushare采集实时分笔数据
            last_time = datetime.datetime.strptime(realtime_qutoes.loc[0][31], '%H:%M:%S')
            # last_time记录从Tushare得到数据里的时间，realtime_qutoes.loc[0][31]为时间，存储格式为字符串'%H:%M:%S'
            if (last_time - now_time).days == 0 and (last_time - now_time).seconds > 10:
                # 如果从realtime_qutoes得到的时间大于当前实际时间，那么说明，当前市场未在交易，
                # 得到的数据为上一交易日最后一笔交易数据，为避免交易所时间和本地时间不一致，设置10 seconds误差
                print('今天不是交易日或者未到交易时间!')
                break

            print('数据抓取成功!')
            data_today.insert(0, realtime_qutoes)  # 储存入数组
            if len(data_today) > 100 * time_mins:
                for i in range(0, 60 * time_mins):
                    # 为了避免data_day数组过长，增加内存占用，所以当长度大于一定程度时，删除一部分
                    del data_today[len(data_today) - 1]
            if len(data_today) > 30 * time_mins:
                # 只需要对应时长的数组
                time_len = 30 * time_mins
            else:
                time_len = len(data_today)
                # 如果股票刚开始交易，分笔数据没有那么多，就全部作为需要的使用
            for i in range(0, len(code)):
                if (float(data_today[0].loc[i][2]) - float(data_today[time_len - 1].loc[i][2])) < -1 * change_mins_max:
                    # 短时间下跌幅的确定
                    flag = 1  # 改变旗帜的值
                    text_add = '%s 分钟跌幅超%s%%' % (time_mins, change_mins_max)
                    # text_add作为邮件提醒的部分文本，当一只股票达到预警值时，结束继续查找其它股票情况，立即发送邮件提醒
                    break
                if (float(data_today[0].loc[i][2]) - float(data_today[time_len - 1].loc[i][2])) > change_mins_max:
                    # 短时间上涨幅的确定
                    flag = 1  # 改变旗帜的值
                    text_add = '%s 分钟涨幅超%s%%' % (time_mins, change_mins_max)
                    # text_add作为邮件提醒的部分文本，当一只股票达到预警值时，结束继续查找其它股票情况，立即发送邮件提醒
                    break
                if 100 * (float(data_today[0].loc[i][3]) - float(data_today[0].loc[i][1])) / float(
                        data_today[0].loc[i][2]) < -1 * change_max:
                    change = 100 * (float(data_today[0].loc[i][3]) - float(data_today[0].loc[i][1])) / float(
                        data_today[0].loc[i][2])
                    # 如果当前股价较开盘价跌幅较大，也发送提醒
                    flag = 1
                    text_add = '较开盘价跌%s %%' % (str(change)[:5])
                    break
                if 100 * (float(data_today[0].loc[i][3]) - float(data_today[0].loc[i][1])) / float(
                        data_today[0].loc[i][2]) > change_max:
                    change = 100 * (float(data_today[0].loc[i][3]) - float(data_today[0].loc[i][1])) / float(
                        data_today[0].loc[i][2])
                    # 如果当前股价较开盘价涨幅较大，也发送提醒
                    flag = 1
                    text_add = '较开盘价涨%s %%' % (str(change)[:5])
                    break
                print(i)

            if flag == 1:
                del code[i]
                # 一只股票达到预警后将该只股票剔除，代码数组
                code_text = realtime_qutoes.loc[i][32]
                # 股票6位数字代码
                name = realtime_qutoes.loc[i][0]
                # 股票名字
                open_price = realtime_qutoes.loc[i][1]
                # 股票开盘价
                now_change = ((float(realtime_qutoes.loc[i][3]) - float(realtime_qutoes.loc[i][2])) / float(
                    realtime_qutoes.loc[i][2])) * 100
                # 股票当前涨跌幅
                price = realtime_qutoes.loc[i][3]
                # 当前股价
                high = realtime_qutoes.loc[i][4]
                # 当日最高价
                low = realtime_qutoes.loc[i][5]
                # 当日最低价
                amount = str(float(realtime_qutoes.loc[i][9]) / 1e8)[:4]
                # 当日成交金额，单位亿，有效数字为3位
                time_text = realtime_qutoes.loc[i][31]
                # 采集到数据的分笔时间
                text = '%s %s %s 当前涨跌幅%s%% 开盘价%s 当前价格%s 最高价%s 最低价%s 总金额%s亿 时间%s' \
                       % (
                           code_text, name, text_add, str(now_change)[:5], open_price, price, high, low, amount,
                           time_text)
                # 邮件要发送的文本信息
                #me.email(text)
                print(text)
                # 发送邮件
                if len(code) == 0:
                    # 如果代码数组没有东西了，就结束程序
                    break

        except Exception as e:
            print('error:', e)
            time.sleep(2)
        # 休息2秒，避免频繁请求造成各种问题
        time.sleep(2)


def main():
    ts.get_hist_data('600848')
    exit()
    code = ['000958', '000725']
    monitor(code)


if __name__ == '__main__':
    main()
