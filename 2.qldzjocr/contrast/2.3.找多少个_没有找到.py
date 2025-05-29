def count_specific_string(file_path, search_string):
    """计算文件中包含特定字符串的行数"""
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return sum(search_string in line for line in file)
    except FileNotFoundError:
        print(f"文件 {file_path} 未找到，请检查路径是否正确。")
        return None

# 使用方法：
file_path = './refined_comparison_result.txt'  # 您要检查的txt文件的路径
file_path = './filtered_comparison_result.txt'

search_string = "没有找到"
result = count_specific_string(file_path, search_string)

if result is not None:
    print(f"在文件 {file_path} 中共有 {result} 行包含 \"{search_string}\".")
