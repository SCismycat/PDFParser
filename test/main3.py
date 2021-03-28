#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2021/1/19 23:34
# @Author  : Leslee
import os
import logging
import pandas as pd
import multiprocessing
from multiprocessing import Process
from PDFParser import PDFParser


# 显示所有列
pd.set_option('display.max_columns', None)
# 显示所有行
pd.set_option('display.max_rows', None)
# 设置value的显示长度为100，默认为50
pd.set_option('max_colwidth', 100)


def main(file_path, writer_path):
    file_dirs = os.listdir(file_path)
    exists_dirs = [x.split(".")[0] for x in os.listdir("../data2/")]
    deal_dirs = []
    for file in file_dirs:
        if file not in exists_dirs:
            deal_dirs.append(file)
        else:
            continue
    for dir_file in deal_dirs[601:800]:
        dir_path = file_path + dir_file + "/"
        current_pdf_result = deal_pdf(file_path=dir_path)
        print("处理完成当前pdf！")
        try:
            save_to_excel(writer_file=writer_path, filename=dir_file, save_list=current_pdf_result)
        except Exception as e:
            logging.warning("保存写入到excel*%s*时出错：%s" % (dir_file, e))
        print("写入到excel完成")


def deal_pdf(file_path):
    """
    批量处理pdf
    :param file_path:
    :return:
    """
    files = os.listdir(file_path)
    # List中是所有pdf，每个pdf分为title：content：tables1：tablesi
    all_pdf = []
    for file in files:
        if not os.path.isdir(file) and file.endswith(".pdf"):
            parsed_pdf = []
            f_path = file_path + file
            file_title = "".join(file.split(".pdf"))
            pdf_parser = PDFParser(f_path)
            logging.info("开始处理文章： %s" % file_title)
            print("开始处理文章： %s" % file_title)
            try:
                pdf_texts, pdf_tables = pdf_parser.parser()
            except Exception as e:
                logging.warning("处理：*%s*时出错：%s" % (file_title, e))
                pdf_texts = ''
                pdf_tables = None
            # 拼成(title, pdf_text, pdf_tables的形式，表格往后排列)
            pdf_texts = "".join(pdf_texts)
            parsed_pdf.append(file_title)
            parsed_pdf.append(pdf_texts)
            if pdf_tables is not None:
                for tab in pdf_tables:
                    parsed_pdf.append(tab)
            all_pdf.append(parsed_pdf)
    return all_pdf


def save_to_excel(writer_file, filename, save_list):
    dataFrame = pd.DataFrame(save_list)
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
    logging.info("Start Writer to Excel!")
    dataFrame.to_excel(writer_file + str(filename) + ".xlsx", index=False)
    logging.info("Excel Writer Over!")


if __name__ == '__main__':
    origin_path = "G:/report/"
    writer_path = "../data2/"
    main(origin_path, writer_path=writer_path)

