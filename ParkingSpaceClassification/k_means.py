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

#---- Creates a random mean for each cluster
    original_means = CreateRandomClustersMeans(0,255)
    means_of_current_clusters = original_means

#---- If the old_average and average are equal no change happend and the loop breaks
    while average != old_average:
        old_average = average

#---- Getting new means for clusters and reassigns objeects to clusters
        means_of_current_clusters,average = AssignClusters(input_data, means_of_current_clusters,data_set)
    DisplayOutput(input_data,means_of_current_clusters,data_set,original_means)
    
##------------------------------------
## Function that creates random clusters to start the loop
## @input_data = the input data array
## @means_of_current_clusters is the previous iteration's means
##------------------------------------   
def DisplayOutput(input_data,means_of_current_clusters,data_set, original_means):
    
#---- Beginning of iteration over the different clusters
    for y in range(len(means_of_current_clusters)):
        results = {}
    for x in range(len(original_means)):
        print("mean["+str(x)+"] is (("+str(original_means[x])+", ), "+str(x)+")")  
#---- Iteration over the input objects to determine their final cluster
        for x in range(len(input_data)-1):
            print(input_data[x][2])
            if input_data[x][2] == y:
                if str(str(data_set.getListOfParkingSpaces()[x].getActual())) in results:
                    results[str(str(data_set.getListOfParkingSpaces()[x].getActual()))] = 1 + results.get(str(data_set.getListOfParkingSpaces()[x].getActual()))
                else:
                    results[str(str(data_set.getListOfParkingSpaces()[x].getActual()))] = 1
        print(results)
    clusters = [[[],0,0,0],[[],0,0,0],[[],0,0,0]]


#---- Beginning of printing results
    print("Initial k means are")
    for x in range(2):
        print("mean[")
    for x in range(2):
        print("Cluster "+str(x))
        print("Size of cluster"+str(x) + " is " + str(clusters[x][1]))
        print("Cluster label: ")
        print("Number of objects misclustered in this cluster is ")


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
    means_of_clusters = []
    random.seed(0)
    for x in range(2):
        temp = []
        for y in range(22500):
            temp.append(random.uniform(min,max))
        means_of_clusters.append(temp)
    return means_of_clusters

##------------------------------------
## Reassigns the objects to the nearest cluster and recalculates means
## @input_data = the input data array
## @means_of_current_clusters is the previous iteration's means
##------------------------------------
def AssignClusters(input_data,means_of_current_clusters,data_set):
    
#---- Create new cluster array for next iteration  
    new_clusters = [[0,0],[0,0]]
    for x in range(0,len(input_data)):
        closest_cluster = -1
#---- Iterates over input objs and finds the closest cluster
            sum = 0
            sum_two = 0
            for z in range(0,len(input_data[x][0])):
                temp = input_data[x][0][z]**2 
                sum += temp + means_of_current_clusters[0][z]**2
                sum_two += temp + means_of_current_clusters[1][z]**2
            if math.sqrt(sum) < math.sqrt(sum_two):
                closest = math.sqrt(sum) 
                input_data[x][1] = closest
                closest_cluster = 0
            else:
                closest = math.sqrt(sum_two) 
                input_data[x][1] = closest
                closest_cluster = 1
        input_data[x][2] = closest_cluster
#---- Adds values to find the average
        new_clusters[closest_cluster][0] += input_data[x][1]
        new_clusters[closest_cluster][1] += 1

#---- Calculating the average of the mean's objs    
    average = 0
    if new_clusters[0][1] != 0:
        new_clusters[0][0] = new_clusters[0][0]/new_clusters[0][1]
    if new_clusters[1][1] != 0:
        new_clusters[1][0] = new_clusters[1][0]/new_clusters[1][1]
    if new_clusters[1][1] != 0 and new_clusters[0][1] != 0:
        average = new_clusters[0][0]/new_clusters[1][0]
    return new_clusters,average
##------------------------------------
## Main Function
##------------------------------------
def main():
    
    path = os.getcwd() + "\CNRPARK-Patches-150x150\A"
    data_set = ParkingLot.ParkingLot(path,10)
#---- Begin main loop for K Means Algorithm
    input_data = []
    i = 0
    for x in data_set.getListOfParkingSpaces():
        input_data.append([x.getPixels(),0,0,i])
        i+=1
    KMeansMainLoop(input_data,data_set)

#---- End function
main()