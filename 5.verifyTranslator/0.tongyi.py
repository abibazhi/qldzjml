# -*- coding: utf-8 -*-
import openpyxl
from openpyxl.utils import cell

def extract_page_numbers(filename):
    """从图片文件名提取页码，如 qldzjpng_001_165.png -> '001165'"""
    if not filename or not isinstance(filename, str):
        return None
    # 去掉扩展名
    name = filename.replace('.png', '').replace('.jpg', '').replace('.jpeg', '')
    parts = name.split('_')
    if len(parts) >= 3:
        try:
            prefix = parts[1]  # 001
            suffix = parts[2]  # 165
            return f"{prefix}{suffix}"
        except:
            return None
    return None

def is_special_row(row_data):
    """
    判断是否为“特殊行”：仅第二列（经名）有内容，其余内容列为空
    这里假设：编号为空，译者为空，文件名为空 → 特殊行
    """
    编号, 经名, 译者, 文件名 = row_data
    return not 编号 and 经名 and not 译者 and not 文件名

def main():
    # 输入和输出文件
    input_file = 'translator.1.大模型验证结果.核对.再加经名.手工核对译者.形式化.xlsx'   # 修改为您的文件名
    output_file = 'output.html' # 输出HTML文件名

    # 加载Excel工作簿
    try:
        wb = openpyxl.load_workbook(input_file)
        ws = wb.active
    except Exception as e:
        print(f"无法读取Excel文件: {e}")
        return

    rows = []
    for row in ws.iter_rows(values_only=True):
        # 只取前4列：编号, 经名, 译者, 文件名
        row = list(row[:4])
        # 填充缺失列
        while len(row) < 4:
            row.append(None)
        # 转换 None 为 空字符串
        row = ['' if cell is None else str(cell).strip() for cell in row]
        rows.append(row)

    # 过滤掉纯标题行（如“大乘般若部”），只保留有效数据
    data = []
    for row in rows:
        编号, 经名, 译者, 文件名 = row
        # 如果编号是数字或可转为数字，认为是有效数据行
        if 编号.isdigit() or extract_page_numbers(文件名):
            data.append(row)
        elif is_special_row(row):
            # 特殊行也保留
            data.append(row)

    # 生成HTML
    html_lines = []
    html_lines.append('<!DOCTYPE html>')
    html_lines.append('<html lang="zh">')
    html_lines.append('<head>')
    html_lines.append('    <meta charset="UTF-8">')
    html_lines.append('    <title>佛经目录</title>')
    html_lines.append('    <style>')
    html_lines.append('        table { border-collapse: collapse; width: 100%; }')
    html_lines.append('        td, th { border: 1px solid #ddd; padding: 8px; text-align: left; }')
    html_lines.append('        .special-anchor { margin-bottom: 10px; font-weight: bold; }')
    html_lines.append('    </style>')
    html_lines.append('</head>')
    html_lines.append('<body>')
    html_lines.append('')

    # 收集特殊行锚点
    special_anchors = []

    # 第一遍：收集特殊行
    for i, row in enumerate(data):
        if is_special_row(row):
            经名 = row[1]
            anchor_id = f"anchor_{i}"
            special_anchors.append(f'<a href="#{anchor_id}">{经名}</a>')

    # 输出特殊行跳转链接（如果有的话）
    if special_anchors:
        html_lines.append('    <div class="special-anchor">')
        html_lines.append('        快速跳转: ' + ' | '.join(special_anchors))
        html_lines.append('    </div>')
        html_lines.append('')

    # 开始表格
    html_lines.append('    <table>')

    # 第二遍：生成表格行
    for i, row in enumerate(data):
        编号, 经名, 译者, 文件名 = row

        # 处理特殊行
        if is_special_row(经名):
            anchor_id = f"anchor_{i}"
            html_lines.append(f'        <tr id="{anchor_id}">')
            html_lines.append(f'            <td></td>')
            html_lines.append(f'            <td colspan="2"><strong>{经名}</strong></td>')
            html_lines.append('        </tr>')
            continue

        # 正常数据行
        start_value = extract_page_numbers(文件名)
        if not start_value:
            print(f"警告：第 {i+1} 行图片文件名格式错误: {文件名}")
            start_value = "000000"

        # 计算 end_value：下一行的 start - 1
        if i < len(data) - 1:
            next_start = extract_page_numbers(data[i+1][3])
            if next_start:
                end_value = str(int(next_start) - 1).zfill(6)
            else:
                end_value = "999999"  # 默认
        else:
            end_value = "999999"  # 最后一行

        # 生成链接
        link = f'sutra.html?start={start_value}&end={end_value}'
        经名_link = f'<a href="{link}">{经名}</a>'

        # 构造表格行
        html_lines.append('        <tr>')
        html_lines.append(f'            <td>{编号}</td>')
        html_lines.append(f'            <td>{经名_link}</td>')
        html_lines.append(f'            <td>{译者}</td>')
        html_lines.append('        </tr>')

    html_lines.append('    </table>')
    html_lines.append('')
    html_lines.append('</body>')
    html_lines.append('</html>')

    # 写入HTML文件
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write('\n'.join(html_lines))
        print(f"✅ 成功生成 HTML 文件: {output_file}")
    except Exception as e:
        print(f"❌ 写入文件失败: {e}")

if __name__ == '__main__':
    main()
