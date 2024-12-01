#!/usr/bin/env python
# coding: utf-8
import os
import pathlib as pt
import shutil
import sys
from pathlib import Path
from docx import Document

# pip install python-docx

def rlist(path: str, match: str = "*") -> list:
    return [str(x) for x in pt.Path(path).rglob(match)]

def make_dir(path: str, mode: int = 0o777):
    p = pt.Path(path)
    p.mkdir(parents=True, exist_ok=True, mode=mode)
    p.chmod(mode=mode)

def docx2txt(docx_path, txt_path):
    doc = Document(docx_path)
    full_text = []
    for para in doc.paragraphs:
        full_text.append(para.text)
    full_text = '\n'.join(full_text)
    with open(txt_path, 'w', encoding='utf-8') as txt_file:
        txt_file.write(full_text)

def move2back(file_path):
    file_path = Path(file_path)
    current_dir = file_path.parent
    backup_dir = current_dir.with_name(current_dir.name + "_back")
    backup_dir.mkdir(parents=True, exist_ok=True)
    destination_path = backup_dir / file_path.name
    shutil.move(str(file_path), str(destination_path))


def dirdocx2dirtxt(src_dir, dest_dir):
    make_dir(dest_dir)
    path_lst = rlist(src_dir, "*.docx")
    for doc_path in path_lst:
        print(doc_path)
        fname = os.path.basename(doc_path).replace(".docx", ".txt")
        fname = fname.lower()
        fname = fname.replace(" ", "_")
        txt_path = os.path.join(dest_dir, fname)
        docx2txt(doc_path,txt_path)
        move2back(doc_path)


if __name__ == "__main__":
    dir_src = "./data/docx"
    dir_dst = "./data/txt"
    if len(sys.argv)<3:
     print("\n\nread_prd.py <dir sorgente>  <dir destinazione")
     exit()
    dir_src = sys.argv[1]
    dir_dst = sys.argv[2]
    dirdocx2dirtxt(dir_src, dir_dst)
