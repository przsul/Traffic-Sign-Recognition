import os
files = []
removed = []
files = os.listdir()
i = 0
j = 1

for file in files:
  file_num = file[:-3]
  xml = file_num + "xml"
  jpg = file_num + "jpg"
  if jpg in files:
    if xml not in files:
      removed.append(file)
      os.remove(file)
      i=i+1

for file in removed:
  print(j, "-", file)
  j=j+1
print("Count:", i)