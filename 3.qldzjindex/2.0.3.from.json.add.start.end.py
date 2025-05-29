import json

def add_start_and_end_fields(input_path, output_path):
    with open(input_path, 'r', encoding='utf-8') as f:
        books = json.load(f)

    for i in range(len(books)):
        book = books[i]

        path = book['path']
        path_parts = path.split('/')

        # 确保路径格式正确，提取册号和页号
        if len(path_parts) < 2:
            book['start'] = ''
            book['end'] = ''
            continue

        # 提取册号和页号（从后往前取）
        page_str = path_parts[-1]
        vol_str = path_parts[-2]

        # 构造 start 字段：三位数格式
        start_vol = vol_str.zfill(3)
        start_page = page_str.zfill(3)
        book['start'] = f"{start_vol}.{start_page}"

        # 构造 end 字段：等于下一本书的 start - 1
        if i < len(books) - 1:
            next_book = books[i + 1]
            next_path_parts = next_book['path'].split('/')
            if len(next_path_parts) >= 2:
                next_vol_str = next_path_parts[-2]
                next_page_str = next_path_parts[-1]
                try:
                    next_vol = int(next_vol_str)
                    next_page = int(next_page_str)
                    prev_page = next_page - 1
                    if prev_page <= 0:
                        end_vol = "000"
                        end_page = "000"
                    else:
                        end_vol = f"{next_vol:03d}"
                        end_page = f"{prev_page:03d}"
                    book['end'] = f"{end_vol}.{end_page}"
                except ValueError:
                    book['end'] = ''
            else:
                book['end'] = ''
        else:
            # 最后一本书
            book['end'] = '000.000'

    # 写入新的 JSON 文件
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(books, f, ensure_ascii=False, indent=4)

    print(f"✅ 已成功生成包含 start 和 end 的书籍列表文件：{output_path}")

# 使用示例
input_json = '2.0.2.json'
output_json = 'books_with_pages.json'
add_start_and_end_fields(input_json, output_json)
