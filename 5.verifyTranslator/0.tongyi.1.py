# -*- coding: utf-8 -*-
import openpyxl

def extract_page_numbers(filename):
    """从图片文件名提取页码，如 qldzjpng_001_165.png -> '001165'"""
    if not filename or not isinstance(filename, str):
        return None
    name = filename.replace('.png', '').replace('.jpg', '').replace('.jpeg', '')
    parts = name.split('_')
    if len(parts) >= 3:
        try:
            prefix = parts[1]
            suffix = parts[2]
            return f"{prefix}{suffix}"
        except:
            return None
    return None

def is_special_row(row_data):
    """
    判断是否为“特殊行”：仅第二列（经名）有内容，其余为空
    row_data: [编号, 经名, 译者, 文件名]
    """
    编号, 经名, 译者, 文件名 = row_data
    # 所有字段转为空字符串处理
    编号 = 编号.strip() if 编号 else ""
    经名 = 经名.strip() if 经名 else ""
    译者 = 译者.strip() if 译者 else ""
    文件名 = 文件名.strip() if 文件名 else ""
    # 特殊行：只有经名有内容
    return not 编号 and 经名 and not 译者 and not 文件名

def main():
    input_file = './translator.1.大模型验证结果.核对.再加经名.手工核对译者.形式化.xlsx'
    output_file = './output.html'

    try:
        wb = openpyxl.load_workbook(input_file)
        ws = wb.active
    except Exception as e:
        print(f"无法读取Excel文件: {e}")
        return

    rows = []
    for row in ws.iter_rows(values_only=True):
        # ✅ 关键修复：只取前4列，避免列数过多
        cleaned_row = []
        for cell in row[:4]:  # 只取前4列
            value = "" if cell is None else str(cell).strip()
            cleaned_row.append(value)
        # 如果不足4列，补空字符串
        while len(cleaned_row) < 4:
            cleaned_row.append("")
        rows.append(cleaned_row)

    # 过滤有效行
    data = []
    for row in rows:
        编号, 经名, 译者, 文件名 = row
        # 如果有编号 或 能提取文件名页码，或为特殊行，则保留
        if 编号.isdigit() or extract_page_numbers(文件名) or is_special_row(row):
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

    # 收集特殊行锚点
    special_anchors = []
    for i, row in enumerate(data):
        if is_special_row(row):
            anchor_id = f"anchor_{i}"
            special_anchors.append(f'<a href="#{anchor_id}">{row[1]}</a>')

    # 输出跳转链接
    if special_anchors:
        html_lines.append('    <div class="special-anchor">')
        html_lines.append('        快速跳转: ' + ' | '.join(special_anchors))
        html_lines.append('    </div>')
        html_lines.append('')

    # 开始表格
    html_lines.append('    <table>')

    # 生成每一行
    for i, row in enumerate(data):
        编号, 经名, 译者, 文件名 = row

        # ✅ 关键修复：传整行给 is_special_row
        if is_special_row(row):
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

        if i < len(data) - 1:
            next_start = extract_page_numbers(data[i+1][3])
            if next_start:
                end_value = str(int(next_start) - 1).zfill(6)
            else:
                end_value = "999999"
        else:
            end_value = "999999"

        link = f'sutra.html?start={start_value}&end={end_value}'
        经名_link = f'<a href="{link}">{经名}</a>'

        html_lines.append('        <tr>')
        html_lines.append(f'            <td>{编号}</td>')
        html_lines.append(f'            <td>{经名_link}</td>')
        html_lines.append(f'            <td>{译者}</td>')
        html_lines.append('        </tr>')

    html_lines.append('    </table>')
    html_lines.append('</body>')
    html_lines.append('</html>')

    # 写入文件
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write('\n'.join(html_lines))
        print(f"✅ 成功生成 HTML 文件: {output_file}")
    except Exception as e:
        print(f"❌ 写入文件失败: {e}")

if __name__ == '__main__':
    main()
