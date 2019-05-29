from xml.etree import ElementTree as et
import os
path = '.'

for filename in os.listdir(path):
    if not filename.endswith('.xml'): continue
    tree = et.parse(filename)
    fullname = os.path.dirname(os.path.abspath(filename))
    x = filename.split(".")
    x[1] = "jpg"
    tree.find('path').text = fullname + "\\" + str(x[0]) + "." + str(x[1])
    tree.write(filename)


