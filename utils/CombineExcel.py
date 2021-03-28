#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2021/2/24 22:38
# @Author  : Leslee
import os
import pandas as pd
from queue import Queue


def main(fileDir, writePath):
    fileList = os.listdir(fileDir)
    i = 0
    while True:
        datas = []
        for name in fileList[i:i+100]:
            excel_path = fileDir + name
            # .values.tolist()
            data = pd.read_excel(excel_path, header=None, index_col=False).values.tolist()
            for d in data[1:]:
                d = [str(a).replace("\n", "") for a in d if not pd.isna(a)]
                datas.append(d)
            print("读取：%s" % excel_path)
        print("处理到第%d 篇" % i)
        i += 100
        # dataFrame = pd.concat(datas)
        dataFrame = pd.DataFrame(datas)
        dataFrame.to_csv(writePath, header=False, index=False, mode="a")
        if i >= len(fileList):
            break

if __name__ == '__main__':
    fileDirs = "../data2/"
    writer_path = "./allexcel.csv"
    main(fileDirs, writer_path)