# test_cases.py
"""
所有测试用例的统一定义
"""

TEST_CASES = [
    {
        "id": "T5-metadata-consistency",
        "sutra_number": 5,
        "title": "道行般若波罗蜜经",
        "expected_author": "晋襄阳释道安撰",
        "note": "以现代整理本目录为准，接受‘道安撰’为正确署名，非‘支娄迦谶译’",
        "field": "author",
        "type": "metadata-consistency"
    },
    {
        "id": "T30-translator-correct",
        "sutra_number": 30,
        "title": "佛说法镜经",
        "expected_author": "后汉安息国优婆塞安玄共沙门严佛调译",
        "note": "封面与序误标为康僧会撰，但目录与正文一致为此译者，以目录为准",
        "field": "author",
        "type": "metadata-consistency"
    },
    {
        "id": "T85-format-separate",
        "sutra_number": 85,
        "title": "大方广佛华严经普贤菩萨行愿品",
        "expected_author": "唐罽宾国三藏般若奉诏译",
        "note": "经名与译者应分开，不可合并为一行",
        "field": "format",
        "type": "format-issue"
    },
    {
        "id": "T115-no-today",
        "sutra_number": 115,
        "title": "佛说方等泥洹经",
        "expected_author": "失译人名附东晋录",
        "forbidden_chars": ["今"],
        "note": "译者信息中不得出现‘今’字，如‘今人整理’等",
        "field": "author",
        "type": "text-validation"
    },
    {
        "id": "T128-must-end-with-yi",
        "sutra_number": 128,
        "title": "不一定入定入印经",
        "expected_author": "元魏婆罗门瞿昙般若流支译",
        "must_end_with": "译",
        "should_not_be": "元魏婆罗门瞿昙般若流支",
        "note": "译者信息必须以‘译’结尾，不可省略",
        "field": "author",
        "type": "text-completeness"
    },
    {
        "id": "T137-no-foshuo-prefix",
        "sutra_number": 137,
        "title": "缘生初胜分法本经",
        "expected_title": "缘生初胜分法本经",
        "forbidden_prefix": "佛说",
        "note": "此经名不应加‘佛说’前缀",
        "field": "title",
        "type": "title-validation"
    },
    {
        "id": "T175-character-accuracy",
        "sutra_number": 175,
        "title": "大萨遮尼乾子受记经",
        "expected_title": "大萨遮尼乾子受记经",
        "forbidden_char": "干",
        "required_char": "乾",
        "note": "‘乾’为专有字符，不可简化为‘干’",
        "field": "title",
        "type": "character-accuracy"
    },
    {
        "id": "T195-source-fidelity",
        "sutra_number": 195,
        "title": "称赞净土佛摄受经",
        "expected_author": "唐三藏法师玄奘奉诏译",
        "note": "封面图片缺‘诏译’，但应以目录为准，补全信息",
        "field": "author",
        "type": "source-fidelity"
    },
    {
        "id": "T212-special-structure",
        "sutra_number": 212,
        "title": "菩萨睒子经一卷",
        "cover_label": "五经同卷",
        "has_individual_cover": False,
        "note": "该经与其他四部合为一卷，封面仅标‘五经同卷’，无独立经名与译者",
        "field": "structure",
        "type": "special-structure"
    }
]
