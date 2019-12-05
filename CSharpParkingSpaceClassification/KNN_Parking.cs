// INFORMATION--------------------------------------------------------------------------
// DEVELOPER:        Anthony Harris
// SLATE:            Anthony999
// DATE:             04 December 2019
// PURPOSE:          Act as KNN algorithm implementation
//--------------------------------------------------------------------------------------

// /\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\

// IMPORTS------------------------------------------------------------------------------
using System;
using System.Collections.Generic;
using System.Text;
using System.IO;
//--------------------------------------------------------------------------------------

// /\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\

namespace CSharpParkingSpaceClassification
{
    // 
    public class KNN_Parking
    {
        // Define the Global Scope variables
        List<Tuple<List<double>, int>> trainingDataSet;
        List<Tuple<List<double>, int>> testDataSet;
        List<int> classifications = new List<int>();
        int K_NumberOfNeighbors;
        int power = 2;
        int numCorrect = 0;
        int numIncorrect = 0;
        double accuracy;
        string lot;

        // Constructor
        public KNN_Parking(
                    string lotChoice,
                    ref List<Tuple<List<double>, int>> train, 
                    ref List<Tuple<List<double>, int>> test,
                    int K_Num, int pow)
        {
            trainingDataSet = train;
            testDataSet = test;
            K_NumberOfNeighbors = K_Num;
            power = pow;
            lot = lotChoice;
        }

        // FUNCTION DESCRIPTION-----------------------------------------------------------------
        // Function Name:    distanceMeasure
        // Parameters:  entry1
        //                  Use:    Represents an entry in the trainingDataSet for use in
        //                          calculating the distance between it and entry2
        //              entry2
        //                  Use:    Represents the current entry of the testDataSet for use
        //                          in calculating the distance between it and entry1
        // Returns:          A floating point representation of the 'distance measure' of the
        //                   2 entries.
        // Description:      For each element e of the entries, find the summation of the 
        //                   absolute value of the difference bewteen e1 and e2 and then take
        //                   the Nth root of that sum
        //--------------------------------------------------------------------------------------
        double DistanceMeasure(Tuple<List<double>, int> entry1, Tuple<List<double>, int> entry2)
        {
            double currentSum = 0;
            for (int index = 0; index < entry1.Item1.Count; ++index)
            {
                currentSum += Math.Pow(Math.Abs(entry1.Item1[index] - entry2.Item1[index]), power);
            }
            return (double)Math.Sqrt(currentSum);
        }

        List<Tuple<int, double>> FindNeighbors(Tuple<List<double>, int> resident)
        {
            List<Tuple<int, double>> neighbors = new List<Tuple<int, double>>();

            for (int index = 0; index < trainingDataSet.Count; ++index)
            {
                if (neighbors.Count < K_NumberOfNeighbors)
                {
                    neighbors.Add(new Tuple<int, double>(index, DistanceMeasure(trainingDataSet[index], resident)));
                }
                else
                {
                    double currentDistance = DistanceMeasure(trainingDataSet[index], resident);
                    Tuple<int, double> currentFarthestNeighbor = neighbors[0];
                    foreach (var neighbor in neighbors)
                    {
                        if (neighbor.Item2 > currentFarthestNeighbor.Item2)
                        {
                            currentFarthestNeighbor = neighbor;
                        }
                    }
                    for (int neighborIndex = 0; neighborIndex < neighbors.Count; ++neighborIndex)
                    {
                        if (neighbors[neighborIndex].Item2 == currentFarthestNeighbor.Item2 && currentDistance < currentFarthestNeighbor.Item2)
                        {
                            neighbors.RemoveAt(neighborIndex);
                            neighbors.Add(new Tuple<int, double>(index, currentDistance));
                        }
                    }
                }
            }
            return neighbors;
        }

        //  FUNCTION DESCRIPTION-----------------------------------------------------------------
        //  Function Name:    PrintData
        //  Parameters:       index
        //                      Use:    The current entry being considered
        //  Returns:          N/A
        //  Description:      Display the formatted information to the screen
        // --------------------------------------------------------------------------------------
        void PrintData(ref int index)
        {
            Console.WriteLine("Desired Class: " + testDataSet[index].Item2.ToString() +
                                "\tComputed Class: " + classifications[index].ToString());
        }

        // FUNCTION DESCRIPTION-----------------------------------------------------------------
        // Function Name:    Classify
        // Parameters:       N/A
        // Returns:          N/A 
        // Description:      Classifies the entries in testDataSet using the KNN classification
        //                   algorithm and displays the actual and computed classes
        //--------------------------------------------------------------------------------------
        void Classify()
        {
            for (int entry = 0; entry < testDataSet.Count; ++entry)
            {
                List<List<double>> classVote = new List<List<double>>()
                {
                    new List<double>(){0, 0},
                    new List<double>(){1, 0},
                };
                List<Tuple<int, double>> neighbors = FindNeighbors(testDataSet[entry]);

                foreach (var neighbor in neighbors)
                {
                    foreach (var classLabel in classVote)
                    {
                        if (classLabel[0] == trainingDataSet[neighbor.Item1].Item2) classLabel[1] += 1 / neighbor.Item2;
                    }
                }

                double maxVoteWeight = double.MinValue;
                int finalVote = -1;
                foreach (var vote in classVote)
                {
                    if (vote[1] > maxVoteWeight)
                    {
                        maxVoteWeight = vote[1];
                        finalVote = (int)vote[0];
                    }
                }
                classifications.Add(finalVote);

                if (finalVote == testDataSet[entry].Item2) ++numCorrect;
                else ++numIncorrect;

                PrintData(ref entry);
            }
        }

        // FUNCTION DESCRIPTION-----------------------------------------------------------------
        // Function Name:    SaveData
        // Parameters:       N/A
        // Returns:          N/A 
        // Description:      Saves the results in a .csv file
        //--------------------------------------------------------------------------------------
        void SaveData()
        {
            string filePath = @"./../../../PostResults/lot" + lot + "_train_" + 
                trainingDataSet.Count.ToString() + "-test_" + testDataSet.Count.ToString() + ".csv";
            string delimiter = ",";
            if (!File.Exists(filePath))
            {
                List<string> labels = new List<string>()
                {
                    "Train Size",
                    "Test Size",
                    "K",
                    "Power",
                    "Correct",
                    "Incorrect",
                    "Accuracy"
                };
                string result = "";
                for (int index = 0; index < labels.Count; ++index)
                {
                    if (index != 0) result += delimiter;
                    result += labels[index];
                }
                File.WriteAllLines(filePath, new List<string>() { result });
            }
            List<string> output = new List<string>()
                {
                    trainingDataSet.Count.ToString(),
                    testDataSet.Count.ToString(),
                    K_NumberOfNeighbors.ToString(),
                    power.ToString(),
                    numCorrect.ToString(),
                    numIncorrect.ToString(),
                    accuracy.ToString()
                };
            string line = "";
            for (int index = 0; index < output.Count; ++index)
            {
                if (index != 0) line += delimiter;
                line += output[index];
            }
            File.AppendAllLines(filePath, new List<string>() { line });
        }

        // FUNCTION DESCRIPTION-----------------------------------------------------------------
        // Function Name:    RunKNN
        // Parameters:       N/A
        // Returns:          N/A 
        // Description:      Starts the algorithm
        //--------------------------------------------------------------------------------------
        public void RunKNN()
        {
            Console.WriteLine("Now beginning display of KNN algorithm information:");
            Console.WriteLine("K = " + K_NumberOfNeighbors.ToString());
            Console.WriteLine("Power = " + power.ToString());

            Console.WriteLine();

            Classify();

            Console.WriteLine();

            int total = numCorrect + numIncorrect;
            accuracy = (double)numCorrect / (double)total;
            Console.WriteLine("Accuracy: " + accuracy.ToString());
            Console.WriteLine("Number correctly classified: " + numCorrect.ToString());
            Console.WriteLine("Number incorrectly classified: " + numIncorrect.ToString());
            Console.WriteLine("Total: " + total.ToString());

            SaveData();
        }
    }
}
