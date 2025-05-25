from PIL import Image
import os

def combine_tiff_to_pdf(folder_path, pdf_file_path):
    # 获取指定文件夹中的所有文件
    files = os.listdir(folder_path)
    # 筛选出TIFF图片文件
    tiff_files = [os.path.join(folder_path, file) for file in files if file.lower().endswith('.tiff')]
    # 按文件名排序
    tiff_files.sort()
    total_images = len(tiff_files)

    if total_images == 0:
        print("未找到TIFF图片文件。")
        return

    # 处理第一张图片
    print(f"正在处理图片 1/{total_images}")
    first_image = Image.open(tiff_files[0])
    output = first_image
    tiff_files.pop(0)
    sources = []

    # 处理其余图片
    for index, file in enumerate(tiff_files, start=2):
        print(f"正在处理图片 {index}/{total_images}")
        img = Image.open(file)
        sources.append(img)

    # 保存为PDF文件
    print("正在保存为PDF文件...")
    output.save(pdf_file_path, "pdf", save_all=True, append_images=sources)
    print(f"PDF文件已保存至 {pdf_file_path}")

if __name__ == "__main__":
    folder = r"/mnt/d/qldzjtiff/038"  # 替换为你的TIFF图片文件夹路径
    pdfFile = r"output.pdf"  # 替换为你想要的输出PDF文件路径
    combine_tiff_to_pdf(folder, pdfFile)
