def ordered_fuzzy_match(astr, bstr):
    # 初始化匹配字符的计数器
    match_count = 0
    # 初始化 bstr 的索引
    b_index = 0
    # 遍历 astr 中的每个字符
    for char in astr:
        # 从 bstr 的当前索引位置开始查找匹配字符
        while b_index < len(bstr):
            if bstr[b_index] == char:
                # 找到匹配字符，计数器加 1
                match_count += 1
                # 更新 bstr 的索引，继续往后查找
                b_index += 1
                break
            # 没找到匹配字符，继续移动 bstr 的索引
            b_index += 1
    return match_count

astr = "a1b2c3d4e5f"
bstr = "adfasdfasdf"
result = ordered_fuzzy_match(astr, bstr)
print(f"匹配的字符数量为: {result}")
