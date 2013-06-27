'''
Created on Jun 21, 2013

@author: Jetse
'''
import File
class VcfFile(File.File):
    """The VcfFile represents a vcf or bcf file and contains instance variables to indicate the processes used on this vcf file
    
    """
    
    def __init__(self, pool, fileName=None, bcf = True, filtered = False):
        """The constructor of the vcf file sets the given variables as instance variables.
        :param bcf: boolean whether the file is bcf or vcf, default: True
        :param filtered: boolean whether the file is already filtered or not, default: True
        """
        self.bcf = bcf
        self.filtered = filtered
        super(VcfFile,self).__init__(pool, fileName=fileName)
        
    def getSuffix(self):
        """implements the getSuffix of the file object.
        
        """
        
        if self.bcf == True:
            return ".bcv"
        return ".vcf"