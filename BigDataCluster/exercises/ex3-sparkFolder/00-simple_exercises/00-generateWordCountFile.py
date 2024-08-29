import sys
from pyspark.sql import SparkSession

class WordCount:
    """
    A class to perform word count on a text file using PySpark.

    Attributes:
    input_path (str): Path to the input file in HDFS.
    output_path (str): Path to the output directory in HDFS.

    Methods:
    count_words(): Reads the input file, performs the word count, and saves the results to the output file.
    """
    
    def __init__(self, input_path, output_path):
        """
        Initializes the class with input and output paths.

        Parameters:
        input_path (str): Path to the input file.
        output_path (str): Path to the output directory.
        """
        self.input_path = input_path
        self.output_path = output_path
        self.spark = SparkSession.builder.appName("WordCount").getOrCreate()

    def count_words(self):
        """
        Performs the word count on the input file and saves the results to the output directory.
        """
        # Read the input file
        text_file = self.spark.read.text(self.input_path)
        
        # Perform word count
        words = text_file.rdd.flatMap(lambda line: line.value.split(" "))
        word_counts = words.map(lambda word: (word, 1)).reduceByKey(lambda a, b: a + b)
        
        # Save the results to the output directory
        word_counts.saveAsTextFile(self.output_path)
        print(f"Word count results saved to {self.output_path}")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: wordcount.py <input_path> <output_path>")
        sys.exit(-1)

    input_path = sys.argv[1]
    output_path = sys.argv[2]

    # Create a WordCount instance and run the count_words method
    wc = WordCount(input_path, output_path)
    wc.count_words()
