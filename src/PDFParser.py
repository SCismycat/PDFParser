#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2021/1/18 8:26
# @Author  : Leslee
import pdfplumber
import itertools
import logging


def read_pdf(file_path):
    return pdfplumber.open(file_path)


class PDFParser(object):
    def __init__(self, pdf_path):
        try:
            self.pdf = read_pdf(pdf_path)
        except Exception as e:
            logging.warning("PDF 读取出错：%s " % e)
    def parser(self):
        pdf_text = []
        pdf_tables = []
        i = 0
        for page in self.pdf.pages:
            i += 1
            if page.extract_text():
                pdf_text.append(page.extract_text())
            print("处理第%d页" % i)
            if page.extract_tables():
                page_tables = page.extract_tables()
                if len(page_tables) == 0 or page_tables == None:
                    continue
                try:
                    for tables in page_tables:
                        pdf_table = []
                        page_table = tables
                        # page_cols = list(map(list,itertools.zip_longest(*table)))
                        #  先对表头进行补全，补全规则为如果第一列存在None的情况，就复制前一个
                        # 无论如何，第一列都是表头
                        header0 = page_table[0]
                        # print(header0)
                        # print(header0)
                        if header0[0] is None or header0[0] == '':
                            header0[0] = ''
                        for i in range(len(header0)):
                            if header0[0] is None or header0[0] == '':
                                continue
                            if i == 1:
                                if header0[0] != None and header0[0] != '':
                                    header0[i] = header0[i-1]
                                    continue
                            if header0[i] is None and len(header0) >= 1:
                                header0[i] = header0[i-1]
                        max_x = 0
                        for x in tables[1:]:
                            if max_x > len(x):
                                max_x = max_x
                            else:
                                max_x = len(x)
                        header = 1
                        for table in tables[1:]:
                            if table.__contains__(None):
                                table.remove(None)
                            if len(table) < max_x:
                                header += 1
                            elif len(table) == max_x:
                                break
                        # 对所有的表头处理规则为，存在None，就转为空
                        for data in page_table[1:header]:
                            for j in range(len(data)):
                                if data[j] is None:
                                    data[j] = ""
                                else:
                                    continue
                        # print(page_table)
                        # 先循环page_table，把表头加在一起
                        header_text = {}
                        table_reverse = list(map(list, itertools.zip_longest(*page_table)))
                        i = 0
                        for reverse in table_reverse:
                            header_text[i] = "".join(reverse[j] if reverse[j] != None else "" for j in range(header))
                            i += 1
                        all_text = ""
                        for table in page_table[header:]:
                            res = ""
                            for n in range(len(table)):
                                if table[n] == None:
                                    table[n] = ""
                                res += header_text[n] + table[n] + " "
                            res = res.replace("\n", "")
                            all_text += res + "\n"
                        pdf_table.append(all_text)
                        pdf_tables.append(all_text)
                except Exception as e:
                    logging.exception("解析PDF表格出错: %s " % e)
            else:
                continue
        self.pdf.close()
        return pdf_text, pdf_tables
