using System;
using System.Collections.Generic;
using System.IO;

namespace CSharpParkingSpaceClassification
{
    class Program
    {
        static List<Tuple<List<double>, int>> trainingDataSet = new List<Tuple<List<double>, int>>();
        static List<Tuple<List<double>, int>> testDataSet = new List<Tuple<List<double>, int>>();
        static List<int> classifications = new List<int>();
        static int K_NumberOfNeighbors;
        static int power = 2;
        static int numCorrect = 0;
        static int numIncorrect = 0;

        static double DistanceMeasure(Tuple<List<double>, int> entry1, Tuple<List<double>, int> entry2)
		{
			double currentSum = 0;
			for (int index = 0; index < entry1.Item1.Count; ++index)
			{
				currentSum += Math.Pow(Math.Abs(entry1.Item1[index] - entry2.Item1[index]), power);
			}
			return (double)Math.Sqrt(currentSum);
		}

        static List<Tuple<int, double>> FindNeighbors(Tuple<List<double>, int> resident)
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

        static void PrintData(ref int index)
        {
            Console.WriteLine("Desired Class: " + testDataSet[index].Item2.ToString() +
                                "\tComputed Class: " + classifications[index].ToString());
        }

        static void Classify()
        {
            for (int entry = 0; entry < testDataSet.Count; ++entry)
            {
                List<List<double>> classVote = new List<List<double>>()
                {
                    new List<double>(){0, 0},
                    new List<double>(){1, 0},
                    new List<double>(){2, 0},
                    new List<double>(){3, 0},
                    new List<double>(){4, 0},
                    new List<double>(){5, 0},
                    new List<double>(){6, 0},
                    new List<double>(){7, 0},
                    new List<double>(){8, 0},
                    new List<double>(){9, 0},
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

        static void CollectData(string fileName, ref List<Tuple<List<double>, int>> dataSet, int sizeOfDataSet, bool startFromBeginning)
        {
            System.IO.DirectoryInfo root = new DirectoryInfo(@"./../../../" + fileName);
            System.IO.FileInfo[] files = null;
            System.IO.DirectoryInfo[] subDirs = null;

            subDirs = root.GetDirectories();
            foreach (var dir in subDirs)
            {
                int entryCounter = 0;
                files = dir.GetFiles();
                if (!startFromBeginning) Array.Reverse(files);
                foreach (var file in files)
                if (entryCounter < sizeOfDataSet / 2)
                {
                    using (var reader = new StreamReader(file.ToString()))
                    {
                        var data = reader.ReadLine();
                        var values = data.Split(',');
                        List<double> pixels = new List<double>();
                        for (int i = 1; i < values.Length; ++i)
                        {
                            pixels.Add(double.Parse(values[i]));
                        }
                        int actual = -1;
                        if (values[0] == "Available")
                        {
                            actual = 1;
                        }
                        else
                        {
                            actual = 0;
                        }
                        dataSet.Add(new Tuple<List<double>, int>(pixels, actual));
                    }
                    entryCounter++;
                }
            }
        }
        static void Main(string[] args)
        {
            Console.WriteLine("Collecting Training Data, Please Wait. . .");
            CollectData("CNRPARK-Patches-150x150-Grayscale/A", ref trainingDataSet, 1000, true);
            Console.WriteLine("Training Data Collection Successful.");

            Console.WriteLine();

            Console.WriteLine("Collecting Testing Data, Please Wait. . .");
            CollectData("CNRPARK-Patches-150x150-Grayscale/A", ref testDataSet, 100, false);
            Console.WriteLine("Testing Data Collection Successful.");

            Console.WriteLine();

            K_NumberOfNeighbors = (int)(Math.Sqrt(trainingDataSet.Count) / 4);
            Console.WriteLine("Now beginning display of KNN algorithm information:");
            Console.WriteLine("K = " + K_NumberOfNeighbors.ToString());

            Console.WriteLine();
            
            Classify();
            
            Console.WriteLine();
            
            int total = numCorrect + numIncorrect;
            double accuracy = (double)numCorrect / (double)total;
            Console.WriteLine("Accuracy: " + accuracy.ToString());
            Console.WriteLine("Number correctly classified: " + numCorrect.ToString());
            Console.WriteLine("Number incorrectly classified: " + numIncorrect.ToString());
            Console.WriteLine("Total: " + total.ToString());
        }
    }
}
