# 定义输出文件名
output_file="cleaned_image_metadata.txt"

# 使用awk去除重复行并保存到新的文件中
awk '!seen[$0]++' image_metadata.txt > "$output_file"

echo "已生成去重后的元数据文件: $output_file"
