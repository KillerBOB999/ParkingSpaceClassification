## Ver 1.3

import os
import imageio
import random

class ParkingSpace:
    
    def __init__(self, str):
        self.pixels = self.getPngData(str)
        self.actual = False
        self.estimated = False
    
    def getPixels(self):
        return self.pixels
    
    def getActual(self):
        return self.actual
    
    def getEstimated(self):
        return self.estimated
    
    def setActual(self, value):
        self.actual = value
    
    def setEstimated(self, value):
        self.estimated = value
    
    def getPngData(self, str):
        pixel_list = imageio.imread(str)
        if pixel_list.shape != (150, 150, 3):
            return None
        res = []
        for x in pixel_list:
            for z in x:
                temp = (float(z[0])+float(z[1])+float(z[2]))/3
                res.append(temp)
        return res
            
            
class ParkingLot:
    
    TOTAL_VERIFIED = 0
    TOTAL_COUNT = 0
    
    def __init__(self, root_dir,number_of_items_to_return):
        self.list_of_paths = self.getItems(root_dir);
        self.list_of_objs = self.getObjects(number_of_items_to_return)
        
    def getObjects(self,number_of_items_to_return):
        random.seed(0)
        random.shuffle(self.list_of_paths)
        res = []
        count = 0
        index = 0
        while count < number_of_items_to_return:
            index +=1
            parking_space = ParkingSpace(self.list_of_paths[index])
            if parking_space.getPixels() == None:
                continue
            if "busy" in self.list_of_paths[index]:
                parking_space.setActual(False)
            else:
                parking_space.setActual(True)
            ParkingLot.TOTAL_COUNT +=1
            res.append(parking_space)
            count +=1
        return res
    
    def getItems(self, root):
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
    
    def setEstimatedOnParkingSpace(self,parking_space, value):
        if parking_space.getEstimated() == value:
            return
        elif parking_space.getActual() == False and value == True:
            ParkingLot.TOTAL_VERIFIED += 1
            parking_space.setEstimated(value)
        elif parking_space.getActual() == True and value == False:
            ParkingLot.Total_VERIFIED -= 1
            parking_space.setEstimated(value)
    
    def getListOfParkingSpaces(self):
        return self.list_of_objs
    
    def getAccuracy(self):
        return ParkingLot.TOTAL_VERIFIED / ParkingLot.TOTAL_COUNT