import base64


def generatePSW(code):
    return bytes.decode(base64.b64encode(bytes(str(code), encoding='utf8')))


if __name__ == "__main__":
    with open("config/authcode.txt", 'r', encoding='gb2312') as c:
        print(generatePSW(str(c)))