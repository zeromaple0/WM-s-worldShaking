import csv
from .models import PrimePrice


class Update_prime_price:

    def __init__(self, update_file_url):

        self.count = 0
        self.update_prime_price(update_file_url)
        print(f"更新结束,更新了{self.count}条数据")

    def update_prime_price(self, update_file_url):

        with open(update_file_url, mode='r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                try:
                    # 查找现有的产品
                    primeprice = PrimePrice.objects.get(url_name=row['url_name'])

                    # 更新字段,如果存在空的值，则赋值为0
                    platinum1 = float(row['platinum1']) if row['platinum1'] else 0
                    platinum2 = float(row['platinum2']) if row['platinum2'] else 0
                    platinum3 = float(row['platinum3']) if row['platinum3'] else 0
                    primeprice.platinum1 = platinum1
                    primeprice.platinum2 = platinum2
                    primeprice.platinum3 = platinum3

                    primeprice.save()
                    self.count += 1

                except primeprice.DoesNotExist:
                    # 如果部件不存在，可以选择创建新记录
                    primeprice = PrimePrice(
                        url_name=row['url_name'],
                        zh_name=row['zh_name'],
                        platinum1=row['platinum1'],
                        platinum2=row['platinum2'],
                        platinum3=row['platinum3'],

                    )

                    primeprice.save()
                    print(f'Successfully created new product: {primeprice.zh_name}')
                except Exception as e:
                    print(f'Error updating product: {row["url_name"]} - {e}')
