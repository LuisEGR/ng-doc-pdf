import codecs
import pdfkit
import os
import glob
import json
from pathlib import Path
from PyPDF2 import PdfFileMerger
from tqdm import tqdm

modulosIncluidos = open('modulos.json', 'r')
modulosIncluidos = json.load(modulosIncluidos)


pre_html = '<html><head><meta charset="utf-8">'
pre_html += '<script>\n'
pre_html += open('prettify.js', 'r').read()
pre_html += '</script>'
pre_html += '<style>.break-before {page-break-before: always;}'
pre_html += 'table, tr, td, th, tbody, thead, tfoot,li { page-break-inside: avoid !important;}</style>'
pre_html += '<style>'
pre_html += open('bootstrap.min.css', 'r').read().encode('utf-8')
pre_html += open('prettify.css', 'r').read().encode('utf-8')
pre_html += open('docs.css', 'r').read().encode('utf-8')
pre_html += '</style></head><div class="content">'

myDir = 'partials'
files = {}
pbar = tqdm(total=len(modulosIncluidos), unit='Mods')
mergerSprint = PdfFileMerger()
for modName in modulosIncluidos:
    files[modName] = []
    for root, dirnames, filenames in os.walk(myDir):
        files[modName].extend(glob.glob(root + "/" + modName +"*.html"))
    files[modName] = sorted(files[modName], reverse=True)

    for _file in files[modName]:
        if not Path(_file + '.pdf').is_file() or True:
            html = '' + pre_html
            html += open(_file, 'r').read()
            html = html.decode('utf-8')
            pbar.write(_file + '.pdf')
            pdfkit.from_string(html, _file + '.pdf', {'quiet': ''})

    merger = PdfFileMerger()
    for _file in files[modName]:
        p = Path(_file)
        pdfName = str(p.parent.joinpath(p.stem + '.html.pdf'))
        merger.append(open(pdfName, 'rb'), import_bookmarks=False)

    with open(modName + '.pdf', "wb") as fout:
        merger.write(fout)
        pbar.update(1)
        pbar.write(modName + '.pdf')

    mergerSprint.append(open(modName +'.pdf', 'rb'), import_bookmarks=False)

ultimateName = 'Sprint5.pdf'
with open(ultimateName, "wb") as fout:
    mergerSprint.write(fout)
    print "Merged " + ultimateName
    pbar.close()
