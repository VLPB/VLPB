'''
Created on Jun 21, 2013

@author: Jetse
'''
import File
class BeagleFile(File.File):
    """The BeagleFile represents a BeagleFile file and contains instance variables to indicate the processes used on this BeagleFile file.
    The beaglefile contains multiple output files.
    
    """
    
    def __init__(self, pool, chrom, fileName = None):
        """The constructor of the BeagleFile sets the instance variables.
        :param chrom: The name of the chromosome
        :type chrom: str
        
        """
        self.chrom = chrom
        super(BeagleFile,self).__init__(pool, fileName=fileName)
        
    def getSuffix(self):
        """implements the getSuffix of the file object.
        returns the chromosome for not overwriting files with differend chromosomes
        """
        
        return self.chrom