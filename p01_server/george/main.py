# Copyright 2013-2020 Amirhossein Vakili and Nancy A. Day

# Use this to run george at the command line as in:
# python3 commandline.py < inputfile.grg

import sys,os
import argparse

sys.path.append(os.path.abspath(os.path.dirname(__file__))+"/..")

import george.section as section


def parse_command_line():
    """Parse the command-line arguments."""
    parser = argparse.ArgumentParser(description="Strip George files of non-grg parts.")
    parser.add_argument(
        "filenames", metavar="FILE", nargs="+", help="george files to check")
    parser.add_argument(
        "-opt",
        "--dpll_optimized",
        action="store_false",
        help="run optimized DPLL function")
    return parser.parse_args()

def main():

  args = parse_command_line()  
  for filename in args.filenames:
    if not os.path.exists(filename):
        print("Filename does not exist. Quitting.\n")
        exit(1)
    f = open(filename,"r")
    data = f.read()
    f.close()
    x = section.main(data,args.dpll_optimized)
    for t in x:
        print(str(t))

if __name__ == "__main__":
    main()   
