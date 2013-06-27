'''
Created on Jun 21, 2013

@author: Jetse
'''
from programs import Decompressor
import abc, os

class File(object):
    """The File object represents a file. This is an abstract object, so can not be instantiated.
    
    """
    
    __metaclass__ = abc.ABCMeta
    
    def __init__(self, pool, sample=None, fileName=None):
        """A file always has a filename, this filename is set in the constructor as instance variable.
        :param pool: The pool this file is from
        :type poo: an instance of a :py:class:`Pool.Pool` object
        :param sample: The sample this file is from, default is None because some files do not have a sample
        :type sample: an instance of a :py:class:`Sample.Sample` object.
        :param fileName: the name of this file, if None, the name will be set to a default name
        :type fileName: str -- path to this file
        
        """
        
        self.sample = sample
        self.pool = pool
        
        
        if fileName == None:
            fileName = self.getPreferredFileName()
        self.fileName = fileName  
        
    def __str__(self):
        return self.fileName
        
    def setFile(self, fileName):
        """The method setFile removes the old file and puts the new file in place.
        :param fileName: The name of the new file
        :type fileName: Str. -- path to the new file
        
        """
        
        if os.path.dirname(fileName) == os.path.dirname(self.fileName):
            os.remove(self.fileName)
            
        os.renames(fileName, self.getPreferredFileName())
        self.fileName = self.getPreferredFileName()
        
    def getPreferredFileName(self):
        """Getter for retrieving the preferred file name of a file
        
        """
        
        if self.sample != None: 
            prefix = self.sample.outputDir + self.sample.libName
        else: 
            prefix = self.pool.outputDir + self.pool.poolName
            
        return prefix + self.getSuffix()
        
    def getNewFileName(self):
        """A simple getter for retrieving a new filename without overwriting the old one.
        
        """
        
        return self.getPreferredFileName() + "New"
            
    
    def getFile(self):
        """This method returns the filename, if the file is compressed, the extracted file will be returned.
        
        """
        if self.fileName.endswith(".gz"):
            dc = Decompressor.Decompressor()
            return dc.extract(self)
        return self.fileName
    
    @abc.abstractmethod
    def getSuffix(self): 
        """The method getSuffix returns the suffix of a file.
        this method is implemented in all subclasses.
        
        :raises: a NotImplementedError when this method is not implemented in a subclass
        """
        raise NotImplementedError("getSuffix method not implemented!")