LCEDA图片转换器

作者：矛盾聚合体 & Kearney

简介：可将图片转换为立创EDA的PCB库文件，然后在立创EDA中以导入库的方式导入图像。
优点是导入后的图片较立创EDA自带的图片工具清晰度更高更细腻。

![win10下效果预览](https://image.lceda.cn/pullimage/2sn0T1YLOZSa1gTZYOoLbB2pJrnzIGx8H9TDlWlr.png)

# 使用说明
- 处理图片：参考[PCB照片_附带生成脚本](https://lceda.cn/Knight_Sin/PCBzhao-pian)，非必需，当然处理后更好看。
- 生成LIB：启动程序后，点击选取文件选取要转换的图片文件（当前仅支持一次一张），然后对各个参数进行修改，不修改将保持默认参数，设置好参数后点击生成图片，生成完成之后会弹出提示框提示转换完成，生成的Lib位于所选择图片相同目录下。  
- 导入LIB：打开立创EDA编辑器，在顶部菜单栏依次选择 -> “文件”-“打开”-“立创EDA”，然后选择刚才生成的LIB_xxx.json文件，在EDA中会打开库编辑器，删掉多余的图层，保存即可。
- PCB高清晰绘图：在PCB绘制界面，在左侧菜单栏依次选择 -> “元件库”-"立创EDA"-"封装",即可导入图片。
# 程序下载方式
GUI_v0.0.1版本的图片拖动功能**暂未完善**、请使用‘选择文件’功能选取图片文件。程序是免安装的，解压双击main.exe即可运行。

## 方法一：下载程序
windows、Linux已经编译好的程序（By pyinstaller）见Release或者百度网盘

[20201201win+linuxV0.0.0 提取码: yirq](https://pan.baidu.com/s/1uG6g0DEBkowuJXRK9za9VA)
[20201204win+linux_GUI_v0.0.1 提取码: d16s](https://pan.baidu.com/s/1RLmTxRCp_XaVfVA_X4VKsA )
## 方法二：自行编译
### 环境准备
- 安装python3
```bash
# linux
$ sudo apt install python3
```
- 安装依赖包：opencv、numpy、pyqt5
```bash
$ pip3 install numpy
$ pip3 install opencv-python
$ pip3 install pyqt5
```
### 克隆代码、运行
```bash
$ git clone git@github.com:KnightSin/PIC2LCEDA.git
$ cd PIC2LCEDA
$ python3 main.py
```
# 贡献方式
入门：点赞右上角Star点一下。  
修Bug和改进：准备依赖环境和Qt designer，fork本仓库，修改bug，一个issus(最小修改单位)一次commit。  
脚本哥：将本程序修改为js脚本作为浏览器插件（期待大佬ing）
# License
GPL-3.0 License
# Reference
- [PCB照片_附带生成脚本](https://lceda.cn/Knight_Sin/PCBzhao-pian)
- [立创EDA文档格式-标准版](https://docs.lceda.cn/cn/DocumentFormat/EasyEDA-Format-Standard/index.html)
- [no module named cv2](https://www.cnblogs.com/zjutzz/p/11944662.html)
