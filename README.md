# MCCSLP
A consulting system for mineral collocation.

[中文手册](./README.cn.md)
## Get Started

Please follow the steps to get installed first.

### Install Python

Go to [OFFICIAL SITE](https://www.python.org/downloads/)

Because the develop environment is based on Python 3.7, so this version is also recommanded for runtime.

In most cases, it can operate properly on Python 3.8 or 3.9 as well.
### Install Requirements

run

```
pip install -r reqirements.txt
```

## To use

### Modify the constraints

Modify the constraints settings within `config/constraints.hjson`

### Modify the mineral contents

Modify the mineral settings within `mineral.csv` (You may use the Excel, but notice that **This file is decoded by GB2312(Chinese), if you want another decoding style, please manually modify the line 53 in `src/run.py` to `with open(path, 'r', encoding='<what-decoder-you-like>') as form:`**)

### Execute

run `python src/run.py` in the root dictionary.


## License

This repository is under the license of GPL 3.0.

You may copy and use the repo for commercial, but every copy of your favor must be open-source. This project is used for study and communication, and also going to be published with a paper. If you want further instruction, please follow the requirements of the institude that provides this repository. 