'''
Created on May 31, 2013

@author: Jetse
'''
from programs import Program, ConvertionTools
import os

class SnvCaller(Program.Program):
    """The SnvCaller class regulates all programs which can call the SNV's
    
    """
    
    def samtoolsMpileup(self, inputFile):
        """The method samtoolsMpileup calls the single nucleotide variations of a bam file with samtools mpileup.
        if the file is not a sorted and indexed bam file, the file first will be sorted
        
        :param inputFile: the sorted and indexed bam file where the SNV calling has to be called on
        :type inputFile: str. -- the path to this file
        :returns: str. -- the vcf file with all SNV's
        """
        
        if os.path.isfile(inputFile + ".bai") == False:
            converter = ConvertionTools.ConvertionTools(self.outputDir, self.refGenome, self.libName)
            inputFile = converter.createBamIndex(inputFile)
            
        outputFile = self.getOutputFile(".vcf")
        cmd = Program.Program.config.getProgramPath("samtools") + " mpileup " + inputFile + " > " + outputFile
        self.execute(cmd, outputFile, "samtools mpileup")
        return outputFile
    
    def gatk(self, inputFile):
        """The method gatk calls all single nucleotide variations of a bam file with GATK.
        If the bam file does not contain a header value with the information about the sample, platform and library, this header first will be added.
        
        :param inputFile: the sorted and indexed bam file with an information header where the SNV calling has to be called on
        :type inputFile: str. -- the path to this file
        :returns: str. -- the vcf file with all SNV's
        
        """
        
        if inputFile.endswith("Wh.bam") == False:
            converter = ConvertionTools.ConvertionTools(self.outputDir, self.refGenome, self.libName)
            inputFile = converter.addHeaderLine(inputFile)
        
        outputFile = self.getOutputFile(".vcf")
        cmd = Program.Program.config.getProgramPath("gatk") + " -T UnifiedGenotyper -R " + self.refGenome + "-I " + inputFile + " -o " + outputFile
        self.execute(cmd, outputFile, "samtools mpileup")
        return outputFile
