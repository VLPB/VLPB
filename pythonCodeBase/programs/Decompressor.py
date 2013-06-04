from programs import Program

class Decompressor(Program.Program):
    """The Decompressor class regulates all Decompress functions
    
    .. module:: programs
    
    .. moduleauthor:: Jetse Jacobi
    
    """    
    def extract(self, inputFile):
        """This function calls extractGz if the file .gz compressed, if this file is .tar.gz is compressed, the method extractTarGz is called
        
        :param inputFile: The compressed .gz or . tar.gz file which has te be extracted
        :type inputFile: str. -- the path to this file
        :returns: str. -- The path to the extracted file
        :raises: TypeError -- When the file type is not recognized
        """
        if inputFile.endswith(".gz"):
            return self.extractGz(inputFile)
        elif inputFile.endswith(".tar.gz"):
            return self.extractTarGz(inputFile)
        else:
            raise TypeError("Unrecognized file format!")
    
    def extractGz(self, inputFile):
        """This function extracts the .gz compressed file
        
        :param inputFile: The .gz file to extract
        :type inputFIle: str.
        :returns: str. -- The path to the extracted file
        
        """
        outFile = self.getOutputFile(".fq")
        cmd = "gunzip -c " + inputFile + " > " + outFile
        self.execute(cmd, outFile, "gunzip")
        return outFile
    
    def extractTarGz(self, inputFile):
        """This function extracts the .tar.gz compressed file
        
        :param inputFile: The .tar.gz file to extract
        :type inputFile: str.
        :returns: str. -- The path to the extracted file
        
        """
        
        outFile = self.getOutputFile(".fq")
        cmd = "tar -xvzf " + inputFile + " -C " + outFile
        self.execute(cmd, outFile, "tar")
        return outFile
