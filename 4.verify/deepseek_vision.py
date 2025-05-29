from transformers import AutoModelForCausalLM, AutoTokenizer

model_name = "deepseek-ai/deepseek-vision-7b-base"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(
    model_name,
    torch_dtype=torch.float16,  # 使用半精度减少显存占用
    device_map="auto"  # 自动分配设备
)
