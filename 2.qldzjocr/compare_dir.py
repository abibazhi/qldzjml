import os

def get_files_in_directory(directory):
    """获取指定目录下的所有文件名"""
    return set(os.listdir(directory))

def compare_directories(dir1, dir2):
    """比较两个目录中的文件名"""
    files_dir1 = get_files_in_directory(dir1)
    files_dir2 = get_files_in_directory(dir2)

    # 找出dir1中有但dir2中没有的文件
    only_in_dir1 = files_dir1 - files_dir2
    # 找出dir2中有但dir1中没有的文件
    only_in_dir2 = files_dir2 - files_dir1

    return only_in_dir1, only_in_dir2

def main():
    dir1 = './selected_images'
    dir2 = './selected_images1'

    only_in_dir1, only_in_dir2 = compare_directories(dir1, dir2)

    if only_in_dir1:
        print(f"仅在 {dir1} 目录下的文件:")
        for file in only_in_dir1:
            print(file)
    else:
        print(f"{dir1} 目录下的文件都存在于 {dir2}")

    if only_in_dir2:
        print(f"\n仅在 {dir2} 目录下的文件:")
        for file in only_in_dir2:
            print(file)
    else:
        print(f"{dir2} 目录下的文件都存在于 {dir1}")

if __name__ == "__main__":
    main()
