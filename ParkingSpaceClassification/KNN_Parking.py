#!/usr/bin/env python3

# INFORMATION--------------------------------------------------------------------------
# DEVELOPER:        Anthony Harris
# SLATE:            Anthony999
# DATE:             24 September 2019
# PURPOSE:          Use the K Nearest Neighbors algorithm to classify entries of the
#                   MNIST dataset.
#--------------------------------------------------------------------------------------

#/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\

# IMPORTS------------------------------------------------------------------------------
import sys
import numpy as np
import ParkingLot
import os
#--------------------------------------------------------------------------------------

#/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\

# GLOBALS------------------------------------------------------------------------------
trainingDataSet = [([],)]   # The dataset to be used, represented as an array of tuples
                            # are defined as (arrayOfPixelValues, class)

testDataSet = [([],)]       # The dataset to be used for testing the accuracy of the
                            # implementation. Same structure as trainingDataSet.

calculatedClass = []        # Parallel to testDataSet, represents the calculated class
                            # of the entity in the data set at the same index

K_NumberOfNeighbors = 10    # Number of neighbors for use in the KNN algorithm

power = 2                   # Power used for Minkowsky distance measurement
                            #   NOTE: 1 = Manhattan distance, 2 = Euclidian distance

numCorrect = 0              # Number of correctly labeled values

numIncorrect = 0            # Number of incorrectly labeled values
#--------------------------------------------------------------------------------------

#/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\

# FUNCTION DESCRIPTION-----------------------------------------------------------------
# Function Name:    collectData
# Parameters:       fileName(string)
#                       Use:    Used as the name of the file containing the current 
#                               dataset
#                   dataSet(either the Training or the Test dataset)
#                       Use:    Simply represents the desired dataset to work with
# Returns:          N/A
# Description:      Performs file handling and converts the data from the file into
#                   a format that is easy to work with
#--------------------------------------------------------------------------------------
def collectData(fileName, dataSet, sizeOfDataSet):
    path = os.getcwd() + fileName
    lot = ParkingLot.ParkingLot(path, sizeOfDataSet);
    for space in lot.getListOfParkingSpaces():
        dataSet.append((space.getPixels(), space.getActual()))
    dataSet.pop(0)

#/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\

# FUNCTION DESCRIPTION-----------------------------------------------------------------
# Function Name:    distanceMeasure
# Parameters:       entry1
#                       Use:    Represents an entry in the trainingDataSet for use in
#                               calculating the distance between it and entry2
#                   entry2
#                       Use:    Represents the current entry of the testDataSet for use
#                               in calculating the distance between it and entry1
# Returns:          A floating point representation of the 'distance measure' of the
#                   2 entries.
# Description:      For each element e of the entries, find the summation of the 
#                   absolute value of the difference bewteen e1 and e2 and then take
#                   the Nth root of that sum
#--------------------------------------------------------------------------------------
def distanceMeasure(entry1, entry2):
    # Temporary variables
    index = 0               # Used for iterating through the pixels of the entry
    count = len(entry1[0])  # Used to prevent memory acces violations
    currentSum = 0          # The sum at any given point in the function

    # Find the summation of the absolute value of the difference between e1 and e2
    while index < count:
        currentSum += np.power(abs(entry1[0][index] - entry2[0][index]), power)
        index += 1

    # Take the Nth root and return it
    return np.power(currentSum, 1/power)

#/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\

# FUNCTION DESCRIPTION-----------------------------------------------------------------
# Function Name:    findNeighbors
# Parameters:       resident
#                       Use:    Represents the current entry whose neighbors we are
#                               attempting to find
# Returns:          An array called neighbors, defined as an array of tuples where the
#                   tuples are as follows: 
#                       (someEntryInTheTrainingDataSet, 
#                        theDistanceMeasureBetweenThatEntryAndResident)
# Description:      Finds the neighbors of resident based upon the distance measure
#                   between resident and each entry in trainingDataSet
#--------------------------------------------------------------------------------------
def findNeighbors(resident):
    # Temporary variables
    neighbors = []      # [(trainingDataSetEntry, distanceMeasure)]
    index = 0           # For iterating through the trainingDataSet
    count = len(trainingDataSet) # For prevention of memory access violations

    # Iterate through the trainingDataSet
    while index < count:
        # If we don't have enough neighbors to consider yet
        if len(neighbors) < K_NumberOfNeighbors:
            neighbors.append((trainingDataSet[index], distanceMeasure(trainingDataSet[index], resident)))
        # We have enough neighbors, so determine which we should keep
        else:
            currentDistance = distanceMeasure(trainingDataSet[index], resident)
            currentFarthestNeighbor = neighbors[0]
            for neighbor in neighbors:
                if neighbor[1] > currentFarthestNeighbor[1]:
                    currentFarthestNeighbor = neighbor
            # Make sure neighbors has the closest entries
            for neighbor in neighbors:
                if neighbor[1] == currentFarthestNeighbor[1] and currentDistance < currentFarthestNeighbor[1]:
                    neighbors.remove(neighbor)
                    neighbors.append((trainingDataSet[index], currentDistance))
        index += 1
    return neighbors

#/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\

# FUNCTION DESCRIPTION-----------------------------------------------------------------
# Function Name:    classify
# Parameters:       N/A
# Returns:          N/A 
# Description:      Classifies the entries in testDataSet using the KNN classification
#                   algorithm and displays the actual and computed classes
#--------------------------------------------------------------------------------------
def classify():
    # Give access to global variables
    global numCorrect
    global numIncorrect
    global testDataSet
    global calculatedClass

    for i in range(0, len(testDataSet)):
        calculatedClass.append(-1)

    # Step through the testDataSet and classify each entry
    for entry in range(0, len(testDataSet)):
        # Possible classes and corresponding liklihood of entry being of that class
        classVote = [[0, 0], [1, 0]]

        # Find closes neighbors
        neighbors = findNeighbors(testDataSet[entry])

        # Based upon the neighbors, update the likelihood of each class
        for neighbor in neighbors:
            for classLabel in classVote:
                if classLabel[0] == neighbor[0][1]:
                    classLabel[1] += 1 / neighbor[1]

        # Determine the final classification
        maxVoteWeight = 0       # Likeliness of the selected classification
        finalVote = -1          # Selected classification
        for Vote in classVote:
            if Vote[1] > maxVoteWeight:
                maxVoteWeight = Vote[1]
                finalVote = Vote[0]
        calculatedClass[entry] = finalVote

        # Update computational statistics
        if finalVote == testDataSet[entry][1]:
            numCorrect += 1
        else:
            numIncorrect += 1

        # Display information
        printData(testDataSet[entry], finalVote)

#/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\

# FUNCTION DESCRIPTION-----------------------------------------------------------------
# Function Name:    printData
# Parameters:       entry
#                       Use:    The current entry being considered
#                   finalVote
#                       Use:    The computed classification of the entry
# Returns:          N/A
# Description:      Display the formatted information to the screen
#--------------------------------------------------------------------------------------
def printData(entry, finalVote):
    print("Desired class: " + str(int(entry[1])) + "\tComputed class: " + str(finalVote))

#/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\

# FUNCTION DESCRIPTION-----------------------------------------------------------------
# Function Name:    Main
# Parameters:       N/A
# Returns:          N/A
# Description:      The starting point of the program. Controls the progression of the
#                   program and displays some relevant information to the screen
#--------------------------------------------------------------------------------------
def main():
    # Give access to global variables
    global numCorrect  
    global numIncorrect

    # Do data gathering stuff
    print("Loading Training Dataset, Please Wait. . .")
    collectData("\CNRPARK-Patches-150x150-Grayscale\A", trainingDataSet, 100)
    print("Training Dataset Loaded Successfully")
    print()
    print("Loading Testing Dataset, Please Wait. . .")
    collectData("\CNRPARK-Patches-150x150-Grayscale\B", testDataSet, 100)
    print("Test Dataset Loaded Successfully")
    print()

    # Reinitialize globals to 0 for accuracy assurance
    numCorrect = 0
    numIncorrect = 0

    # Start actual information display and KNN algorithm
    print("Beginning KNN algorithm information display:")
    print("K = " + str(K_NumberOfNeighbors))
    print()
    classify()
    print()
    total = numCorrect + numIncorrect
    accuracy = numCorrect / total
    print("Accuracy: " + str(accuracy))
    print("Number correctly classified: " + str(numCorrect))
    print("Number incorrectly classified: " + str(numIncorrect))
    print("Total: " + str(total))

#/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\

main()
