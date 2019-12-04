// INFORMATION--------------------------------------------------------------------------
// DEVELOPER:        Anthony Harris
// SLATE:            Anthony999
// DATE:             04 December 2019
// PURPOSE:          Use the K Nearest Neighbors algorithm to classify entries of the
//                   CNRPark dataset.
//--------------------------------------------------------------------------------------

// /\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\

// IMPORTS------------------------------------------------------------------------------
using System;
using System.Collections.Generic;
using System.IO;
//--------------------------------------------------------------------------------------

namespace CSharpParkingSpaceClassification
{
    class Program
    {
        // GLOBALS------------------------------------------------------------------------------
        static List<Tuple<List<double>, int>> trainingDataSet = new List<Tuple<List<double>, int>>();
        static List<Tuple<List<double>, int>> testDataSet = new List<Tuple<List<double>, int>>();
        static string lot = "A";    // Specifies which lot in the dataset to use
        static int trainSize = 100; // Size of training dataset
        static int testSize = 100;  // Size of testing dataset
                                    // ----------------------------------------------------------

        // /\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\

        //  FUNCTION DESCRIPTION-----------------------------------------------------------------
        //  Function Name:  collectData
        //  Parameters:     fileName
        //                      Use:    Used as the name of the file containing the current 
        //                              dataset
        //                  dataSet(either the Training or the Test dataset)
        //                      Use:    Simply represents the desired dataset to work with
        //                  sizeOfDataSet
        //                      Use:    Represents desired number of entries in the data set
        //                  startFromBeginning
        //                      Use:    Specifies whether entries should be selected from the 
        //                              beginning or the end of the data set
        //  Returns:          N/A
        //  Description:    Performs file handling and converts the data from the file into
        //                  a format that is easy to work with
        // --------------------------------------------------------------------------------------
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
        // --------------------------------------------------------------------------------------

        // /\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\

        // FUNCTION DESCRIPTION-----------------------------------------------------------------
        // Function Name:   Main
        // Parameters:      N/A
        // Returns:         N/A
        // Description:     The starting point of the program. Controls the progression of the
        //                  program and displays some relevant information to the screen
        // --------------------------------------------------------------------------------------
        static void Main(string[] args)
        {
            Console.WriteLine("Collecting Training Data, Please Wait. . .");
            CollectData("CNRPARK-Patches-150x150-Grayscale/" + lot, ref trainingDataSet, trainSize, true);
            Console.WriteLine("Training Data Collection Successful.");

            Console.WriteLine();

            Console.WriteLine("Collecting Testing Data, Please Wait. . .");
            CollectData("CNRPARK-Patches-150x150-Grayscale/" + lot, ref testDataSet, testSize, false);
            Console.WriteLine("Testing Data Collection Successful.");

            Console.WriteLine();

            for (int neighborCount = 1; neighborCount <= (int)Math.Sqrt(trainingDataSet.Count); ++neighborCount)
            {
                for (int powLevel = 1; powLevel <= 5; ++powLevel)
                {
                    KNN_Parking iteration = new KNN_Parking(lot, ref trainingDataSet, ref testDataSet, neighborCount, powLevel);
                    iteration.RunKNN();
                    Console.WriteLine();
                }
            }
        }
        // --------------------------------------------------------------------------------------
    }
}
