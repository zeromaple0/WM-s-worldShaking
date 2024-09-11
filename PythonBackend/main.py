from Prime_ocr import PrimeOcr

img_path = "static/部件5.jpg"
Prime_ocr = PrimeOcr(img_path)
res = Prime_ocr.process_result
print("最终结果:")
print(res)
