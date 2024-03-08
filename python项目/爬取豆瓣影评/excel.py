# -*- coding: utf-8 -*-
'''
Created on 2015-6-4

@author: yuanyuan
'''
import xlrd
import xlwt
import os


class Excel:
    def __init__(self, excel_name, sheet_name):
        global bookWrite
        global bookRead
        global sheet

        self.excel_name = excel_name
        self.sheet_name = sheet_name

        bookWrite = xlwt.Workbook(encoding='utf-8')
        sheet = bookWrite.add_sheet(sheet_name, cell_overwrite_ok=True)

    # 写数据到excel
    def write(self, row, col, data):
        sheet.write(row, col, data)

    # 保存数据到文件
    def save(self):
        if os.path.exists(self.excel_name):
            os.remove(self.excel_name)
            bookWrite.save(self.excel_name)
        else:
            bookWrite.save(self.excel_name)

    # 读取excel数据：单元格
    def read(self, sheet_index, row, col):
        bookRead = xlrd.open_workbook(self.excel_name)
        sheet = bookRead.sheet_by_index(sheet_index)  # 根据索引获取工作表
        return sheet.cell(row, col).value  # 根据行与列获取单元格值

    # 读取excel数据：单行数据
    def read_by_row(self, sheet_index, row):
        bookRead = xlrd.open_workbook(self.excel_name)
        sheet = bookRead.sheet_by_index(sheet_index)  # 根据索引获取工作表
        return sheet.row_values(row)  # 根据行获取一行单元格

    # 读取excel数据：单列数据
    def read_by_col(self, sheet_index, col):
        bookRead = xlrd.open_workbook(self.excel_name)
        sheet = bookRead.sheet_by_index(sheet_index)  # 根据索引获取工作表
        return sheet.col_values(col)  # 根据列获取一列单元格