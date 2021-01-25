#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2021/1/19 23:34
# @Author  : Leslee
import os
import pandas as pd
from PDFParser import PDFParser

#显示所有列
pd.set_option('display.max_columns', None)
#显示所有行
pd.set_option('display.max_rows', None)
#设置value的显示长度为100，默认为50
pd.set_option('max_colwidth',100)


def main(file_path, header, writer_path):
    """
    批量处理pdf
    :param file_path:
    :param header:
    :param writer_path:
    :return:
    """
    files = os.listdir(file_path)
    # List中是所有pdf，每个pdf分为title：content：tables1：tablesi
    all_pdf = []
    for file in files:
        if not os.path.isdir(file):
            parsed_pdf = []
            f_path = file_path + file
            file_title = "".join(file.split(".pdf"))
            pdfParser = PDFParser(f_path)
            pdf_texts, pdf_tables = pdfParser.parser(header)
            # 拼成(title, pdf_text, pdf_tables的形式，表格往后排列)
            pdf_texts = "".join(pdf_texts)
            parsed_pdf.append(file_title)
            parsed_pdf.append(pdf_texts)
            if pdf_tables is not None:
                for tab in pdf_tables:
                    parsed_pdf.append(tab)
            all_pdf.append(parsed_pdf)
    dataFrame = pd.DataFrame(all_pdf)
    print(dataFrame)
    col_name = []
    col_length = dataFrame.shape[1]
    for i in range(col_length):
        # 第一列是title
        if i == 0:
            col_name.append("文件名")
            continue
        if i == 1:
            col_name.append("文本")
            continue
        col_name.append("表格" + str(i))
    dataFrame.columns = col_name
    dataFrame.to_excel(writer_path, index=False)
    print("Excel Writer Over!")


if __name__ == '__main__':
    main("../data/", header=2, writer_path="./demo.xlsx")