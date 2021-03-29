#!/usr/bin/python3

import argparse
import multiprocessing
import os
import timeit
from concurrent.futures import ThreadPoolExecutor

# Amhald's law
max_threads = multiprocessing.cpu_count() * 2 + 1


# TODO: Pytest case

class AtbashCipher:
    """Argument parse will process command line argument, and read method will
    be called to read data and pass each string to encrypt method and weite the output
    using write_file method"""

    def __init__(self, infile, outfile, concurrent=True):
        """Initialize arguments from arg parser
        :param infile:
        :param outfile:
        :param concurrent:
        """
        self.in_file = infile
        self.out_file = outfile
        self.concurrent = concurrent

    def validate_input(self):
        """
        validate input and check whether both input and output file is valid
        1) Check whether infile exists and is readable
        2) Input data is a string
        3) Output file is writable
        :return:
        """
        if not os.path.isfile(self.in_file):
            print("input file not exits, please check input")
            return False
        ifptr = open(self.in_file, "r")
        if not ifptr.readable():
            print("input file is not readable")
            return False
        ofptr = open(self.out_file, "w")
        if not ofptr.writable():
            print("outfile file not exits, please check input")
            return False
        return True

    @staticmethod
    def encrypt(in_str: str):
        """
        TODO: Multithreading
        encrypt input string and return output
        :param in_str:
        :return:
        """
        out_str = ''
        for i in in_str:
            if ord(i) in range(97, 123):
                out_str += chr(96 + (26 - (ord(i) - ord('a'))))
            elif ord(i) in range(65, 91):
                out_str += chr(64 + (26 - (ord(i) - ord('A'))))
            else:
                out_str += i
        return out_str

    def execute(self):
        """
        read input file and return data as generator
        :return:
        """
        with open(self.out_file, 'w') as outfile:
            with open(self.in_file, 'r') as infile:
                if self.concurrent:
                    # concurrent execution
                    with ThreadPoolExecutor(max_workers=max_threads) as executor:
                        for line in infile:
                            future = executor.submit(self.encrypt, line)
                            output_str = future.result()
                            outfile.write(output_str)
                else:
                    # sequential execution
                    for line in infile:
                        output_str = self.encrypt(line)
                        outfile.write(output_str)
            infile.close()
        outfile.close()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Take file in input.')
    parser.add_argument('--infile', dest='infile', type=str, help='input file path to read data')
    parser.add_argument('--outfile', dest='outfile', type=str, help='output file to write encryption')
    parser.add_argument('--concurrent', required=False, dest='concurrent', type=bool,
                        help='provide flag for sequential, concurrent execution')
    parser.set_defaults(concurrent=True)
    args = parser.parse_args()
    # validate input
    start_time = timeit.default_timer()
    atbash_cipher = AtbashCipher(args.infile, args.outfile, args.concurrent)
    if atbash_cipher.validate_input():
        atbash_cipher.execute()
        print("program executed successfully, output file: {}".format(args.outfile))
    else:
        print("invalid input, please check inout and out file")
    print("Time taken by program to execute : {} seconds".format(timeit.default_timer() - start_time, '.3f'))
