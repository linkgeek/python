# 50 14 * * 1-5 bash /data/www/giant/python/monitor/cron.sh > /data/www/giant/python/data/cron_fund_log.txt 2>&1  # 每周一到周五14点50运行一下脚本程序，并把输入写入 log 文件中
/usr/local/bin/python3 /data/www/giant/python/monitor/fund/eastmoney.py