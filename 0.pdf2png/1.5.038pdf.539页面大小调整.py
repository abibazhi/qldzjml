import os
from PIL import Image
from PyPDF2 import PdfReader, PdfWriter

def tiff_to_pdf_page(tiff_path, target_pdf_path, page_num):
    """将 TIFF 图片转换为与目标PDF页面大小相匹配的PDF页面"""
    # 获取目标PDF页面尺寸
    with open(target_pdf_path, 'rb') as pdf_file:
        reader = PdfReader(pdf_file)
        page = reader.pages[page_num - 1]  # 注意：页码从1开始
        pdf_width = float(page.mediabox.width)
        pdf_height = float(page.mediabox.height)

    img = Image.open(tiff_path).convert('L')  # 将图像转换为灰度图像
    img = img.point(lambda x: 0 if x < 128 else 255, '1')  # 转换为二值图像
    
    img_ratio = img.width / img.height
    pdf_ratio = pdf_width / pdf_height
    
    # 根据宽高比调整图片大小
    if img_ratio > pdf_ratio:
        new_width = int(pdf_width)
        new_height = int(pdf_width / img_ratio)
    else:
        new_width = int(pdf_height * img_ratio)
        new_height = int(pdf_height)
    
    # 调整图片大小
    img_resized = img.resize((new_width, new_height), Image.BILINEAR)
    
    # 创建一个白色背景图像，并将调整大小后的图像粘贴到中心
    background = Image.new('L', (int(pdf_width), int(pdf_height)), 255)  # 使用'L'模式创建白色背景
    paste_x = int((background.width - img_resized.width) / 2)
    paste_y = int((background.height - img_resized.height) / 2)
    background.paste(img_resized, (paste_x, paste_y))

    pdf_path = os.path.splitext(tiff_path)[0] + '.pdf'
    background.save(pdf_path, "PDF", resolution=300, save_all=False)
    return pdf_path


def insert_and_replace_pdf_page(pdf_path, page_num, new_page_path):
    """插入新页面并替换指定位置的页面"""
    pdf_reader = PdfReader(pdf_path)
    pdf_writer = PdfWriter()

    # 添加指定位置之前的页面
    for index in range(page_num - 1):
        page = pdf_reader.pages[index]
        pdf_writer.add_page(page)

    # 添加新的页面
    new_pdf_reader = PdfReader(new_page_path)
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

    # 将 TIFF 图片转换为与目标PDF页面大小相匹配的PDF页面
    new_page_pdf = tiff_to_pdf_page(tiff_file, pdf_file, page_number)

    # 插入新页面并替换指定位置的页面
    replaced_pdf = insert_and_replace_pdf_page(pdf_file, page_number, new_page_pdf)

    print(f"已成功将 {tiff_file} 插入到 {pdf_file} 的第 {page_number} 页位置，新文件保存为 {replaced_pdf}")

    # 删除临时生成的 PDF 页面文件
    os.remove(new_page_pdf)
