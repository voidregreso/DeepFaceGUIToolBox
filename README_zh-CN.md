# DeepFace GUI Toolbox



*其他语言阅读: [英语](README.md), [西班牙语](README_es.md), [法语](README_fr.md), [巴西葡语](README_pt-BR.md), [阿拉伯语](README_ar.md), [简体中文](README_zh-CN.md).*

### 1. 简介

> Deepface是一个轻量级的Python框架，用于人脸识别和面部属性分析（年龄、性别、情绪和种族）。它是一个混合的人脸识别框架，包含最先进的模型：VGG-Face, Google FaceNet, OpenFace, Facebook DeepFace, DeepID, ArcFace, Dlib 和 SFace。

但是，原来的项目只有API模块和样板控制台程序，使用和操作都不方便；同时，由于相应的模型文件需要从网上下载来识别面部特征，而这些文件非常大，在一些国家其网址被干扰和封锁，所以我用Python+PyQt5开发了一个可视化界面的程序。它支持以下功能： 

- 用矩形选框表示识别的面部区域；
- 做彻底的年龄、性别、种族、情绪分析，其中种族和表情分析可以精确到每个可能的识别结果的百分比；
- 验证两张脸是否代表同一个人，即用百分比推断出相似度；
- 多种人脸检测器后端和验证模型可供选择；
- 配置代理，加快模型文件的下载速度（目前只支持HTTP(S)协议，SOCKS协议的代理仍需研究和改进）；
- 友好易上手的用户界面。

### 2. 用法

1. 下载并安装 Python 3.9；

2. 用如下命令安装依赖包：

   ```bash
   pip install deepface dlib configparser urllib3 PyQt5 PyQt5-tools
   ```

3. 运行 main.py

现在，单一文件的运行环境也正在打包，并将在稍后发布。

如果你想重新设计用户界面文件，你应该在编辑UI文件之后通过以下命令重新生成相应的初始化代码文件：

```bash
pyuic5 -o ventana.py ventana.ui
```

### 3. 面部图片资源实例

我把相应种族的脸部照片放在五个文件夹里。*asian, black, hispanic, india_arab, white*，每个文件夹有大约15张图片。你可以自由使用它们进行分析和测试。

### 4. 界面截图

![](scrshot.jpg)
