# 50 14 * * 1-5 bash /root/fund/fund_code.sh > /root/fund/log.txt 2>&1  # 这句话的意思是 每周一到周五14点50运行一下脚本程序，并把输入写入 log 文件中
/root/anaconda3/bin/python3 /data/www/python/stock/fund_monitor.py