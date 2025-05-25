import os
import fitz  # PyMuPDF
from PIL import Image

def tiff_to_pdf(tiff_path):
    """ 将单个 TIFF 文件转换为 PDF 文件 """
    pdf_path = tiff_path.replace('.tiff', '.pdf').replace('.tif', '.pdf')
    images = Image.open(tiff_path)
    pdf_bytes = img2pdf.convert(images.filename)
    file_path = os.path.join(os.path.dirname(tiff_path), pdf_path)
    with open(file_path, "wb") as f:
        f.write(pdf_bytes)
    return file_path

def merge_tiffs_to_pdf(directory):
    """ 合并目录下所有 TIFF 文件为一个 PDF 文件 """
    output_pdf_path = os.path.join(directory, "merged_output.pdf")
    doc = fitz.open()

    # 获取目录下所有 .tiff 或 .tif 文件，并按文件名排序
    tiff_files = [f for f in os.listdir(directory) if f.endswith('.tiff') or f.endswith('.tif')]
    tiff_files.sort()

    for tiff_file in tiff_files:
        tiff_path = os.path.join(directory, tiff_file)
        # 使用Pillow打开TIFF文件
        image = Image.open(tiff_path)
        # 将每一页TIFF图像转换为PDF字节流
        pdf_bytes = image.tobytes("pdf", resolution=150)
        # 打开临时PDF
        temp_pdf = fitz.open("pdf", pdf_bytes)
        # 将PDF页面插入到输出文档
        doc.insert_pdf(temp_pdf)
    
    # 输出合并后的PDF文件
    doc.save(output_pdf_path)
    doc.close()
    print(f"PDF created at: {output_pdf_path}")

# 替换为你自己的目录路径
directory_path = '/mnt/d/qldzjtiff/038'
merge_tiffs_to_pdf(directory_path)
