import sys
import os
from programs import SnvCaller 



'''
The main method is the main flow of the whole program
'''

def main():
    print("###############################################################################\n")
    print("input file: " + inputFile)
    print("reference genome: " + refGenome)
    print("output directory: " + outDir)
    print("library: " + libName)
    print("\n###############################################################################\n")

    if not os.path.exists(outDir):
	os.makedirs(outDir)
    snvCaller= SnvCaller.SnvCaller(outDir, refGenome, libName)
    snvCaller.samtoolsMpileup(inputFile)


'''
Check input parameters
'''
if len(sys.argv) < 5:
    print("USAGE: python __init__.py <inputFile> <reference genome> <output directory> <library name>")
    sys.exit(1)
elif sys.argv[1] == "-h" or sys.argv[1] == "--help":
    print("USAGE: python __init__.py <inputFile> <reference genome> <output directory> <library name>\n")
    print("InputFile\t\t a fastq file with extension .fq or a compressed (.tar.gz or .gz) file.") 
    print("\t\t\t\t Also files created by the pipeline can be used as input for next analysis (without changing the names!")
    print("Reference genome\t The reference genome to use as a reference for mapping/snp calling/haplotyping and phenotyping")
    print("Output directory\t The directory where to write the output to, a sub directory for the library will be made")
    print("Library name\t The name of the library...")
else:
    inputFile = sys.argv[1]
    refGenome = sys.argv[2]
    outDir = sys.argv[3]
    libName = sys.argv[4]
    main()

