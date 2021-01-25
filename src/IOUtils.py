#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2021/1/19 23:34
# @Author  : Leslee


def writer_excel(path, sheet_name, value):
    index = len(value)
    work_book = xlwt.Workbook()
    sheet = work_book.add_sheet(sheet_name)
    for i in range(index):
        for j in range(0, len(value[i])):
            sheet.write(i, j, value[i][j])
    work_book.save(path)
    print("写入成功")

path = "../data/002.xlsx"
ff_res = []
final_res = []
text_ = ""
for text in pdf_text:
    text = text.replace("\n","").replace("\n\n","")
    text_ += text
final_res.append([text_])
for table in pdf_tables:
    final_res.append(table)
ff_res.append(final_res)
writer_excel(path, "002", final_res)