#!/usr/bin/env python3
import struct, sys, io
from PIL import Image

# 参数：文件 宽 高 dpi_x dpi_y
file, w, h, dpi = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4])

with open(file, 'rb') as f:
    data = f.read()

# 1. 构造最小 TIFF 头（仅 5 个必需标签）
ifd_off = 8
tiff = bytearray()
tiff.extend(b'II\x2a\x00')                              # 字节序 + 版本
tiff.extend(struct.pack('<I', ifd_off))                 # IFD 偏移
# IFD
tiff.extend(struct.pack('<H', 5))                       # 条目数 5
tiff.extend(struct.pack('<HHII', 256, 4, 1, w))        # ImageWidth
tiff.extend(struct.pack('<HHII', 257, 4, 1, h))        # ImageLength
tiff.extend(struct.pack('<HHII', 259, 3, 1, 4))        # Compression = G4
tiff.extend(struct.pack('<HHII', 273, 4, 1, 8+2+5*12+4))  # StripOffsets
tiff.extend(struct.pack('<HHII', 279, 4, 1, len(data))) # StripByteCounts
tiff.extend(b'\x00\x00\x00\x00')                        # IFD 结束
tiff.extend(data)                                       # CCITT 裸流

# 2. Pillow 打开并转 PNG
img = Image.open(io.BytesIO(tiff))
img.save('page-000.png', dpi=(dpi, dpi))
print('→ page-000.png')
