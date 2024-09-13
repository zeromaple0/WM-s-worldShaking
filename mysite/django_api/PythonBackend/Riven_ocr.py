import json
import os
import re
from fuzzywuzzy import fuzz
from wx_ocr import WxOcr


class RivenOcr:
    """
    用于识别图片中的紫卡信息，并返回识别结果
    传入相对路径，返回识别结果
    结果为列表
    """

    def __init__(self, img_path):
        # 获得当前项目路径
        self.project_path = os.path.dirname(os.path.abspath(__file__))
        self.img_path = img_path
        self.comparison_list = json.load(open("static/riven_cname.json", "r", encoding="utf-8"))
        # 调用wx_ocr
        ocr_result = self.wx_ocr_result_callback(self.img_path)
        print(ocr_result)
        # 最终处理要返回的结果process_result
        self.process_result = self.process_wxocr_result(ocr_result)

    def wx_ocr_result_callback(self, img_path):
        return WxOcr(img_path).results

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
        combined_texts = self.remove_non_chinese_characters(combined_texts)
        # 把筛选后的结果与参考列表进行对比，调用对比函数
        combined_texts = self.compare_name(combined_texts, self.comparison_list)
        return combined_texts

    # 删除列表中所有元素的数字
    def remove_non_chinese_characters(self, lst):
        ocr_list = []
        # 过滤output_list中的每一个元素，只保留该元素的汉字部分
        for line in lst:
            # 使用正则表达式匹配汉字
            match = re.search(r'[\u4e00-\u9fff]+', line)
            if match:
                # 提取匹配到的汉字部分并添加到列表中
                ocr_list.append(match.group())
        return ocr_list
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

    def print_result(self, comparison_list):
        for i in comparison_list:
            print(i)


if __name__ == '__main__':
    ocr_result = RivenOcr("static/多张紫卡.png")
    ocr_result.print_result(ocr_result.process_result)
