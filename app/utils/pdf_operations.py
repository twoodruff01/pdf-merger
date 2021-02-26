"""
Copied from:
https://realpython.com/pdf-python/
"""
from PyPDF2 import PdfFileReader, PdfFileWriter
from flask import current_app


def merge_pdfs(paths, output):
    current_app.logger.info('merge_pdfs function called')
    pdf_writer = PdfFileWriter()

    for path in paths:
        pdf_reader = PdfFileReader(path)
        for page in range(pdf_reader.getNumPages()):
            # Add each page to the writer object
            pdf_writer.addPage(pdf_reader.getPage(page))

    # Write out the merged PDF
    with open(output, 'wb') as out:
        pdf_writer.write(out)
