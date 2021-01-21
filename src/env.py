import platform
import os
import sys
import logging

logging.getLogger().setLevel(logging.DEBUG)
#logging.getLogger().setLevel(logging.INFO)

def verifyPlatform():
    thisPlatform = platform.architecture()
    if thisPlatform[1] != "WindowsPE":
        logging.fatal(
            f"检测到您的运行系统为{platform.platform()}，本程序暂时只支持在Windows系统中运行，请部署虚拟环境或尝试自行配置线性优化器。"
        )
        return None
    else:
        if thisPlatform[0] == "32bit":
            logging.info(
                f"检测到您的运行环境为32位Windows系统：{platform.platform()}, Python版本为：{platform.python_version()}。"
            )
            return 'w32'
        elif thisPlatform[0] == "64bit":
            logging.info(
                f"检测到您的运行环境为64位Windows系统：{platform.platform()}, Python版本为：{platform.python_version()}。"
            )
            return 'w64'
        else:
            logging.warning(
                f"检测到您的运行环境为未知的Windows系统：{platform.platform()}, Python版本为：{platform.python_version()}，可能暂不受支持。"
            )
            return None

def getPath():
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    logging.debug(f"[BASE-PATH]{BASE_DIR}")
    return BASE_DIR

def pathSetup():
    version = verifyPlatform()
    if version != None:
        GLPK_DIR = os.path.join(getPath(),'utils','glpk-4.65',version)
    if GLPK_DIR not in sys.path:
        logging.debug("[CONFIRMED] Already Setup.")
        return
    else:
        logging.debug("[NEWLY-SETUP] Appending to the system path.")
        sys.path.append(GLPK_DIR)
        return


if __name__ == "__main__":
    #getPath()
    pathSetup()
    pass