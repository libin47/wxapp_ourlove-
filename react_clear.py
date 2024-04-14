import os

def check():
    file = "templates/index.html"
    with open(file, "r", encoding="utf8") as f:
        text = f.read()
    index = text.find("static/_next")
    return index


def html_rp():
    l = ["templates/index.html","templates/admin.html","templates/self.html", "templates/welcome.html","templates/show.html"]
    for file in l:
        with open(file, "r", encoding="utf8") as f:
            text = f.read()
        text = text.replace("/_next", "/static/_next")
        with open(file, "w", encoding="utf8") as f:
            f.write(text)


def replace_next(file):
    if file[-2:] != 'js' and file[-3:]!='css':
        return
    with open(file, "r", encoding="utf8") as f:
        text = f.read()
    text = text.replace("_next/static", "static/_next/static")
    with open(file, "w", encoding="utf8") as f:
        f.write(text)


def digui(l):
    for name in os.listdir(l):
        filedir = os.path.join(l, name)
        if os.path.isfile(filedir):
            replace_next(filedir)
        else:
            digui(filedir)


if __name__ == "__main__":
    if check()<0:
        html_rp()
        l = "static/_next"
        digui(l)
    else:
        print("已替换，未进行操作！")

