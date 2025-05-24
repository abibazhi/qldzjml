from modelscope.pipelines import pipeline
from modelscope.utils.constant import Tasks
from PIL import Image

# 加载多模态聊天模型（假设支持图像输入）
model_id = 'qwen/Qwen3-Chat-Int8-GPU'  # 根据实际情况调整模型ID

# 创建pipeline实例
multi_modal_chat_pipeline = pipeline(task=Tasks.multi_modal_chat, model=model_id)

# 图片路径
image_path = './165.png'  # 替换为你的图片路径

# 打开图片
image = Image.open(image_path)

# 提出问题
text_input = "请描述这张图片，并指出上面的文字是什么？"

# 使用pipeline进行预测
result = multi_modal_chat_pipeline(image, text_input)

# 输出结果
print("模型回答:", result['text'])
