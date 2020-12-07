#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QMessageBox
from PyQt5.QtGui import QIcon
from functools import partial
import sys
import ui
import PIC2LCEDA

ICO = QIcon

# 刷新图片


def refreshImg():
    sourcefullpath = ui.sourcefullpath.text()
    x_size = float(ui.x_size.text())
    y_size = float(ui.y_size.text())
    width = int(ui.width.text())
    layer_index = int(ui.layer.currentIndex())  # 文字对应的序号 0～9
    color_invert_f = int(ui.color_invert_f.checkState())  # 默认不取反0，选中为2
    x_invert_f = int(ui.x_invert_f.checkState())  # 默认不翻转0，选中为2
    y_invert_f = int(ui.y_invert_f.checkState())  # 默认不翻转0，选中为2
    threshold = ui.thresholdSlider.value()

    if layer_index < 8:
        layer = layer_index + 1
    else:
        layer = layer_index + 2

    if PIC2LCEDA.transformpic(sourcefullpath, x_size, y_size, width, layer, color_invert_f, x_invert_f, y_invert_f, threshold) != -1:
        img = PIC2LCEDA.transformpic(sourcefullpath, x_size, y_size, width,
                                     layer, color_invert_f, x_invert_f, y_invert_f, threshold)[0]
    else:
        print("image missed！！！")
        msg = QMessageBox()
        msg.setWindowIcon(QIcon("img/ico.png"))
        msg.setText("图片不存在")
        msg.setInformativeText("可能还没有选择图片，\n或者选择的图片神秘消失了Σ(ﾟдﾟ;)")
        msg.setWindowTitle("温馨提示")
        msg.setStandardButtons(QMessageBox.Ok)
        msg.show()
        retval = msg.exec_()
        print(retval)
        return
    # 缩放比例
    k = 400/img.shape[0]
    # 展示图片
    PIC2LCEDA.showImg(img, k)

# 线宽编辑框值改变


def width_textChanged(ui):
    refreshImg()

# x最大尺寸编辑框值改变


def x_size_textChanged(ui):
    refreshImg()

# y最大尺寸编辑框值改变


def y_size_textChanged(ui):
    refreshImg()

# 阈值条数值变更


def thresholdSlider_valueChanged(ui):
    ui.threshold_label.setText(str(ui.thresholdSlider.value()))
    refreshImg()

# 反相选项框被单击


def color_invert_f_clicked(ui):
    refreshImg()

# 水平翻转选项框被单击


def x_invert_f_clicked(ui):
    refreshImg()

# 垂直翻转选项框被单击


def y_invert_f_clicked(ui):
    refreshImg()

# 选取文件按钮被单击


def on_clicked_btn_getfile(ui):
    fileName = QFileDialog.getOpenFileName()
    if len(fileName[0]):
        # print(fileName[0])
        ui.sourcefullpath.setText(fileName[0])
        refreshImg()
    else:
        print("empty")

# 文件生成按钮被单击


def on_clicked_btn_convert(ui):

    sourcefullpath = ui.sourcefullpath.text()
    x_size = float(ui.x_size.text())
    y_size = float(ui.y_size.text())
    width = int(ui.width.text())
    # layer_text = ui.layer.currentText()  # 文字
    layer_index = int(ui.layer.currentIndex())  # 文字对应的序号 0～9
    color_invert_f = int(ui.color_invert_f.checkState())  # 默认不取反0，选中为2
    copper_f = int(ui.copper_f.checkState())  # 默认无铜皮0，选中为2
    x_invert_f = int(ui.x_invert_f.checkState())  # 默认不翻转0，选中为2
    y_invert_f = int(ui.y_invert_f.checkState())  # 默认不翻转0，选中为2
    threshold = ui.thresholdSlider.value()
    print(sourcefullpath, x_size, y_size, width, layer_index,
          color_invert_f, x_invert_f, y_invert_f, threshold)
    if layer_index < 8:
        layer = layer_index + 1
    else:
        layer = layer_index + 2
    # print(layer)
    res = PIC2LCEDA.makepcb(sourcefullpath, x_size, y_size, width, layer,
                            color_invert_f, copper_f, x_invert_f, y_invert_f, threshold)
    if res == 0:
        print("Convert Done")
        msg = QMessageBox()
        msg.setWindowIcon(QIcon("img/ico.png"))
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
        msg.setWindowIcon(QIcon("img/ico.png"))
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
    MainWindow.setWindowIcon(QIcon("img/ico.png"))

    ui = ui.Ui_ui()
    ui.setupUi(MainWindow)
    ui.btn_convert.clicked.connect(partial(on_clicked_btn_convert, ui))
    ui.btn_getfile.clicked.connect(partial(on_clicked_btn_getfile, ui))
    ui.thresholdSlider.valueChanged.connect(
        partial(thresholdSlider_valueChanged, ui))
    ui.color_invert_f.clicked.connect(partial(color_invert_f_clicked, ui))
    ui.x_invert_f.clicked.connect(partial(x_invert_f_clicked, ui))
    ui.y_invert_f.clicked.connect(partial(y_invert_f_clicked, ui))
    ui.width.textChanged.connect(partial(width_textChanged, ui))
    ui.x_size.textChanged.connect(partial(x_size_textChanged, ui))
    ui.y_size.textChanged.connect(partial(y_size_textChanged, ui))

    MainWindow.show()
    sys.exit(app.exec_())
