import os
from PIL import Image
import PyPDF2


def tiff_to_pdf_page(tiff_path):
    """将 TIFF 图片转换为 300 dpi 的 PDF 页面"""
    img = Image.open(tiff_path)
    img.info['dpi'] = (300, 300)
    pdf_path = os.path.splitext(tiff_path)[0] + '.pdf'
    img.save(pdf_path, "pdf", save_all=False)
    return pdf_path


def insert_and_replace_pdf_page(pdf_path, page_num, new_page_path):
    """插入新页面并替换指定位置的页面"""
    pdf_reader = PyPDF2.PdfReader(pdf_path)
    pdf_writer = PyPDF2.PdfWriter()

    # 添加指定位置之前的页面
    for index in range(page_num - 1):
        page = pdf_reader.pages[index]
        pdf_writer.add_page(page)

    # 添加新的页面
    new_pdf_reader = PyPDF2.PdfReader(new_page_path)
    new_page = new_pdf_reader.pages[0]
    pdf_writer.add_page(new_page)

    # 添加指定位置之后的页面
    for index in range(page_num, len(pdf_reader.pages)):
        page = pdf_reader.pages[index]
        pdf_writer.add_page(page)

    # 保存修改后的 PDF 文件
    output_pdf_path = os.path.splitext(pdf_path)[0] + '_replaced.pdf'
    with open(output_pdf_path, 'wb') as output_file:
        pdf_writer.write(output_file)

    return output_pdf_path


if __name__ == "__main__":
    current_dir = os.getcwd()
    pdf_file = os.path.join(current_dir, '038.pdf')
    tiff_file = os.path.join(current_dir, '539.tiff')
    page_number = 539  # 要替换的页码

    # 将 TIFF 图片转换为 300 dpi 的 PDF 页面
    new_page_pdf = tiff_to_pdf_page(tiff_file)

    # 插入新页面并替换指定位置的页面
    replaced_pdf = insert_and_replace_pdf_page(pdf_file, page_number, new_page_pdf)

    print(f"已成功将 {tiff_file} 插入到 {pdf_file} 的第 {page_number} 页位置，新文件保存为 {replaced_pdf}")

    # 删除临时生成的 PDF 页面文件
    os.remove(new_page_pdf)
