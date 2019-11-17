## Importing ParkingLot. The ParkingLot.py must be in the same directory
import ParkingLot
import os

## Creating a parkingLot object named a.
## First arguement is the path. DO NOT CHANGE THE FOLDER NAMES. it needs these to classify them
## Second arguement is the number of items to load. This is random items
## The busy and free folder names is how the py figures out what it is
path = os.getcwd() + "\CNRPARK-Pathces-150x150-Grayscale\A"
a = ParkingLot.ParkingLot(path,10)


## Iterating over the list of parkingspaces
## x is hte parkingspace
for x in a.getListOfParkingSpaces():
    ## Calling the parkinglot object to set the parkingspace object to set its value to True
    ## This is important to have the parkinglot object do this so it can keep track of the accuracy
    a.setEstimatedOnParkingSpace(x,True)
    print(x.getEstimated())
    print(x.getActual())
print(a.TOTAL_COUNT)
print(a.TOTAL_VERIFIED)
## Getting the accuracy of the parkinglot object
print(a.getAccuracy())
print(a.getListOfParkingSpaces()[0].getName())