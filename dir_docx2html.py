#!/usr/bin/env python
# coding: utf-8
import os
import pathlib as pt
from pathlib import Path
import sys
import pypandoc
import shutil

# pip install pypandoc

def rlist(path: str, match: str = "*") -> list:
    return [str(x) for x in pt.Path(path).rglob(match)]

def make_dir(path: str, mode: int = 0o777):
    p = pt.Path(path)
    p.mkdir(parents=True, exist_ok=True, mode=mode)
    p.chmod(mode=mode)

def move2back(file_path):
    # Converti il percorso del file in un oggetto Path
    file_path = Path(file_path)
    # Ottieni la directory corrente del file
    current_dir = file_path.parent
    # Crea il nome della directory di backup
    backup_dir = current_dir.with_name(current_dir.name + "_back")
    # Crea la directory di backup se non esiste
    backup_dir.mkdir(parents=True, exist_ok=True)
    # Costruisci il percorso di destinazione nella directory di backup
    destination_path = backup_dir / file_path.name
    # Sposta il file nella directory di backup
    shutil.move(str(file_path), str(destination_path))


def docx2html(docx_path, html_path):
    try:
        # Usa pypandoc per convertire il file DOCX in HTML
        output = pypandoc.convert_file(docx_path, 'html', outputfile=html_path)
        assert output == ""
        print(f"Conversione completata: {html_path}")
    except Exception as e:
        print(f"Errore: {e}")
        exit(1)

def dirdocx2html(src_dir, dest_dir):
    make_dir(dest_dir)
    path_lst = rlist(src_dir, "*.docx")
    for doc_path in path_lst:
        print(doc_path)
        fname = os.path.basename(doc_path).replace(".docx", ".html")
        fname = fname.lower()
        fname = fname.replace(" ", "_")
        html_path = os.path.join(dest_dir, fname)
        docx2html(doc_path, html_path)
        move2back(doc_path)

if __name__ == "__main__":
    dir_src = "./data/docx"
    dir_dst = "./data/html"
    if len(sys.argv) < 3:
        print("\n\ndir_docx2html.py <dir sorgente>  <dir destinazione>")
        exit()
    dir_src = sys.argv[1]
    dir_dst = sys.argv[2]
    dirdocx2html(dir_src, dir_dst)
