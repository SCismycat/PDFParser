#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2021/1/18 8:26
# @Author  : Leslee
import re
import pdfplumber


def read_pdf(file_path):
    return pdfplumber.open(file_path)


my_pdf = read_pdf("../data/000002.pdf")
for page in my_pdf.pages:
    print(page.extract_text())
    page_tables = page.extract_tables()
    print(page.to_image())
    for pdf_table in page.extract_tables():
        table = []
        cells = []
        for row in pdf_table:
            if not any(row):
                if any(cells):
                    table.append(cells)
                    cells = []
            elif all(row):
                # 如果一行全不为空，本条是新行，上一条结束
                if any(cells):
                    table.append(cells)
                    cells = []
                table.append(row)
            else:
                if len(cells) == 0:
                    cells = row
                else:
                    for i in range(len(row)):
                        if row[i] is not None:
                            cells[i] = row[i] if cells[i] is None else cells[i] + row[i]
        for row in table:
            print([re.sub('\s+', '', cell) if cell is not None else None for cell in row])
        print('---------- 分割线 ----------')
my_pdf.close()
