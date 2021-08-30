import sys, os
from PIL import Image, ImageDraw
from PyPDF2 import PdfFileReader
from itertools import product
from collections import defaultdict
box_indices = list(product(range(3), range(10)))
constants = defaultdict(lambda : (51, 83, 377, 147))
constants[2] = (51, 100, 377, 147)

# x_offset, y_offset, x_width, y_height = 51, 100, 377, 147

def extract_image_from_pdf_page(p):
    img = next(iter(p.get('/Resources').get('/XObject').values())).getObject()
    assert img['/BitsPerComponent'] == 8
    assert img['/Filter'] == '/FlateDecode'
    assert img['/ColorSpace'] == '/DeviceRGB'
    assert img['/Width'] == 1241
    assert img['/Height'] == 1753
    img = Image.frombytes('RGB', (1241,1753), img.getData())
    return img


def card_extractor(input_pdf_path, output_dir):
    f = PdfFileReader(open(input_pdf_path, 'rb'))
    n = f.getNumPages()
    # assume that voter info is present from page 3 to second last page.
    # getPage function is zero indexed.
    cards = []
    for k in range(2, n-1):
        img = extract_image_from_pdf_page(f.getPage(k))
        x_offset, y_offset, x_width, y_height = constants[k]
        for (i, j) in box_indices:
            left, upper = (x_offset + i * x_width), (y_offset + j * y_height)
            right, lower = left + x_width, upper + y_height
            # print(k, i, j, left, upper, right, lower)
            card = img.crop(box=(left, upper, right, lower))
            cards.append([card, k, i, j, upper, lower])
            card.save(os.path.join(output_dir, f'{k}_{i}_{j}.jpeg'), format='jpeg', dpi=[100,100])
    
    return cards 

input_pdf_path = sys.argv[1] 
output_dir = sys.argv[2]
cards = card_extractor(input_pdf_path, output_dir)
