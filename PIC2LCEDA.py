#!/usr/bin/python3
# -*- coding: utf-8 -*-
import cv2
import numpy as np
from numpy import mat
import datetime
import os

layerstr = [
    'NULL', '顶层', '底层', '顶层丝印层', '底层丝印层', '顶层焊盘层', '底层焊盘层', '顶层阻焊层', '底层阻焊层',
    '边框层', '文档层'
]

# 测试模式
# 输入参数
# test_f = int(input('测试模式?(1, yes 0, no):'))
# if test_f == 1:
# if True:
#     x_size = 50
#     y_size = 50
#     layer = 7
#     sourcepath = '/home/kearney/Documents/Lan/python/PIC2LCEDA/'
#     sourcename = 'ddl.bmp'
#     invert_f = 1
#     threshold = 127  # 阈值
#     width = 5

# else:
#     x_size = int(input('请输入X最大尺寸(mm): '))
#     y_size = int(input('请输入y最大尺寸(mm): '))
#     width = int(input('请输入线宽(mil，越小精度越高，但可能导致卡顿，典型值5mil): '))
#     layer = int(
#         input(
#             '请输入所在层(1，顶层；2，底层；3，顶层丝印层；4，底层丝印层；5，顶层焊盘层；6，底层焊盘层；7，顶层阻焊层；8，底层阻焊层；10，边框层；11，文档层): '
#         ))
#     sourcepath = input('请输入源文件路径(示例：C:\\Users\\sora\\Desktop\\): ')
#     sourcename = input('请输入源文件名称(示例：test4.bmp): ')
#     invert_f = int(input('图像取反?(0,不取反 1,取反): '))
#     threshold = int(input('图像阈值(范围0~255，典型值127): '))

# 输入参数
# linux deepin,windows10均测试过支持相对路径
sourcefullpath = input('请输入图片路径(可直接拖曳文件至窗口) \
    \n示例：windows10:    C:\\Users\\sora\\Desktop\\test4.bmp \
    \n     Linux:  /home/kearney/Documents/Lan/python/PIC2LCEDA/ddl.bmp  \n:')
# 由文件绝对路径分离出路径和文件名
if os.path.isfile(sourcefullpath):
    (sourcepath, sourcename) = os.path.split(sourcefullpath)
    print((sourcepath, sourcename))
else:
    print("文件不存在！！！")
    raise
x_size = float(input('请输入X最大尺寸(mm): '))
y_size = float(input('请输入y最大尺寸(mm): '))
width = int(input('请输入线宽(mil，越小精度越高，但可能导致卡顿，典型值5mil): '))
layer = int(
    input(
        '请输入所在层(1，顶层；2，底层；3，顶层丝印层；4，底层丝印层；5，顶层焊盘层；6，底层焊盘层；7，顶层阻焊层；8，底层阻焊层；10，边框层；11，文档层): '
    ))

invert_f = int(input('图像取反?(0,不取反 1,取反): '))
threshold = int(input('图像阈值(范围0~255，典型值127): '))

# 打印输入参数
print('\n| 参数\t\t| 值 \t')
print('------------------------------------------------------')
print('| X最大尺寸\t| %.2f mm' % x_size)
print('| y最大尺寸\t| %.2f mm' % y_size)
print('| 所在层\t| %s' % layerstr[layer])
print('| 源文件路径\t| %s' % sourcefullpath)
print('| 图像取反\t| %s' % ('true' if invert_f == 1 else 'false'))
print("| 阈值\t\t| %d\n" % threshold)
print("| 线宽\t\t| %d mil\n" % width)

# 预设参数
origin_x = 0  # 原点x坐标
origin_y = 0  # 原点y坐标
path = os.path.join(
    sourcepath,
    'LCEDA' + str(datetime.datetime.now().strftime("%Y-%m-%d-%H-%M")))
if not os.path.exists(path):
    # 如果不存在则创建目录,win目录不能含有冒号
    os.makedirs(path)

lib_filename = 'LIB_' + sourcename + '.json'  # Lib文件名
pcb_filename = 'PCB_' + sourcename + '.json'  # PCB文件名

# 单位转换
x_size_mil = int(x_size / 2.54 * 100)
y_size_mil = int(y_size / 2.54 * 100)

# 图片处理
# 将数据存储在I矩阵
img = cv2.imread(sourcefullpath)
# 备份原图
cv2.imwrite(os.path.join(path, 'pre.jpg'), img,
            [int(cv2.IMWRITE_JPEG_QUALITY), 95])
# 图片缩放
im_raw, im_col = img.shape[0:2]
if im_raw / y_size_mil > im_col / x_size_mil:
    k = y_size_mil / im_raw
    x_size_mil = int(im_col * k) + 1
else:
    k = x_size_mil / im_col
    y_size_mil = int(im_raw * k) + 1
img = cv2.resize(img, (int(im_col * k / width), int(im_raw * k / width)))
# 色相取反
if invert_f != 0:
    img = cv2.bitwise_not(img)
# 拓展边缘
img = cv2.copyMakeBorder(img,
                         1,
                         1,
                         1,
                         1,
                         cv2.BORDER_CONSTANT,
                         value=[255, 255, 255])
# 去色
img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
# 二值化
ret, img = cv2.threshold(img, threshold, 255, cv2.THRESH_BINARY)
# img = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
#                             cv2.THRESH_BINARY, 11, 2)
# 翻转图片
if layer == 2 or layer == 4 or layer == 6 or layer == 8:
    img = cv2.flip(img, 1)
# 旋转
# img = img.transpose()
# 备份处理后的图片
cv2.imwrite(os.path.join(path, 'after.jpg'), img,
            [int(cv2.IMWRITE_JPEG_QUALITY), 95])

# 将图片处理成线条
# 图片-> 线段
#   o------>x (col)     o---0-->o
#   |                   ^       |1
#   |                 3 |       v
#   v                   o<--2---o
#   y (raw)
# lines_mil(start_x, start_y, end_x, end_y)
# lines_mil(start_col, start_raw, end_col, end_raw)
lines_mil = mat([
    [0, 0, x_size_mil / 10, 0],  # 0
    [x_size_mil / 10, 0, x_size_mil / 10, y_size_mil / 10],  # 1
    [x_size_mil / 10, y_size_mil / 10, 0, y_size_mil / 10],  # 2
    [0, y_size_mil / 10, 0, 0]  # 3
])
im_raw1, im_col1 = img.shape[0:2]
lastPix = 255
line_start = 0
line_end = 0
report_f = 1
print('step1:')
for i in range(im_raw1):
    lastPix = img[i, 0]
    for j in range(im_col1):
        if lastPix != img[i, j] and lastPix == 255:
            line_start = j
        elif lastPix != img[i, j] and lastPix == 0:
            line_end = j
            lines_mil = np.vstack((lines_mil,
                                   mat([
                                       line_start / 10 * width, i * width / 10,
                                       line_end / 10 * width, i * width / 10
                                   ])))
        lastPix = img[i, j]
        if (((i / img.shape[0]) * 100) - report_f) > 0.01:
            if report_f % 10 == 0:
                print('|  %2.0f%%\t|' % ((i / img.shape[0]) * 100), flush=True)
            else:
                print('|  %2.0f%%\t' % ((i / img.shape[0]) * 100),
                      flush=True,
                      end='')
            report_f = report_f + 1
print('| 100%\t|')
# 将图片数据写入Lib文件
# 打开文件，文件不存在则建立，文件已存在则覆盖
f = open(os.path.join(path, lib_filename), "w")
# 写入内容
f.write(
    '{\n    "head": {\n      "docType": "4",\n      "editorVersion": "6.4.2",\n      "newgId": true,\n      "c_para": {\n        "package": "%s",\n        "pre": "PIC?",\n        "Contributor": "LCNB",\n        "link": ""\n      },\n      "hasIdFlag": true,\n      "x": %.4f,\n      "y": %.4f\n    },\n'
    % (sourcename.split('.', 1)[0], (lines_mil[0, 0] + lines_mil[2, 0]) / 2,
       (lines_mil[0, 1] + lines_mil[2, 1]) / 2))
# 写入内容
f.write(
    '    "canvas": "CA~1000~1000~#000000~yes~#FFFFFF~10~1000~1000~line~10~mil~1~45~~0.5~%.4f~%.4f~0~none",\n    "shape": [\n'
    % ((lines_mil[0, 0] + lines_mil[2, 0]) / 2,
       (lines_mil[0, 1] + lines_mil[2, 1]) / 2))
# 开始打印写入进度
report_f = 1
print('\nstep2:')
# 写入实心填充-铜皮数据
f.write(
    '    "SOLIDREGION~1~~M %.4f %.4f L %.4f %.4f L %.4f %.4f L%.4f,%.4f Z~solid~ggb0~~~~0",\n'
    % (
        lines_mil[0, 0],
        lines_mil[0, 1],
        lines_mil[0, 2],
        lines_mil[0, 3],
        lines_mil[2, 0],
        lines_mil[2, 1],
        lines_mil[2, 2],
        lines_mil[2, 3],
    ))
f.write(
    '    "SOLIDREGION~2~~M %.4f %.4f L %.4f %.4f L %.4f %.4f L%.4f,%.4f Z~solid~ggb1~~~~0",\n'
    % (
        lines_mil[0, 0],
        lines_mil[0, 1],
        lines_mil[0, 2],
        lines_mil[0, 3],
        lines_mil[2, 0],
        lines_mil[2, 1],
        lines_mil[2, 2],
        lines_mil[2, 3],
    ))
# 写入边框数据
for i in range(4):
    f.write('    "TRACK~1~%d~~%.4f %.4f %.4f %.4f~ggc%d~0",\n' %
            (layer, lines_mil[i, 0], lines_mil[i, 1], lines_mil[i, 2],
             lines_mil[i, 3], i))
# 写入图像数据
for i in range(lines_mil.shape[0]):
    f.write('    "TRACK~%.1f~%d~~%.4f %.4f %.4f %.4f~gge%d~0"' %
            (width / 10, layer, lines_mil[i, 0], lines_mil[i, 1],
             lines_mil[i, 2], lines_mil[i, 3], i))
    if i != lines_mil.shape[0] - 1:
        f.write(',')
    f.write('\n')
    if (((i / lines_mil.shape[0]) * 100) - report_f) > 0.01:
        if report_f % 10 == 0:
            print('|  %2.0f%%\t|' % ((i / lines_mil.shape[0]) * 100),
                  flush=True)
        else:
            print('|  %2.0f%%\t' % ((i / lines_mil.shape[0]) * 100),
                  flush=True,
                  end='')
        report_f = report_f + 1
print('| 100%\t|')
# 写入内容
f.write(
    '],\n"layers": [\n  "1~TopLayer~#FF0000~true~true~true~",\n  "2~BottomLayer~#0000FF~true~false~true~",\n  "3~TopSilkLayer~#FFCC00~true~false~true~",\n  "4~BottomSilkLayer~#66CC33~true~false~true~",\n  "5~TopPasteMaskLayer~#808080~true~false~true~",\n  "6~BottomPasteMaskLayer~#800000~true~false~true~",\n  "7~TopSolderMaskLayer~#800080~true~false~true~0.3",\n  "8~BottomSolderMaskLayer~#AA00FF~true~false~true~0.3",\n  "9~Ratlines~#6464FF~false~false~true~",\n  "10~BoardOutLine~#FF00FF~true~false~true~",\n  "11~Multi-Layer~#C0C0C0~true~false~true~",\n  "12~Document~#FFFFFF~true~false~true~",\n  "13~TopAssembly~#33CC99~false~false~false~",\n  "14~BottomAssembly~#5555FF~false~false~false~",\n  "15~Mechanical~#F022F0~false~false~false~",\n  "19~3DModel~#66CCFF~false~false~false~",\n  "21~Inner1~#999966~false~false~false~~",\n  "22~Inner2~#008000~false~false~false~~",\n  "23~Inner3~#00FF00~false~false~false~~",\n  "24~Inner4~#BC8E00~false~false~false~~",\n  "25~Inner5~#70DBFA~false~false~false~~",\n  "26~Inner6~#00CC66~false~false~false~~",\n  "27~Inner7~#9966FF~false~false~false~~",\n  "28~Inner8~#800080~false~false~false~~",\n  "29~Inner9~#008080~false~false~false~~",\n  "30~Inner10~#15935F~false~false~false~~",\n  "31~Inner11~#000080~false~false~false~~",\n  "32~Inner12~#00B400~false~false~false~~",\n  "33~Inner13~#2E4756~false~false~false~~",\n  "34~Inner14~#99842F~false~false~false~~",\n  "35~Inner15~#FFFFAA~false~false~false~~",\n  "36~Inner16~#99842F~false~false~false~~",\n  "37~Inner17~#2E4756~false~false~false~~",\n  "38~Inner18~#3535FF~false~false~false~~",\n  "39~Inner19~#8000BC~false~false~false~~",\n  "40~Inner20~#43AE5F~false~false~false~~",\n  "41~Inner21~#C3ECCE~false~false~false~~",\n  "42~Inner22~#728978~false~false~false~~",\n  "43~Inner23~#39503F~false~false~false~~",\n  "44~Inner24~#0C715D~false~false~false~~",\n  "45~Inner25~#5A8A80~false~false~false~~",\n  "46~Inner26~#2B937E~false~false~false~~",\n  "47~Inner27~#23999D~false~false~false~~",\n  "48~Inner28~#45B4E3~false~false~false~~",\n  "49~Inner29~#215DA1~false~false~false~~",\n  "50~Inner30~#4564D7~false~false~false~~",\n  "51~Inner31~#6969E9~false~false~false~~",\n  "52~Inner32~#9069E9~false~false~false~~",\n  "99~ComponentShapeLayer~#00CCCC~false~false~false~",\n  "100~LeadShapeLayer~#CC9999~false~false~false~",\n  "Hole~Hole~#222222~~false~true~",\n  "DRCError~DRCError~#FAD609~~false~true~"\n],\n"objects": [\n  "All~true~false",\n  "Component~true~true",\n  "Prefix~true~true",\n  "Name~true~false",\n  "Track~true~true",\n  "Pad~true~true",\n  "Via~true~true",\n  "Hole~true~true",\n  "Copper_Area~true~true",\n  "Circle~true~true",\n  "Arc~true~true",\n  "Solid_Region~true~true",\n  "Text~true~true",\n  "Image~true~true",\n  "Rect~true~true",\n  "Dimension~true~true",\n  "Protractor~true~true"\n],\n'
)
# 写入内容
f.write(
    '  "BBox": {\n    "x": %.1f,\n    "y": %.1f,\n    "width": %.1f,\n    "height": %.1f\n  },'
    % ((lines_mil[0, 0] + lines_mil[2, 0]) / 2,
       (lines_mil[0, 1] + lines_mil[2, 1]) / 2, x_size_mil, y_size_mil))
# 写入内容
f.write('  "netColors": {}\n}')
f.close()

# 将边框数据写入PCB文件
# 打开文件
f = open(os.path.join(path, pcb_filename), "w")
# 写入内容
f.write(
    '{\n    "head": {\n      "docType": "3",\n      "editorVersion": "6.4.2",\n      "newgId": true,\n      "c_para": {},\n      "hasIdFlag": true\n    },\n    "canvas": "CA~1000~1000~#000000~yes~#FFFFFF~39.370079~1000~1000~line~3.937008~mm~1~45~~0.5~%.4f~%.4f~0~yes",\n    "shape": [\n'
    % ((lines_mil[0, 0] + lines_mil[2, 0]) / 2,
       (lines_mil[0, 1] + lines_mil[2, 1]) / 2))
# 输出提示信息
print('\nstep3:')
# 写入边框数据
for i in range(4):
    f.write('    "TRACK~1~%d~S$998~%.4f %.4f %.4f %.4f~ggc%d~0"' %
            (10, lines_mil[i, 0], lines_mil[i, 1], lines_mil[i, 2],
             lines_mil[i, 3], i))
    if i != 3:
        f.write(',')
    f.write('\n')
# 完成
print('| 100%\t|')
# 写入内容
f.write(
    '    ],\n"layers": [\n  "1~TopLayer~#FF0000~true~false~true~",\n  "2~BottomLayer~#0000FF~true~false~true~",\n  "3~TopSilkLayer~#FFCC00~true~false~true~",\n  "4~BottomSilkLayer~#66CC33~true~true~true~",\n  "5~TopPasteMaskLayer~#808080~true~false~true~",\n  "6~BottomPasteMaskLayer~#800000~true~false~true~",\n  "7~TopSolderMaskLayer~#800080~true~false~true~0.3",\n  "8~BottomSolderMaskLayer~#AA00FF~true~false~true~0.3",\n  "9~Ratlines~#6464FF~false~false~true~",\n  "10~BoardOutLine~#FF00FF~true~false~true~",\n  "11~Multi-Layer~#C0C0C0~true~false~true~",\n  "12~Document~#FFFFFF~true~false~true~",\n  "13~TopAssembly~#33CC99~false~false~false~",\n  "14~BottomAssembly~#5555FF~false~false~false~",\n  "15~Mechanical~#F022F0~false~false~false~",\n  "19~3DModel~#66CCFF~false~false~false~",\n  "21~Inner1~#999966~false~false~false~~",\n  "22~Inner2~#008000~false~false~false~~",\n  "23~Inner3~#00FF00~false~false~false~~",\n  "24~Inner4~#BC8E00~false~false~false~~",\n  "25~Inner5~#70DBFA~false~false~false~~",\n  "26~Inner6~#00CC66~false~false~false~~",\n  "27~Inner7~#9966FF~false~false~false~~",\n  "28~Inner8~#800080~false~false~false~~",\n  "29~Inner9~#008080~false~false~false~~",\n  "30~Inner10~#15935F~false~false~false~~",\n  "31~Inner11~#000080~false~false~false~~",\n  "32~Inner12~#00B400~false~false~false~~",\n  "33~Inner13~#2E4756~false~false~false~~",\n  "34~Inner14~#99842F~false~false~false~~",\n  "35~Inner15~#FFFFAA~false~false~false~~",\n  "36~Inner16~#99842F~false~false~false~~",\n  "37~Inner17~#2E4756~false~false~false~~",\n  "38~Inner18~#3535FF~false~false~false~~",\n  "39~Inner19~#8000BC~false~false~false~~",\n  "40~Inner20~#43AE5F~false~false~false~~",\n  "41~Inner21~#C3ECCE~false~false~false~~",\n  "42~Inner22~#728978~false~false~false~~",\n  "43~Inner23~#39503F~false~false~false~~",\n  "44~Inner24~#0C715D~false~false~false~~",\n  "45~Inner25~#5A8A80~false~false~false~~",\n  "46~Inner26~#2B937E~false~false~false~~",\n  "47~Inner27~#23999D~false~false~false~~",\n  "48~Inner28~#45B4E3~false~false~false~~",\n  "49~Inner29~#215DA1~false~false~false~~",\n  "50~Inner30~#4564D7~false~false~false~~",\n  "51~Inner31~#6969E9~false~false~false~~",\n  "52~Inner32~#9069E9~false~false~false~~",\n  "99~ComponentShapeLayer~#00CCCC~false~false~false~",\n  "100~LeadShapeLayer~#CC9999~false~false~false~",\n  "Hole~Hole~#222222~~false~true~",\n  "DRCError~DRCError~#FAD609~~false~true~"\n],\n"objects": [\n  "All~true~false",\n  "Component~true~true",\n  "Prefix~true~true",\n  "Name~true~false",\n  "Track~true~true",\n  "Pad~true~true",\n  "Via~true~true",\n  "Hole~true~true",\n  "Copper_Area~true~true",\n  "Circle~true~true",\n  "Arc~true~true",\n  "Solid_Region~true~true",\n  "Text~true~true",\n  "Image~true~true",\n  "Rect~true~true",\n  "Dimension~true~true",\n  "Protractor~true~true"\n],'
)
# 写入内容
f.write(
    '\n  "BBox": {\n    "x": %.1f,\n    "y": %.1f,\n    "width": %.1f,\n    "height": %.1f\n  }'
    % ((lines_mil[0, 0] + lines_mil[2, 0]) / 2,
       (lines_mil[0, 1] + lines_mil[2, 1]) / 2, x_size_mil, y_size_mil))
# 写入内容
f.write(
    ',\n  "preference": {\n    "hideFootprints": "",\n    "hideNets": ""\n  },\n  "DRCRULE": {\n    "Default": {\n      "trackWidth": 1,\n      "clearance": 0.6,\n      "viaHoleDiameter": 2.4,\n      "viaHoleD": 1.2\n    },\n    "isRealtime": false,\n    "isDrcOnRoutingOrPlaceVia": false,\n    "checkObjectToCopperarea": true,\n    "showDRCRangeLine": true\n  },\n  "netColors": {}\n}'
)
f.close()

# 生成图片信息文件
# 输出提示信息
print('\nstep4:')
# 写入内容
f = open(os.path.join(path, 'info.txt'), "w")
f.write('\n| 参数\t\t| 值 \n'),
f.write('------------------------------------------------------\n')
f.write('| 原图X像素\t| %.4f pix\n' % im_col)
f.write('| 原图y像素\t| %.4f pix\n' % im_raw)
f.write("| 线宽\t\t| %d mil\n" % width)
f.write('| X最大尺寸\t| %.4f mm\n' % x_size)
f.write('| y最大尺寸\t| %.4f mm\n' % y_size)
f.write('| X实际像素\t| %.4f pix\n' % x_size_mil)
f.write('| y实际像素\t| %.4f pix\n' % y_size_mil)
f.write('| X实际尺寸\t| %.4f mm\n' % (x_size_mil / 100 * 2.54))
f.write('| y实际尺寸\t| %.4f mm\n' % (y_size_mil / 100 * 2.54))
f.write('| 所在层\t\t| %s\n' % layerstr[layer])
f.write('| 源文件路径\t| %s\n' % sourcepath)
f.write('| 源文件名称\t| %s\n' % sourcename)
f.write('| 生成文件路径\t| %s\n' % path)
f.write('| Lib文件名称\t| %s\n' % lib_filename)
f.write('| Lib文件名称\t| %s\n' % pcb_filename)
f.write('| 图像取反\t| %s\n' % ('true' if invert_f == 1 else 'false'))
f.write("| 阈值\t\t| %d\n" % threshold)
f.close()
# 完成
print('| 100%\t|')

# 写入完成
print(
    '\n生成成功！\nLib文件路径: %s\nPCB文件路径: %s\n实际图片大小: \tX %.4f mil,\tY %.4f mil \n\t\tX %.4f mm,\t\tY %.4f mm'
    % (path + lib_filename, path + pcb_filename, x_size_mil, y_size_mil,
       x_size_mil / 100 * 2.54, y_size_mil / 100 * 2.54))
