import random
import argparse
import nltk
from nltk.corpus import words

# Intentar cargar el corpus de palabras, y si no está disponible, descargarlo
try:
    word_list = words.words()
except LookupError:
    print("Words corpus not found. Downloading...")
    nltk.download('words')
    word_list = words.words()

# -o or --output: Specify the output file name (default is wordcount.txt).
# -l or --lines: Specify the number of lines (default is 1,000,000).
# -w or --words: Specify the number of words per line (default is 10).
# -r or --range: Specify the word length range with two integers, e.g., 3 10 for lengths between 3 and 10 characters (default is [3, 10]).
# examples
# Generate with default values:
    # python dynamicGenerator.py
# Generate a file with 500,000 lines and 20 words per line:
    # python dynamicGenerator.py -l 500000 -w 20
# Generate with custom word length range (5 to 15 characters):
    # python dynamicGenerator.py -r 5 15
# Specify a custom output file:
    # python dynamicGenerator.py -o my_wordcount.txt
    
class WordCountFileGenerator:
    def __init__(self, output_file, num_lines, words_per_line):
        self.output_file = output_file
        self.num_lines = num_lines
        self.words_per_line = words_per_line
        self.word_list = word_list  # Lista de palabras en inglés

    def generate_line(self):
        # Generar una línea con palabras aleatorias del diccionario inglés
        return ' '.join(random.choice(self.word_list) for _ in range(self.words_per_line))

    def dynamicGenerator_file(self):
        # Escribir el archivo con las palabras generadas
        with open(self.output_file, "w") as f:
            for _ in range(self.num_lines):
                f.write(self.generate_line() + "\n")
        print(f"Generated {self.output_file} with {self.num_lines} lines.")

def main():
    # Configuración del parser de argumentos
    parser = argparse.ArgumentParser(
        description="Generate a large dynamic wordcount.txt file with real English words."
    )
    
    parser.add_argument(
        "-o", "--output",
        type=str,
        default="/tmp/hadoop/wordcount.txt",
        help="Output file name (default: wordcount.txt)"
    )
    
    parser.add_argument(
        "-l", "--lines",
        type=int,
        default=1000000,
        help="Number of lines in the file (default: 1,000,000)"
    )
    
    parser.add_argument(
        "-w", "--words",
        type=int,
        default=10,
        help="Number of words per line (default: 10)"
    )
    
    args = parser.parse_args()
    
    # Instanciar la clase y generar el archivo
    generator = WordCountFileGenerator(args.output, args.lines, args.words)
    generator.dynamicGenerator_file()

if __name__ == "__main__":
    main()