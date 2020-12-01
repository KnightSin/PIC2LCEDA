# PIC2LCEDA
立创EDA_PCB照片生成器，作者：矛盾聚合体  
使用文档请看[PCB照片_附带生成脚本](https://lceda.cn/Knight_Sin/PCBzhao-pian)
# 使用
## 方法一：下载程序
windows、Linux已经编译好的程序（By pyinstaller）见Release或者百度网盘
[20201201win+linuxV0.0.0 提取码: yirq](https://pan.baidu.com/s/1uG6g0DEBkowuJXRK9za9VA)
## 方法二：自行编译
### 环境准备
- 安装python3
```bash
# linux
$ sudo apt install python3
```
- 安装依赖包：opencv、numpy
```bash
$ pip3 install numpy
$ pip3 install opencv-python
```
### 克隆代码、运行
```bash
$ git clone githubUrl
$ cd PIC2LCEDA
$ python3 PIC2LCEDA.py
```

# License
GPL-3.0 License
# Reference
- [KnightSin/PIC2LCEDA](https://github.com/KnightSin/PIC2LCEDA/blob/master/1.png)
- [PCB照片_附带生成脚本](https://lceda.cn/Knight_Sin/PCBzhao-pian)
- [no module named cv2](https://www.cnblogs.com/zjutzz/p/11944662.html)
