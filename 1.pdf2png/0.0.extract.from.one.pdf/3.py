import os, re, glob
from PIL import Image

for ccitt in glob.glob('*.ccitt'):
    base = os.path.splitext(ccitt)[0]
    with open(base+'.params') as p:
        w = int(re.search(r'-x (\d+)', p.read()).group(1))
    img = Image.open(ccitt)
    img.save(base+'.png')
