#!/usr/bin/env python
# coding: utf-8
import sys
import pypandoc

def html2md(input_path, output_path):
    # Usa pypandoc per convertire il file HTML in Markdown
    output = pypandoc.convert_file(input_path, 'md', outputfile=output_path)
    assert output == ""
    print(f"Conversione completata: {output_path}")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Uso: python html2md.py <file_html> <file_md>")
        sys.exit(1)
    input_path = sys.argv[1]
    output_path = sys.argv[2]
    html2md(input_path, output_path)
