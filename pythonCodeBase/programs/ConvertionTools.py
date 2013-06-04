'''
Created on May 31, 2013

@author: Jetse
'''
from programs import Program, Mapper
import os

class ConvertionTools(Program.Program):
    """The class ConvertionTools regulates the support between the mappers and the programs for SV calling.
    
    """
    
    def sortBam(self, inputFile):
        """The method sortBam sorts a bam file, if the input file is not a bam file, the file will be converted to a bam file.
        
        :param inputFile: the bam file which has to be sorted
        :type inputFile: str. -- the path to this file
        :returns: str. -- the sorted bam file
        
        """
        
        if inputFile.endswith(".bam") == False:
            inputFile = self.convertToBam(inputFile)

        outputFile = self.getOutputFile("Sorted")
        cmd = Program.Program.config.getProgramPath("samtools") + " sort " + inputFile + " " + outputFile
        self.execute(cmd, outputFile, "samtools sort")
        return outputFile + ".bam"
        
    def convertToBam(self, inputFile):
        """The method convertToBam converts a sam file to a bam file, if the file is not a sam file, the file first will be mapped
        
        :param inputFile: the sam file which has to be converted to a bam file
        :type inputFile: str. -- the path to this file
        :returns: str. -- the created bam file
        
        """
        
        if inputFile.endswith(".sam") == False:
            mapper = Mapper.Mapper(self.outputDir, self.refGenome, self.libName)
            inputFile = mapper.executeBwa(inputFile)

        outputFile = self.getOutputFile(".bam")
        cmd = Program.Program.config.getProgramPath("samtools") + " view -bS " + inputFile + " > " + outputFile
        self.execute(cmd, outputFile, "samtools view")
        return outputFile
        
    def createBamIndex(self, inputFile):
        """creates a bam index file for the sorted bam file, if its not a sorted bam file, the file will be sorted
        
        :param inputFile: the sorted bam file which has to be indexed
        :type inputFile: str. -- the path to this file
        :returns: str. -- the sorted bam file
        
        """
        
        if inputFile.endswith("Sorted.bam") == False:
            inputFile = self.sortBam(inputFile)

        cmd = Program.Program.config.getProgramPath("samtools") + " index " + inputFile
        self.execute(cmd, self.getOutputFile("Sorted.bam.bai"), "samtools index")
        return inputFile
    
    def addHeaderLine(self, inputFile):
        """Adds a header line to a bam file
        
        :param inputFile: the sorted bam file with index where the header has to be added to
        :type inputFile: str. -- the path to this file
        :returns: str. -- the bam file with the new header line
        """
        if os.path.isfile(inputFile + ".bai") == False:
            inputFile = self.createBamIndex(self, inputFile)
        
        outputFile = self.getOutputFile("Wh.bam")
        cmd = "java -jar " + Program.Program.config.getProgramPath("picardTools") + "AddOrReplaceReadGroups.jar I=" + inputFile + " O=" + outputFile + " LB=" + self.libName + " PL=illumina PU=lane SM=samplename"
        self.execute(cmd, outputFile, "picardtools AddOrReplaceReadGroups")
        return outputFile
        
        
        
