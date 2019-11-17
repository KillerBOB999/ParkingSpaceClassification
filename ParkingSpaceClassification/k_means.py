import ParkingLot
import random
import os
import math

##------------------------------------
## Function to load input data
## @file_name = the input file name to be loaded
##------------------------------------

##------------------------------------
## Function that contains the main loop for the program
## @input_data = the input data array
##------------------------------------
def KMeansMainLoop(input_data, data_set):

#---- Sets average and old_average to negative values for future use
#----   @average is the current average
#----   @old_average is the prior iterations average
    average = -1
    old_average = -2
    print(average)
#---- Creates a random mean for each cluster
    original_means = CreateRandomClustersMeans(0,255)
    means_of_current_clusters = original_means

#---- If the old_average and average are equal no change happend and the loop breaks
    while average != old_average:
        old_average = average

#---- Getting new means for clusters and reassigns objeects to clusters
        means_of_current_clusters,average = AssignClusters(input_data, means_of_current_clusters,data_set)
        print(average)
    DisplayOutput(input_data,means_of_current_clusters,data_set,original_means)
    
##------------------------------------
## Function that creates random clusters to start the loop
## @input_data = the input data array
## @means_of_current_clusters is the previous iteration's means
##------------------------------------   
def DisplayOutput(input_data,means_of_current_clusters,data_set, original_means):
    
#---- Beginning of iteration over the different clusters
    final = []
    for y in range(2):
        results = {"True":0,"False":0}
        final.append(results)
#---- Iteration over the input objects to determine their final cluster
    for y in range(2):
        for x in range(len(input_data)-1):
            if input_data[x][2] == y:
                final[y][str(data_set.getListOfParkingSpaces()[x].getActual())] += 1
        if final[y]["False"] > final[y]["True"]:
            final[y]["Final"] = False
        else:
            final[y]["Final"] = True
    temp_list = data_set.getListOfParkingSpaces()
    for y in final:
        for x in range(len(input_data)-1):
            if input_data[x][2] == y:
                data_set.setEstimatedOnParkingSpace(temp_list[input_data[x][3]],y["Final"])
    print(final)
    for x in data_set.getListOfParkingSpaces():
        print(str(x.getActual())+" "+str(x.getEstimated()))

#---- Beginning of printing results

    print("=====================")
    print("Accuracy rate is ",end="")
    print(data_set.getAccuracy())
##------------------------------------
## Function that creates random clusters to start the loop
## @input_data = the input data array
## @min = the smallest value in the input objs
## @max = the max value of the input objs
##------------------------------------
def CreateRandomClustersMeans(min,max):
    
#---- Sets the cluster mean value
    means_of_clusters = [[[],0],[[],0]]
    for x in range(2):
        for y in range(22500):
            means_of_clusters[x][0].append(random.randint(min,max))
    return means_of_clusters

##------------------------------------
## Reassigns the objects to the nearest cluster and recalculates means
## @input_data = the input data array
## @means_of_current_clusters is the previous iteration's means
##------------------------------------
def AssignClusters(input_data,means_of_current_clusters,data_set):
#---- Create new cluster array for next iteration  
    new_clusters = [[[],0],[[],0]]
    for x in range(22500):
        new_clusters[0][0].append(0)
        new_clusters[1][0].append(0)
    for x in range(0,len(input_data)):
        closest_cluster = -1
#---- Iterates over input objs and finds the closest cluster
        sum_one = 0
        sum_two = 0
        for z in range(0,len(input_data[x][0])):
            temp = input_data[x][0][z]
            sum_one += abs(temp-means_of_current_clusters[0][0][z])
            sum_two += abs(temp-means_of_current_clusters[1][0][z])

        if sum_one < sum_two:
            closest_cluster = 0
        else:
            closest_cluster = 1
        input_data[x][2] = closest_cluster
#---- Adds values to find the average
        for q in range(22500):
            new_clusters[closest_cluster][0][q] += input_data[x][0][q]
        new_clusters[closest_cluster][1] = 1 + new_clusters[closest_cluster][1]

#---- Calculating the average of the mean's objs    
    average = 0
    sum = 0

    if new_clusters[1][1] != 0 and new_clusters[0][1] != 0:
        for x in new_clusters:
            for q in range(22500):
                sum+=x[0][q]
                x[0][q] = x[0][q] / x[1]
        average = (sum/2)/new_clusters[0][1]+new_clusters[0][1]
    return new_clusters,average
##------------------------------------
## Main Function
##------------------------------------
def main():
    
    path = os.getcwd() + "\CNRPARK-Pathces-150x150-Grayscale\A"
    parking_lot = ParkingLot.ParkingLot(path,100)
    list_of_parkingspots = parking_lot.getListOfParkingSpaces()
#---- Begin main loop for K Means Algorithm
    input_data = []
    i = 0
    for x in parking_lot.getListOfParkingSpaces():
        input_data.append([x.getPixels(),0,0,i])
        i+=1
    KMeansMainLoop(input_data,parking_lot)

#---- End function
main()