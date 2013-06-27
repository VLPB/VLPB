'''
Created on Jun 21, 2013

@author: Jetse
'''
from VlpbConfig import Configuration, Logger
import os

class Pool(object):
    """The Pool object represents a pool of samples where programs can be executed on
    
    """
    def __init__(self, poolName, outputDir, refGenome, configFile="../VlpbConfig/config.ini"):
        """The constructor of the Pool sets the instance variables, creates the output directory and a Logger object.
        :param poolName: The name of this pool
        :type poolName: str
        :param outputDir: The output directory of this pool, a sub directory will be created for each pool.
        :type outputDir: str -- Path to the output direcotory
        :param refGenome: The reference genome
        :type refGenome: str -- Path to the reference genome
        :param configFile: The path to the configuration file, default is for the default 150 genomes project path
        :type configFile: str -- path to the configuration file
        
        **Instance variables**
        * samples: an array of all :py:class:`Sample.Sample`s in this pool
        * vcf: an :py:class:`VcfFile.VcfFile` of this pool, None if not created yet
        * beagleOut: an :py:class:`BeagleFile.BeagleFile` of this pool, None if not created yet
        
        """
        self.samples = []
        self.vcf = None
        self.beagleOut = None
        
        self.refGenome = refGenome
        self.config = Configuration.Config(configFile)
        self.poolName = poolName
        self.outputDir = outputDir + "/" + poolName + "/"
        if not os.path.isdir(self.outputDir):
            os.makedirs(self.outputDir)
        self.logger = Logger.Logger(self.outputDir + poolName + ".log")
        
        
            
    def addSample(self, sample):
        """Method for adding a sample to the arraylist of samples
        
        """
        self.samples.append(sample)