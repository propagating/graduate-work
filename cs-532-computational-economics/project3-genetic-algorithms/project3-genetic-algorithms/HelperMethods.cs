using System;
using System.Collections.Generic;

namespace project3_genetic_algorithms
{
    public static class HelperMethods
    {
        private static Random rand = new Random();
        public static double RandomNumberBetween(double minValue, double maxValue)
        {
            var next = rand.NextDouble();

            return minValue + (next * (maxValue - minValue));
        }

        public static IEnumerable<IEnumerable<T>> UniquePairs<T>(List<T> arr)
        {

            for(var i=0;i<arr.Count;i++)
            {
                for(var j=i+1;j<arr.Count;j++)
                {
                    yield return new[]{ arr[i],arr[j] };
                }
            }
        }
    }
}
