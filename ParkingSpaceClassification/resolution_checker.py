import os
import imageio
root = "D:\CSC_535\Final_Project\Data_Set\ParkingSpaceClassification\ParkingSpaceClassification\CNRPARK-Patches-150x150"
res = {}
count = 0
for subdir, dirs, files in os.walk(root):
    temp = []
    for file in files:
        if file[-4:] == '.jpg':
            path = os.path.join(subdir, file)         
            temp = imageio.imread(path)
            if str(temp.shape) in res:
                res[str(temp.shape)] = res[str(temp.shape)] +1
            else:
                res[str(temp.shape)] = 1
            count +=1
print(res)
print("Total number of files = "+str(count))