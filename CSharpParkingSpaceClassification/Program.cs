using System;
using System.Collections.Generic;
using System.IO;

namespace CSharpParkingSpaceClassification
{
    class Program
    {
        static List<Tuple<List<float>, int, int>> trainingDataSet = new List<Tuple<List<float>, int, int>>();
        static List<Tuple<List<float>, int, int>> testDataSet = new List<Tuple<List<float>, int, int>>();
        static int K_NumberOfNeighbors = 10;
        static int power = 2;
        static int numCorrect = 0;
        static int numIncorrect = 0;

        static float DistanceMeasure(Tuple<List<float>, int, int> entry1, Tuple<List<float>, int, int> entry2)
		{
			float currentSum = 0;
			for (int index = 0; index < entry1[0].Count; ++index)
			{
				currentSum += Math.Pow(entry1[0][index] - entry2[0][index], power);
			}
			return Math.Pow(currentSum, 0.5);
		}

        static List<Tuple<int, float>> FindNeighbors(Tuple<List<float>, int, int> resident)
        {
            List<Tuple<int, float>> neighbors = new List<Tuple<int, float>>();

            for (int index = 0; index < trainingDataSet.Count; ++index)
            {
                if (neighbors.Count < K_NumberOfNeighbors)
                {
                    neighbors.Add(new Tuple<int, float>(index, DistanceMeasure(trainingDataSet[index], resident)));
                }
                // KEEP GOING HERE
            }

            return neighbors;
        }

        static void Classify()
        {
            foreach (var entry in testDataSet)
            {
                List<List<float>> classVote = new List<List<float>>()
                {
                    new List<float>(){0, 0},
                    new List<float>(){1, 0}
                };
                List<Tuple<int, float>> neighbors = FindNeighbors(entry);
            }
        }

        static void CollectData(string fileName, ref List<Tuple<List<float>, int, int>> dataSet, int sizeOfDataSet)
        {
            System.IO.DirectoryInfo root = new DirectoryInfo(@"./../../../" + fileName);
            System.IO.FileInfo[] files = null;
            System.IO.DirectoryInfo[] subDirs = null;

            subDirs = root.GetDirectories();
            foreach (var dir in subDirs)
            {
                int entryCounter = 0;
                files = dir.GetFiles();
                foreach (var file in files)
                {
                    if (entryCounter < sizeOfDataSet / 2)
                    {
                        using (var reader = new StreamReader(file.ToString()))
                        {
                            var data = reader.ReadLine();
                            var values = data.Split(',');
                            List<float> pixels = new List<float>();
                            for (int i = 1; i < values.Length; ++i)
                            {
                                pixels.Add(float.Parse(values[i]));
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
                            dataSet.Add(new Tuple<List<float>, int, int>(pixels, actual, -1));
                        }
                        entryCounter++;
                    }
                }
            }
        }
        static void Main(string[] args)
        {
            Console.WriteLine("Collecting Training Data, Please Wait. . .");
            CollectData("CNRPARK-Patches-150x150-Grayscale/A", ref trainingDataSet, 1000);
            Console.WriteLine("Training Data Collection Successful.");

            Console.WriteLine();

            Console.WriteLine("Collecting Testing Data, Please Wait. . .");
            CollectData("CNRPARK-Patches-150x150-Grayscale/B", ref testDataSet, 100);
            Console.WriteLine("Testing Data Collection Successful.");

            Console.WriteLine();

            Console.WriteLine("Now beginning display of KNN algorithm information:");
            Console.WriteLine("K = " + K_NumberOfNeighbors.ToString());
            Console.WriteLine();
            Classify();
            Console.WriteLine();
            int total = numCorrect + numIncorrect;
            float accuracy = (float)numCorrect / (float)numIncorrect;
            Console.WriteLine("Accuracy: " + accuracy.ToString());
            Console.WriteLine("Number correctly classified: " + numCorrect.ToString());
            Console.WriteLine("Number incorrectly classified: " + numIncorrect.ToString());
            Console.WriteLine("Total: " + total.ToString());
        }
    }
}
