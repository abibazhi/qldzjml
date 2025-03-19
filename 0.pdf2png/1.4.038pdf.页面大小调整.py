import os
from PyPDF2 import PdfReader, PdfWriter

def set_page_size_to_a4(pdf_path):
    """将PDF文件的所有页面设置为A4大小"""
    a4_width = 210 * 2.835
    a4_height = 297 * 2.835

    pdf_reader = PdfReader(pdf_path)
    pdf_writer = PdfWriter()

    for page in pdf_reader.pages:
        # 设置页面大小为A4
        page.mediabox.lower_left = (0, 0)
        page.mediabox.lower_right = (a4_width, 0)
        page.mediabox.upper_left = (0, a4_height)
        page.mediabox.upper_right = (a4_width, a4_height)
        pdf_writer.add_page(page)

    # 保存修改后的PDF文件
    output_pdf_path = os.path.splitext(pdf_path)[0] + '_a4.pdf'
    with open(output_pdf_path, 'wb') as output_file:
        pdf_writer.write(output_file)

    return output_pdf_path

if __name__ == "__main__":
    current_dir = os.getcwd()
    pdf_file = os.path.join(current_dir, '038.pdf')
    set_page_size_to_a4(pdf_file)
