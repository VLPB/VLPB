'''
Created on May 29, 2013

@author: Jetse
'''
from programs import Program, QualityControl

class Mapper(Program.Program):
    """The class Mapper regulates all mapping processes, available mapper: BWA
    
    """
    
    def executeBwa(self,inputFile):
        """The method executeBwa. If the file is not a high quality fastq file, the quality control first will be done.
        
        :param inputFile: the High quality fastq file which to map
        :type inputFile: str. -- the path to this file
        :returns: str. -- the mapped fastq file in sam format
        
        """
        if inputFile.endswith("Hq.fq") == False:
            qc = QualityControl.QualityControl(self.outputDir, self.refGenome, self.libName)
            inputFile = qc.doQualityControl(inputFile)
            
        outputFile = self.getOutputFile(".sam")
        cmd = Program.Program.config.getProgramPath("bwa") + " mem " + self.refGenome + " " + inputFile + " > " + outputFile
        self.execute(cmd, outputFile, "BWA")
        return outputFile

