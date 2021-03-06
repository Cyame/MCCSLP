# 优化配矿辅助系统 MCCSLP

一个为解决优化配矿问题而设计的系统。

[Tutorial in English](./README.md)

## 开始

请依次完成下述步骤以完成安装。

### 方案一：在本地环境中运行

#### 安装Python运行环境

前往[官网](https://www.python.org/downloads/)下载Python
#### 安装依赖

运行

```
pip install -r requirements.txt
```

如在中国大陆，可添加`-i https://mirrors.aliyun.com/pypi/simple/`以使用阿里云镜像

### 方案二：在虚拟环境中运行

#### 安装Python

前往官网下载Python3.7+

#### 安装虚拟环境支持

```
pip install virtualenv
```

#### 进入虚拟环境

```
source env/Scripts/activate
```

或(CMD)

```
env/Scripts/activate
```
## 使用

### 修改参数

请修改`config/constraint.hjson`中内容以变更优化参数。

### 设置成分

请修改`config/mineral.csv`中内容以变更成分参数。

### 运行

在根目录下运行`python src/run.py`以运行程序，相关模型和结论报告将在`workload/`中生成

## 许可

本仓库遵循GPL3.0协议。