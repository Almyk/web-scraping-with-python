import pymysql

pwFile = open("mysql.key", "r")
pw = pwFile.readline()
pw = pw.strip()
pwFile.close()

conn = pymysql.connect(host='localhost', user='root', passwd=pw, db='mysql')
cur = conn.cursor()
cur.execute("USE scraping")
cur.execute("SELECT * FROM pages WHERE id=1")
print(cur.fetchone())
cur.close()
conn.close()
