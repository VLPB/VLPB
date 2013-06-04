from programs import Program, Decompressor

class QualityControl(Program.Program):
    """The class qualityControl regulates all processes which have to do with the quality control.
    
    .. module:: programs
    .. moduleauthor:: Jetse Jacobi
    """
    
    def doQualityControl(self, inputFile):
        """The method doQualityControl checks whether the input is a fastq file, if not the file first will be extracted.
         After this this method does a quality control on the fastq file
        
        :param inputFile: The .fq file where to do a quality control on
        :type inputFile: str. -- the path to this file
        :returns: str. -- The path to file with high quality reads
        
        """
        if inputFile.endswith(".fq") == False:
            decompressor = Decompressor.Decompressor(self.outputDir, self.refGenome, self.libName)
            inputFile = decompressor.extract(inputFile)
        outputFile = self.getOutputFile("Hq.fq")
        self.execute("cp " + inputFile + " " + outputFile, outputFile, "qc (not yet implemented, just copying...)")
        return outputFile