## Ver 1.3

import os
import csv
import random
class ParkingSpace:
    
    def __init__(self, str, name):
        self.pixels,self.name = self.getPngData(str)
        self.actual = False
        self.estimated = None
        self.file_name = name
    
    def getName(self):
        return self.name
    
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
        contents = ""
        with open(str) as data:
            csv_reader = csv.reader(data)
            contents = next(csv_reader)
        name = contents[0]
        contents = contents[1:]
        pixel_list = (float(i) for i in contents)
        return list(pixel_list),name

    def setName(self, str):
        self.name = str
            
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
        for x in range(number_of_items_to_return):        
            parking_space = ParkingSpace(self.list_of_paths[x],self.list_of_paths[x][-30:])
            if parking_space.getName() == "Available":
                parking_space.setActual(False)
            else:
                parking_space.setActual(True)
            ParkingLot.TOTAL_COUNT +=1
            res.append(parking_space)
        return res
    
    def getItems(self, root):
        res = []
        for subdir, dirs, files in os.walk(root):
            temp = []
            for file in files:
                if file[-4:] == '.csv':
                    path = os.path.join(subdir, file)         
                    temp.append(path)    
            for x in temp:
                res.append(x)
        
        return res
    
    def setEstimatedOnParkingSpace(self,parking_space, value):
        if parking_space.getEstimated() == None:
            if value == True and parking_space.getActual() == True:
                parking_space.setEstimated(value)
                ParkingLot.TOTAL_VERIFIED +=1
            elif value == False and parking_space.getActual() == False:
                ParkingSpace.setEstimated(parking_space,value)
                ParkingLot.TOTAL_VERIFIED +=1
            else:
                parking_space.setEstimated(value)
        else:
            if parking_space.getEstimated() == True:
                if value == True and parking_space.getActual() == True:
                    return
                if value == False and parking_space.getActual() == True:
                    parking_space.setEstimated(value)
                    ParkingLot.TOTAL_VERIFIED-=1
                if value == True and parking_space.getActual() == False:
                    parking_space.setEstimated(value)
                    ParkingLot.TOTAL_VERIFIED-=1
            if parking_space.getEstimated() == False:
                if value == False and parking_space.getActual() == False:
                    ParkingLot.TOTAL_VERIFIED+=1
                    return
                elif value == True and parking_space.getActual() == False:
                    parking_space.setEstimated(value)
                    ParkingLot.TOTAL_VERIFIED-=1
                else:
                    parking_space.setEstimated(value)
        
  
        
        
    def getListOfParkingSpaces(self):
        return self.list_of_objs
    
    def getAccuracy(self):
        return ParkingLot.TOTAL_VERIFIED / ParkingLot.TOTAL_COUNT