import ParkingLot
import random
import os
import csv
import time
import sys
##------------------------------------
## Function to load input data
## @file_name = the input file name to be loaded
##------------------------------------

##------------------------------------
## Function that contains the main loop for the program
## @input_data = the input data array
##------------------------------------
def KMeansMainLoop(input_data, data_set,k):
    start = time.time()
#---- Sets average and old_average to negative values for future use
#----   @average is the current average
#----   @old_average is the prior iterations average
    average = -1
    old_average = -2
#---- Creates a random mean for each cluster
    original_means = CreateRandomClustersMeans(0,255,k)
    means_of_current_clusters = original_means

#---- If the old_average and average are equal no change happend and the loop breaks
    while average != old_average:
        old_average = average

#---- Getting new means for clusters and reassigns objeects to clusters
        means_of_current_clusters,average = AssignClusters(input_data, means_of_current_clusters,data_set,k)
    DisplayOutput(input_data,means_of_current_clusters,data_set,original_means,start,k)
    
##------------------------------------
## Function that creates random clusters to start the loop
## @input_data = the input data array
## @means_of_current_clusters is the previous iteration's means
##------------------------------------   
def DisplayOutput(input_data,means_of_current_clusters,data_set, original_means,start,k):

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
    for y in range(2):
        z = 0
        for x in data_set.getListOfParkingSpaces():
            if input_data[z][2] == y:
                data_set.setEstimatedOnParkingSpace(x,final[y]["Final"])
            z+=1
    
    field_names = ['k','number_of_samples','percentage_correct','duration','distance_type']
    dirname = os.getcwd()
    writepath = dirname + '\\postoutputlogs\\classification_log.csv'
    mode = 'a' if os.path.exists(writepath) else 'w'
    f = open(writepath, mode)
    field_names_for_log = ['name_of_file','actual','estimated']
    output_data_writer = csv.DictWriter(f, fieldnames=field_names)
    
    end = time.time()
    
    for x in final:
        output_data_writer.writerow({'number_of_samples':str(len(data_set.getListOfParkingSpaces())),'percentage_correct':str(data_set.getAccuracy()),'duration':str(end-start),'distance_type':'Manhattan','k':k})
    f.close()

    dirname = os.getcwd()
    writepath = dirname + '\\postoutputlogs\\err_log.csv'
    mode = 'a' if os.path.exists(writepath) else 'w'
    p = open(writepath, mode)
    logs_writer = csv.DictWriter(p,fieldnames=field_names_for_log)
    
    for x in data_set.getListOfParkingSpaces():
        if x.getActual() != x.getEstimated():
            logs_writer.writerow({"name_of_file":str(x.getFileName()),"actual":str(x.getActual()),"estimated":str(x.getEstimated())})
    p.close()
#---- Beginning of printing results

    print(data_set.getAccuracy())

##------------------------------------
## Function that creates random clusters to start the loop
## @input_data = the input data array
## @min = the smallest value in the input objs
## @max = the max value of the input objs
##------------------------------------
def CreateRandomClustersMeans(min,max,k):
    
#---- Sets the cluster mean value
    means_of_clusters = []
    for x in range(k):
        temp = [[],0]
        for y in range(22500):
            temp[0].append(random.randint(min,max))
        means_of_clusters.append(temp)
    return means_of_clusters

##------------------------------------
## Reassigns the objects to the nearest cluster and recalculates means
## @input_data = the input data array
## @means_of_current_clusters is the previous iteration's means
##------------------------------------
def AssignClusters(input_data,means_of_current_clusters,data_set,k):
#---- Create new cluster array for next iteration  
    new_clusters = []
    template_cluster = []
    for x in range(22500):
        template_cluster.append(0)
    for x in range(k):
        new_clusters.append([template_cluster,0])
    for x in range(0,len(input_data)):
        closest_cluster = -1
#---- Iterates over input objs and finds the closest cluster
        sum = [0]*k
        closest = 999999999999999
        for z in range(0,len(input_data[x][0])):
            temp = input_data[x][0][z]
            for o in range(len(sum)):
                sum[o] += abs(temp - means_of_current_clusters[o][0][z])
        for o in range(len(sum)):
            if sum[o] < closest:
                closest = sum[o]
                closest_cluster = o
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
    for x in new_clusters:
        average+= x[0][q]
    average = average / len(input_data)
    return new_clusters,average
##------------------------------------
## Main Function
##------------------------------------
def main():
    dirname = os.getcwd()
    for z in range(99,100):
        path = dirname + '\\CNRPARK-Patches-150x150-Grayscale\\A'
        parking_lot = ParkingLot.ParkingLot(path,z)
    #---- Begin main loop for K Means Algorithm
        input_data = []
        i = 0
        for x in parking_lot.getListOfParkingSpaces():
            input_data.append([x.getPixels(),0,0,i])
            i+=1
        for x in range(2,10):        
            KMeansMainLoop(input_data,parking_lot,x)
#---- End function
main()