from xml.etree import ElementTree as et
import os
path = '.'

for filename in os.listdir(path):
    if not filename.endswith('.xml'): continue
    tree = et.parse(filename)
    fullname = os.path.dirname(os.path.abspath(filename))
    print(tree.find('path').text)
    


