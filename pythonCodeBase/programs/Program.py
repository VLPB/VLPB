"""

.. module::programs

.. moduleauthor:: Jetse Jacobi <jetsejacobi@gmail.com>
"""
import os
from VlpbConfig import Configuration,Logger
from subprocess import Popen, PIPE

class Program(object):
    """The Program is a class which represents a program.
    All information the programs need are set to class variables in the constructor of the program class.
    """
    config=Configuration.Config()
    logger=None
    
    def __init__(self, outputDir, refGenome=None, libName="unknown"):
        """The constructor of program sets the arguments which the most of the programs need. A sub directory is created for the library.
        
        :param outputDir: The output directory where to write all files too
        :type outputDir: str.
        :param refGenome: The reference genome, needed by many programs but not all, so default is set to None
        :type refGenome: str.
        :param libName: The name of the library
        :type libName: str.
        
        """
        
        if Program.logger == None:
            Program.logger = Logger.Logger(outputDir + "/" + libName + ".log")
        self.outputDir = outputDir
        self.refGenome = refGenome
        self.libName = libName
        #TODO improve to get directory of getOutputFile
        if not os.path.exists(outputDir + "/" + libName):
            os.makedirs(outputDir + "/" + libName)
    
    def getOutputFile(self, progressSuffix):
        """This method gets the output fileName
        
        :param progressSuffix:The name of the progessSuffix represents the part where the file is in the pipeline
        :type progressSuffix: one of these suffices:
        - '.tar.gz' or '.gz': The file is compressed, only can contain one fq file! 
        - '.fq' fastq format without quality control
        - 'Hq.fq' fastq format where quality control is done
        - '.sam' sam file
        - '.bam' unsorted bam file
        - 'Sorted.bam' The bam file is sorted
        - 'WithHeader.bam' The bam file can be used for GATK
        
        """
        return self.outputDir + "/" + self.libName + "/" + self.libName+ progressSuffix
    
    def execute(self, command, outputFile, programName):
        """This method executes the command created by its children
        
        :param command: The command to execute
        :type command: str.
        :param outputFile: The output file which will be checked if already exists, also will be added to the :class:`.GarbageCollector`
        :type outputFile: str.
        
        """
        
        self.logger.nextProgram(programName, command)
        if self.checkProgramExecuted(outputFile):
            self.logger.logOut("Output of command: " + command + "already executed.\nSkipping this command")
        else:
            print("executing: " + programName)
            error,output = Popen(command, shell=True, stdout=PIPE, stderr=PIPE).communicate()
            self.logger.logOut(output)
            self.logger.logError(error)
            print("Finished!\n")

    def checkProgramExecuted(self, outputFile):
	if os.path.isfile(outputFile):
	    if os.path.getsize(outputFile) > 10:
		return True
	return False

