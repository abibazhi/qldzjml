#pip install transformers torch requests pillow

from PIL import Image
import requests
from io import BytesIO
from transformers import AutoModelForCausalLM, AutoTokenizer

# 加载 OFA 模型和分词器
model_name = "damo/ofa-base-m6"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name)

def preprocess_image(image_path):
    # 读取图像
    if image_path.startswith("http"):
        response = requests.get(image_path)
        img = Image.open(BytesIO(response.content))
    else:
        img = Image.open(image_path)
    return img

def generate_response(image_path, question=None):
    # 预处理图像
    img = preprocess_image(image_path)

    # 根据是否有问题决定输入格式
    if question:
        inputs = tokenizer(f"Question: {question} Given an image:", images=[img], return_tensors="pt")
    else:
        inputs = tokenizer("What does the image describe?", images=[img], return_tensors="pt")

    # 生成响应
    generated_ids = model.generate(**inputs)
    response = tokenizer.batch_decode(generated_ids, skip_special_tokens=True)[0]
    return response

# 示例图片路径或URL
image_url = "https://upload.wikimedia.org/wikipedia/commons/thumb/b/ba/Felis_catus-cat_on_snow.jpg/1920px-Felis_catus-cat_on_snow.jpg"

# 获取并打印描述
description = generate_response(image_url)
print("Description of the image:")
print(description)

# 提出一个问题
question = "What animal is in the image?"
answer = generate_response(image_url, question)
print("\nAnswer to the question:")
print(answer)




