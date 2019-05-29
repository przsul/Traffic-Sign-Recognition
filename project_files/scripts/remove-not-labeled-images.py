import os, re, sys

files = []
removed = []
files = os.listdir()
i = 0
j = 1

while True:
  option = input("\nAre you want to remove not labeled images? Y/N: ")
  no = re.search("[nN]|[nN][oO]", option)
  yes = re.search("[yY]|[yY][eE][sS]", option)

  if no != None:
    sys.exit()

  elif yes != None:
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
    sys.exit()

  else:
    print("Error: Type correct answer.")


