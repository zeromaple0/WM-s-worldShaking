import sqlite3
import csv

# 数据库文件路径
db_file = 'mysite/db.sqlite3'

# CSV文件路径
csv_file_path = 'price_090412.csv'

# 创建数据库连接
conn = sqlite3.connect(db_file)
cursor = conn.cursor()

# 清空表（可选）
# cursor.execute('DELETE FROM django_api_primeprice;')

# 插入数据
with open(csv_file_path, 'r', newline='', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile)
    insert_query = '''
    INSERT INTO django_api_primeprice (url_name, zh_name, platinum1, platinum2, platinum3, platinum_avg)
    VALUES (?, ?, ?, ?, ?, ?)
    '''
    for row in reader:
        # 将空字符串转换为0
        platinum1 = float(row['platinum1'] or 0)
        platinum2 = float(row['platinum2'] or 0)
        platinum3 = float(row['platinum3'] or 0)
        platinum_avg = float(row['platinum_avg'] or 0)

        cursor.execute(insert_query, (
            row['url_name'],
            row['zh_name'],
            platinum1,
            platinum2,
            platinum3,
            platinum_avg
        ))

# 提交事务
conn.commit()

# 关闭数据库连接
conn.close()

print("数据导入完成。")