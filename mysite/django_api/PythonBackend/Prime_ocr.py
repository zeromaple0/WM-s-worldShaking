import json
import os
from fuzzywuzzy import fuzz
import sys
from wx_ocr import WxOcr

#用于隐藏print输出
class HiddenPrints:
    def __enter__(self):
        self._original_stdout = sys.stdout
        sys.stdout = open(os.devnull, 'w')

    def __exit__(self, exc_type, exc_val, exc_tb):
        sys.stdout.close()
        sys.stdout = self._original_stdout



class PrimeOcr:
    """
    调用微信本地ocr，传入图片相对路径或绝对路径
    最终处理结果保存为成员变量process_result
    """
    def __init__(self, img_path):
        # 获得当前项目路径
        self.project_path = os.path.dirname(os.path.abspath(__file__))
        self.img_path = img_path
        self.comparison_list = json.load(open("static/tradable_parts_name.json", "r", encoding="utf-8"))
        # 调用wx_ocr
        ocr_result = self.wx_ocr_result_callback(self.img_path)

        # 最终处理要返回的结果process_result
        self.process_result = self.process_wxocr_result(ocr_result)

    def wx_ocr_result_callback(self, img_path):
        # 屏蔽掉打印信息
        with HiddenPrints():
            ocr_result = WxOcr(img_path).results
        return ocr_result

    def process_wxocr_result(self, ocr_results):
        # 存储最终合并后的文本
        combined_texts = []
        # 存储已处理项目的索引，避免重复处理
        processed_indices = set()

        # 遍历每一个OCR识别结果
        for i, item in enumerate(ocr_results):
            # 如果当前项目已经处理过，则跳过
            if i in processed_indices:
                continue

            # 以当前项目为中心，收集与之位置相近的文本
            combined = [item['text']]
            for j, other_item in enumerate(ocr_results):
                # 如果是比较对象自身，或者已经被处理过，则跳过
                if j in processed_indices or i == j:
                    continue
                try:
                    # 计算两个文本在x轴和y轴上的距离
                    distance_x = abs(item['pos']['x'] - other_item['pos']['x'])
                    distance_y = abs(item['pos']['y'] - other_item['pos']['y'])
                except KeyError:
                    print("Error: Missing position information in OCR result.", item)
                    continue

                # 计算两个文本直接的距离
                # distance = (distance_x ** 2 + distance_y ** 2) ** 0.5

                # 如果距离在设定范围内，则认为位置相近，将文本加入合并列表，并标记为已处理
                if distance_x <= 100 and distance_y <= 60:
                    combined.append(other_item['text'])
                    processed_indices.add(j)  # 标记比较对象为已处理

            # 将合并后的文本加入结果列表，并标记当前项目为已处理
            combined_texts.append(''.join(combined))
            processed_indices.add(i)  # 标记当前项目为已处理
        # 删除组合元素中的数字
        combined_texts = self.remove_numbers(combined_texts)
        #把筛选后的结果与参考列表进行对比，调用对比函数
        combined_texts = self.compare_name(combined_texts, self.comparison_list)
        return combined_texts

    # 删除列表中所有元素的数字
    def remove_numbers(self, lst):
        return [item for item in lst if not any(char.isdigit() for char in item)]

    def compare_name(self, ocr_list, comparison_list):
        compare_result = []
        # 遍历OCR名称列表和比较名称列表，寻找相似度高于80%的名称
        for ocr_name in ocr_list:
            # 遍历比较名称列表,保存相似度最高的名称
            best_match = None
            best_ratio = 0
            for comparison_name in comparison_list:
                ratio = fuzz.ratio(ocr_name, comparison_name)
                if ratio > best_ratio and ratio > 50:
                    best_match = comparison_name
                    best_ratio = ratio
            if best_match is not None:
                compare_result.append(best_match)

        return compare_result


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python Prime_ocr.py 图片路径")
    else:
        # 使用从命令行接收的第一个参数
        obj = PrimeOcr(sys.argv[1])
        print(obj.process_result)
