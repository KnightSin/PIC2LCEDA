#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
'''
@File    :  main.py
@Time    :  2020/12/03 23:32:20
@Author  :  Kearney
@Version :  0.0.0
@Contact :  191615342@qq.com
@License :  GPL 3.0
@Desc    :  图片转LCEDA封装的程序入口
'''
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QMessageBox
from functools import partial
import sys
import ui
import PIC2LCEDA


# 选取文件
def on_clicked_btn_getfile(ui):
    fileName = QFileDialog.getOpenFileName()
    if len(fileName[0]):
        # print(fileName[0])
        ui.sourcefullpath.setText(fileName[0])
    else:
        print("empty")


# 获取参数
def on_clicked_btn_convert(ui):

    sourcefullpath = ui.sourcefullpath.text()
    x_size = float(ui.x_size.text())
    y_size = float(ui.y_size.text())
    width = int(ui.width.text())
    # layer_text = ui.layer.currentText()  # 文字
    layer_index = int(ui.layer.currentIndex())  # 文字对应的序号 0～9
    invert_f = int(ui.invert_f.checkState())  # 默认不取反0，选中为2
    threshold = int(ui.threshold.text())
    print(sourcefullpath, x_size, y_size, width, layer_index, invert_f,
          threshold)
    if layer_index < 8:
        layer = layer_index + 1
    else:
        layer = layer_index + 2
    # print(layer)
    res = PIC2LCEDA.makepcb(sourcefullpath, x_size, y_size, width, layer,
                            invert_f, threshold)
    if res == 0:
        print("Convert Done")
        msg = QMessageBox()
        msg.setText("转换完成")
        msg.setInformativeText("图片已成功转换为立创EDA的库")
        msg.setWindowTitle("温馨提示")
        msg.setStandardButtons(QMessageBox.Ok)
        msg.show()
        retval = msg.exec_()
        print(retval)
    else:
        print("image missed！！！")
        msg = QMessageBox()
        msg.setText("图片不见啦")
        msg.setInformativeText("可能还没有选择图片哟、或者选择的图片神秘消失了哟")
        msg.setWindowTitle("温馨提示")
        msg.setStandardButtons(QMessageBox.Ok)
        msg.show()
        retval = msg.exec_()
        print(retval)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    MainWindow = QMainWindow()
    ui = ui.Ui_ui()
    ui.setupUi(MainWindow)
    ui.btn_convert.clicked.connect(partial(on_clicked_btn_convert, ui))
    ui.btn_getfile.clicked.connect(partial(on_clicked_btn_getfile, ui))
    MainWindow.show()
    sys.exit(app.exec_())
