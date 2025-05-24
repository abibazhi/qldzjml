from transformers import AutoModelForCausalLM, AutoTokenizer

model_name = "Qwen/Qwen3-0.6B"  # 假设这是正确的模型名称Qwen/Qwen3-0.6B
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name)

import torch
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(f"Using device: {device}")

model.to(device)  # 将模型移动到指定设备

'''
def generate_text(prompt):
    inputs = tokenizer(prompt, return_tensors="pt")
    outputs = model.generate(**inputs, max_length=50)  # 可以根据需要调整max_length
    return tokenizer.decode(outputs[0], skip_special_tokens=True)
'''

def generate_text(prompt):
    inputs = tokenizer(prompt, return_tensors="pt")
    # 将输入张量移动到与模型相同的设备
    inputs = {key: value.to(device) for key, value in inputs.items()}
    
    outputs = model.generate(**inputs, max_length=50)  # 可以根据需要调整max_length
    return tokenizer.decode(outputs[0], skip_special_tokens=True)


prompt = "你好，介绍一下你自己吧。"
print(generate_text(prompt))
