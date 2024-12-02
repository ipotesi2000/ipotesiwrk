#!/usr/bin/env python
# coding: utf-8
import sys
import pypandoc

def docx2html(input_path, output_path):
    # Usa pypandoc per convertire il file DOCX in HTML
    output = pypandoc.convert_file(input_path, 'html', outputfile=output_path)
    assert output == ""
    print(f"Conversione completata: {output_path}")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("docx2html.py <file_docx> <file_html>")
        sys.exit(1)
    input_path = sys.argv[1]
    output_path = sys.argv[2]
    docx2html(input_path, output_path)
