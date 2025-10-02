from PIL import Image

# 假设 combined 是修复后的图像对象
# 计算裁剪区域，例如，如果你想裁剪掉右侧50像素：
left = 0
top = 0
right = combined.width - 50  # 调整这个值以决定裁剪多少
bottom = combined.height

# 裁剪图像
cropped_combined = combined.crop((left, top, right, bottom))

# 保存裁剪后的图像
out_path_cropped = os.path.join(OUTPUT_DIR, "002_fixed_cropped.png")
cropped_combined.save(out_path_cropped, dpi=(140, 140))
print(f"✅ 裁剪完成: {out_path_cropped}")

# 关闭所有打开的图像文件以释放资源
cropped_combined.close()
combined.close()
