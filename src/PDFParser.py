#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2021/1/18 8:26
# @Author  : Leslee
import re
import pdfplumber
import itertools
import xlrd, xlwt

def read_pdf(file_path):
    return pdfplumber.open(file_path)

f = open("../data/001.txt", "a+", encoding="utf-8")

my_pdf = read_pdf("../data/000001.pdf")
pdf_text = []
pdf_tables = []
for page in my_pdf.pages:
    print(page.extract_text())
    page_tables = page.extract_tables()
    page_text = page.extract_text()
    page_words = page.extract_words()
    # print(page.to_image())
    if page.extract_text():
        pdf_text.append(page.extract_text())
        f.write(page.extract_text())
    if page.extract_tables():
        combine_text = []
        page_tables = page.extract_tables()
        # page_cols = list()  # TODO： 先考虑每页只有一个表格的情况。有可能存在一页有多个表格的情况
        # page_table = []
        for table in page_tables:
            pdf_table = []
            page_table = table
            # page_cols = list(map(list,itertools.zip_longest(*table)))

            # 判断表头有最长有几行，将表头拼接在一起；
            header = 2
            result = []
            #  先对表头进行补全，补全规则为如果第一列存在None的情况，就复制前一个
            header0 = page_table[0]
            for i in range(len(header0)):
                if header0[0] is None:
                    continue
                if header0[i] is None:
                    header0[i] = header0[i-1]
            # 对第二行的表头处理规则为，存在None，就转为空
            for data in page_table[1:header]:
                for j in range(len(data)):
                    if data[j] is None:
                        data[j] = ""
                    else:
                        continue
            print(page_table)
            # 先循环page_table，把表头加在一起
            header_text = {}
            table_reverse = list(map(list,itertools.zip_longest(*page_table)))
            i = 0
            for reverse in table_reverse:
                header_text[i] = "".join(reverse[j] for j in range(header))
                i += 1
            all_text = ""
            for table in page_table[header:]:
                res = ""
                for n in range(len(table)):
                    res += header_text[n] + table[n]
                res = res.replace("\n", "")
                all_text += res + "\n"
                f.write(res+"\n")
            pdf_table.append(all_text)
            pdf_tables.append(pdf_table)
    else:
        continue

my_pdf.close()
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

