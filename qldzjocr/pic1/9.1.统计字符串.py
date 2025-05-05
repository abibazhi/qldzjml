import sys

def count_specific_string(file_path, search_string):
    """计算文件中包含特定字符串的行数"""
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return sum(search_string in line for line in file)
    except FileNotFoundError:
        print(f"文件 {file_path} 未找到，请检查路径是否正确。")
        return None

def main():
    # 检查是否有正确的命令行参数
    if len(sys.argv) != 3:
        print("用法: python 脚本名.py 文件路径 搜索字符串")
        sys.exit(1)

    file_path = sys.argv[1]  # 第一个参数是文件路径
    search_string = sys.argv[2]  # 第二个参数是搜索字符串
    
    result = count_specific_string(file_path, search_string)

    if result is not None:
        print(f"在文件 {file_path} 中共有 {result} 行包含 \"{search_string}\".")

if __name__ == "__main__":
    main()
