from impala.dbapi import connect


class Impala:
    conn = connect(host='pro-bigdata-api.stevengame.com', port=21000)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM mytable LIMIT 100')
    results = cursor.fetchall()
    print(results)


Impala()