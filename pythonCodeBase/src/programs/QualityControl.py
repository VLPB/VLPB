from programs import Program
import os, stat

class QualityControl(Program.Program):
    """The class qualityControl regulates all processes which have to do with the quality control.
    
    """
    
    def doQualityControl(self, sample):
        """The method doQualityControl executes the quality control on the raw data of the forward and reversed reads of the sample
        
        :param sample: The sample where to do a quality control on
        :type sample: :py:class:`Sample.Sample`
        :raises: ValueError when the sample has no forward fastq file
        
        """
        
        if sample.forwardFq == None:
            raise ValueError("The sample has no forward fastq file!")
        
        if sample.forwardFq.hq == False:  
            self._doQualityControlOnFile(sample.forwardFq)
        
        if sample.reversedFq != None and sample.reversedFq.hq == False:
            self._doQualityControlOnFile(sample.reversedFq)
        
    def _doQualityControlOnFile(self, file):
        """This method executes the quality control function on the given file of the given sample
        
        :param file: The file to do the quality control on
        :type file: instance of a child object of the :py:class:`File.File` object
        
        """
        
        inFile = file.getFile()
        outFile = file.getNewFileName()
        self.execute("cp " + inFile + " " + outFile, "qc (not yet implemented, just making a copy...)", file)
        os.chmod(outFile, stat.S_IRUSR | stat.S_IRGRP | stat.S_IROTH | stat.S_IWUSR)
        file.setFile(outFile)
        file.hq = True