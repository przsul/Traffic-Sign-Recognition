from xml.etree import ElementTree as et
import os
path = [".","../test"]
thisset = set([])
for xpath in path:
    for filename in os.listdir(xpath):
        if not filename.endswith('.xml'): continue
        print(xpath + "/" + filename)
        tree = et.parse(xpath + "/" + filename)
        for x in tree.findall('object/name'):
            print(x.text)
            thisset.add(x.text)
    
	
print(thisset)
print(len(thisset))

for i in thisset:
    print(i)