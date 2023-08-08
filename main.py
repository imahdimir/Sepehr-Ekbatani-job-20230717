"""

    """

import zlib
import re
from pathlib import Path

def extract_data(pdf , offset) :
    """ extract the encoded Cmap from offset in the pdf file """

    start_block = pdf[offset + 10 :pdf.find(b'\x52' , offset)]
    start_block = pdf.find(start_block , 0)
    start_block = pdf.find(b'\x78' , start_block)

    end_block = pdf.find(b'\x65\x6E\x64' , start_block)

    return start_block , pdf[start_block : end_block] , end_block

def find_all_to_unicode(pdf) :
    """ find all the encoded Cmap in the pdf """
    return re.finditer(b'\x54\x6F\x55\x6E\x69\x63\x6F\x64\x65' , pdf)

def extract_all_data(pdf) :
    _all = find_all_to_unicode(pdf)
    return [extract_data(pdf , x.start()) for x in _all]

def decode_all_data(encoded_cmaps: list[tuple]) :
    return [zlib.decompress(x[1]).decode('utf-8') for x in encoded_cmaps]

def extract_and_decode_all_data(pdf) :
    return decode_all_data(extract_all_data(pdf))

def replace_cmaps(pdf , new_cmaps: list[str]) :
    """ replace the old Cmap with the new Cmap in the pdf file """

    # find how many Cmap are in the pdf file
    x = find_all_to_unicode(pdf)

    # replace the old Cmap with the new Cmap
    for _i in range(len(list(x))) :
        ecmp = extract_all_data(pdf)
        ecmp = ecmp[_i]

        print(ecmp[0] , ecmp[2])

        # compress the new Cmap
        ncomp = zlib.compress(new_cmaps[_i].encode())

        # replace the old Cmap with the new Cmap in the pdf file
        pdf = pdf[: ecmp[0]] + ncomp + pdf[ecmp[2] :]

        print(pdf[ecmp[0] : ecmp[0] + 40])

    return pdf

def main() :
    pass

    ##
    with open('2.pdf' , 'rb') as f :
        pdf = f.read()

    extract_and_decode_all_data(pdf)

    ##
    x = extract_and_decode_all_data(pdf)
    print(x)
    print(len(x))

    ##
    for i in range(len(x)) :
        with open(f't_{i}.txt' , 'w') as f :
            f.write(x[i])

    ##
    with open('1.pdf' , 'rb') as f :
        pdf1 = f.read()

    m = re.finditer(b'\x54\x6F\x55\x6E\x69\x63\x6F\x64\x65' , pdf1)

    for el in m :
        print(el.start())

    ##
    extract_data(pdf1 , 2237937)

    ##
    extract_all_data(pdf1)

    ##
    x = extract_and_decode_all_data(pdf1)
    print(x)

    print(len(x))

    ##
    with open('2.pdf' , 'rb') as f :
        pdf1 = f.read()

    x = extract_all_data(pdf1)

    for i in range(1) :
        with open(f't1.txt' , 'r') as f :
            t1 = f.read()

        p1 = replace_cmaps(pdf1 , [t1] * len(x))

        with open(f'2r.pdf' , 'wb') as f :
            f.write(p1)

    ##
    from pdfreader import PDFDocument

    with open('1.pdf' , 'rb') as f :
        doc = PDFDocument(f.read())

    ##
    from itertools import islice

    page = next(islice(doc.pages() , 0 , 1))

    ##
    page.Resources.Font.keys()

    ##
    type(page.Resources.Font.F1)

    ##
    x = page.Resources.Font.F1
    x

    ##
    x = page.Resources.Font.F1.FontDescriptor.CharSet
    x.decode('utf-8')

    ##
    ch = x.CharSet

    ##

    ##
    from pdfreader import PDFDocument
    from itertools import islice

    with open('1.pdf' , 'rb') as f :
        doc = PDFDocument(f.read())

    page = next(islice(doc.pages() , 5 , 6))

    ##
    page.Resources.Font.keys()

    ##
    page.Resources.Font.C2_0

    ##
    tuc = page.Resources.Font.C2_0.ToUnicode

    ##
    tuc.filtered

    with open('t2.txt' , 'wb') as fi :
        fi.write(tuc.filtered)

    ##

    ##

    ##
    cmap = page.Resources.Font.F1.ToUnicode

    ##
    dat = cmap.filtered

    ##

    ##
    dat

    ##
    from pdfreader import SimplePDFViewer

    with open('2.pdf' , "rb") as fi :
        fd = fi.read()

    viewer = SimplePDFViewer(fd)
    viewer.render()

    ##
    markdown = viewer.canvas.text_content
    markdown

    ##
    viewer.canvas.text_content

    ##
    for i , ky in enumerate(page.Resources.Font.keys()) :
        print(ky)
        font = page.Resources.Font[ky]
        font.Subtype , bool(font.ToUnicode)

        cmap = font.ToUnicode
        if not cmap :
            continue

        print(cmap.filtered)

        with open(f't_{i}.txt' , 'wb') as f :
            f.write(cmap.filtered)

    ##
    c1 = "h"
    c2 = 'ﻖ'

    x1 = ord(c1)
    print(hex(x1) , x1)
    x2 = ord(c2)
    print(hex(x2) , x2)

    st0 = '<'.strip() + '0' * (6 - len(str(hex(x1)))) + str(hex(x1))[
                                                        2 :].strip() + '> <' + '0' * (
                  6 - len(str(hex(x2)))) + str(hex(x2))[2 :].strip() + '>'
    print(st0)

    ##
    for ky , vl in bc.items() :
        if vl[0] == 'u' :
            print(chr(int(f'0x{vl[1 :]}' , 16)) , vl)

    ##
    from fontTools.ttLib import TTFont

    font = TTFont('B Titr Bold.ttf')

    bc = font.getBestCmap()
    bc

    ##
    for ky , vl in bc.items() :
        print('<' , str(hex(ky))[2 :].strip() , '> <' , vl[2 :] , '>')

    ##
    for ky , vl in bc.items() :
        if vl[0] == 'u' :
            print(chr(int(f'0x{vl[1 :]}' , 16)) , vl)

    ##
    font.getReverseGlyphMap()

    ##
    font.getGlyphOrder()

    ##
    font.buildReversed()

    ##
    font.getBestCmap()

    ##
    from pypdf import PdfReader

    reader = PdfReader("2.pdf")
    number_of_pages = len(reader.pages)
    page = reader.pages[0]
    text = page.extract_text()

    text

    ##

    ##

    ##

    ##
    from fitz import Document

    doc = Document('1.pdf')

    ##
    pg = doc.load_page(5)

    ft = pg.get_fonts(full = True)

    ft

    ##
    name , ext , _ , content = doc.extract_font(918)

    with open(name + "." + ext , 'wb') as fi :
        fi.write(content)

    ##
    pg

    ##
    from fitz import Font

    font = Font(fontfile = 'AAAAAM+BRoyaBold.cff')

    font

    ##
    font.valid_codepoints()

    ##

    ##
    vuc = font.valid_codepoints()

    for i in vuc :
        print("%04X %s (%s)" % (i , chr(i) , font.unicode_to_glyph_name(i)))

    ##
    font.flags

    ##
    font.glyph_count

    ##
    font.is_writable

    ##
    font.valid_codepoints()

    ##
    font.unicode_to_glyph_name(134)

    ##
    font.ascender

    ##
    font.descender

    ##
    font.glyph_count

    ##

    ##

    ##
    from fitz import Document

    doc = Document('2.pdf')

    ##
    pg = doc[0]

    ##
    pg.get_text()

    ##
    r = pg.get_text()
    with open('t.txt' , 'w') as f :
        f.write(r)

    ##

    ##

    ##

    ##

    ##

    ##

##


if __name__ == "__main__" :
    main()
    print(f'{Path(__file__).name} Done!')

##


def test() :
    pass

    ##

    ##
