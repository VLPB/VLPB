from programs import Program, SnvCaller
import csv, os
from model import BeagleFile

class Haplotyper(Program.Program):
    """The Haplotyper class regulates the haplotyping of a vcf file
    
    """
    
    def callHaplotypes(self, pool):
        """The method callHaplotypes calls the haplotypes of a vcf file. When the vcf file is not set, first the SNVs are called with the :py:class:`SnvCaller.SnvCaller` object
        In future when multiple programs for haplotyping are implemented, here the check will be performed which haplotyper to execute. First only beagle is implemented so this method will be called
        :param pool: The pool a haplotyping tools has to be executed on
        :type pool: an instance of a :py:class:`Pool.Pool` object
        
        """
        if pool.vcf == None:
            self.sc = SnvCaller.SnvCaller(pool)
            self.sc.callSNVs(pool)
            
        self._executeBeagle(pool)
    
    def _executeBeagle(self, pool):
        """The method executeBeagle executes beagle. First the vcf file is converted to a format beagle needs, then beagle is executed.
        :param pool: The pool beagle has to executed on
        :type pool: an instance of a :py:class:`Pool.Pool` object
        
        """
        if pool.vcf.bcf==True:
            self.sc.callSNVs(pool)
        
        prefixes = self._createBeagleInput(pool)
        newPrefixes = []
        for prefix in prefixes:
            inputFile = prefix + ".BEAGLE.PL"
            cmd = "java -jar " + pool.config.getProgramPath("beagle")  + " like=" + inputFile + " out=" + pool.outputDir + "out"
            self.execute(cmd, "beagle", pool.beagleOut)
            newPrefixes.append(pool.outputDir + "out." + os.path.basename(prefix))
            
        return newPrefixes
        
    def _createBeagleInput(self, pool):
        """The method createBeagleInput prepares the vcf file of a pool for using this vcf file with beagle.
        :param pool: The pool beagle has to executed on
        :type pool: an instance of a :py:class:`Pool.Pool` object
        
        """        
        outputFilePrefixes = []
        for chrIndex in self._getChromosomes(pool.refGenome):
            pool.beagleOut = BeagleFile.BeagleFile(pool, chrom=chrIndex)
            outputPrefix = pool.beagleOut.getPreferredFileName()
            
            #build the command
            cmd = pool.config.getProgramPath("vcftools") 
            if pool.vcf.bcf == True:
                cmd = cmd + " --bcf " + pool.vcf.getFile() 
            else:
                cmd = cmd + " --vcf " + pool.vcf.getFile() 
            cmd = cmd + " --out " + outputPrefix + " --chr " + chrIndex + " --BEAGLE-PL"
            
            self.execute(cmd, "vcftools", pool.vcf)
            outputFilePrefixes.append(outputPrefix)
            
        return outputFilePrefixes
        
    def _getChromosomes(self, refGenome):
        """The method getChromosomes retrieves the chromosomes of a reference file
        :param refGenome: path to the reference genome where to retrieve the reference sequences from
        :type refGenome: str
        
        """
        refIndex = refGenome + ".fai"
        chromosomes = []
        with open(refIndex) as indexFile:
            indexReader = csv.reader(indexFile, delimiter="\t")
            for line in indexReader:
                chromosomes.append(line[0])
        return chromosomes
                