#!/usr/bin/env python
# coding: utf-8
import os
import pathlib as pt
from pathlib import Path
import sys
import shutil
import markdown


def rlist(path: str, match: str = "*") -> list:
    return [str(x) for x in pt.Path(path).rglob(match)]

def make_dir(path: str, mode: int = 0o777):
    p = pt.Path(path)
    p.mkdir(parents=True, exist_ok=True, mode=mode)
    p.chmod(mode=mode)

def md2html(md_path, html_path):
    with open(md_path, 'r', encoding='utf-8') as md_file:
        md_content = md_file.read()
    html_content = markdown.markdown(md_content)
    with open(html_path, 'w', encoding='utf-8') as html_file:
        html_file.write(html_content)

def move2back(file_path):
    file_path = Path(file_path)
    current_dir = file_path.parent
    backup_dir = current_dir.with_name(current_dir.name + "_back")
    backup_dir.mkdir(parents=True, exist_ok=True)
    destination_path = backup_dir / file_path.name
    shutil.move(str(file_path), str(destination_path))

def dirmd2html(src_dir, dest_dir):
    print(dest_dir)
    make_dir(dest_dir)
    path_lst = rlist(src_dir, "*.md")
    for md_path in path_lst:
        print(md_path)
        fname = os.path.basename(md_path).replace(".md", ".html")
        fname = fname.lower()
        fname = fname.replace(" ", "_")
        html_path = os.path.join(dest_dir, fname)
        md2html(md_path, html_path)
        move2back(md_path)

if __name__ == "__main__":
    if len(sys.argv) < 3:
     print("\n\nread_prd.py <dir sorgente>  <dir destinazione>")
     exit()
    dir_src = sys.argv[1]
    dir_dst = sys.argv[2]
    dirmd2html(dir_src, dir_dst)
