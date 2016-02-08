import glob
import os

class_files = glob.glob("tmp/*/")
class_files += glob.glob("tmp2/*/")

class_files = [i+"classification.txt" for i in class_files]

class_files.sort()
for i in class_files:
    print(i)
for name in class_files:
    f = open(name, 'w')
    print(name.split('/')[1])
    for i in range(1, 13):
        r = input("{}: ".format(i))
        f.write("{} {}\n".format(i, r))
    f.close()
