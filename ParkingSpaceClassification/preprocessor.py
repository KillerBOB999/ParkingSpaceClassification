import os
import imageio
import random
import csv

def getItems(root):
    res = []
    for subdir, dirs, files in os.walk(root):
        temp = []
        for file in files:
            if file[-4:] == '.jpg':
                path = os.path.join(subdir, file)         
                temp.append(path)    
        for x in temp:
            res.append(x)
    return res

def main():
    root = os.getcwd() + "/CNRPARK-Patches-150x150"
    count = 0
    list_of_paths = getItems(root)
    for index in range(0, len(list_of_paths)):
        newFile = list_of_paths[index].replace("CNRPARK-Patches-150x150", "CNRPARK-Pathces-150x150-Grayscale")
        newFile = newFile.replace(".jpg", ".csv")
        with open(newFile, "w", newline='') as csv_file:
            writer = csv.writer(csv_file, delimiter=',')
            res = []
            if "busy" in list_of_paths[index]:
                res.append("Occupied")
            else:
                res.append("Available")

            pixel_list = imageio.imread(list_of_paths[index])
            if pixel_list.shape == (150, 150, 3):
                for x in pixel_list:
                    for z in x:
                        res.append((float(z[0])+float(z[1])+float(z[2]))/3)
            else:
                continue
            print("Writing entry #", count)
            writer.writerow(res)
            count += 1

main()