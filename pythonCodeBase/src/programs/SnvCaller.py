from programs import Program, ConversionTools
from model import VcfFile
class SnvCaller(Program.Program):
    """The SnvCaller class regulates all programs which can call the SNV's
    
    """
    
    def callSNVs(self, pool):
        """The method callSNVs checks if all conversion steps are executed on the bam file of all samples.
        Then the program to call SNVs with is read from the configuration file with the method: :py:meth:`Configuration.Configuration.getProgram`.
        After this check the read method is executed
        
        """
       
        for sample in pool.samples:
            ct = ConversionTools.ConversionTools()
            ct.addHeaderLine(sample.bam)
            ct.removeDuplicates(sample.bam)
            ct.addMdTag(sample.bam)
            ct.createBamIndex(sample.bam)
            
        snvCaller = pool.config.getProgram(["samtools mpileup","GATK"])
        if snvCaller == "samtools mpileup":
            self._samtoolsMpileup(pool)
        elif snvCaller == "GATK":
            self._gatk(pool)
    
    def _samtoolsMpileup(self, pool):
        """The method samtoolsMpileup calls the single nucleotide variations of a pool with samtools mpileup.
        
        :param pool: the pool to call all SNVs from
        :type pool: an instance of a :py:class:`Pool.Pool` object
        
        """

        inputFileString = ""
        for sample in pool.samples:
            inputFileString = inputFileString + " " + sample.bam.getFile()
            
        pool.vcf = VcfFile.VcfFile(pool)
        outputFile = pool.vcf.getFile()
        cmd = pool.config.getProgramPath("samtools") + " mpileup " + self.getProgramArguments("samtools mpileup", pool.config) + " -gf " + pool.refGenome + inputFileString + " > " + outputFile
        self.execute(cmd, "samtools mpileup", pool.vcf)
        self._filterVcf(pool.vcf)
    
    def _convertToVcf(self, vcfFile):
        """This method converts a bcf file to a vcf file of a given pool.
        
        :param vcfFile: The bcf file which has to be converted to vcf.
        :type vcfFile: an instance of a :py:class:`VcfFile.VcfFile` object
        
        """
        if vcfFile == None:
            raise TypeError("Pool contains no vcf file!")
        
        if vcfFile.bcf == False:
            return
        
        outputFile = vcfFile.getNewFileName()
        cmd = vcfFile.pool.config.getProgramPath("bcftools") + " view -vcg " + self.getProgramArguments("bcftools view", vcfFile.pool.config) + " " + vcfFile.getFile() + " > " + outputFile 
        self.execute(cmd,"bcftools view", vcfFile)
        vcfFile.bcf = False
        vcfFile.setFile(outputFile)
    
    def _filterVcf(self, vcfFile):
        """The method filterVcf removes the insignificant SNVs from the vcf file.
        
        :param vcfFile: The vcf file which has to be filtered, when it is bcf, it first will be converted to vcf.
        :type vcfFile: an instance of a :py:class:`VcfFile.VcfFile` object
        
        """
        self._convertToVcf(vcfFile)
        
        if vcfFile.filtered == True:
            return
        
        outputFile = vcfFile.getNewFileName()
        cmd = "perl " + vcfFile.pool.config.getProgramPath("vcfutils") + " varFilter " + self.getProgramArguments("vcfutils varFilter", vcfFile.pool.config) + " " + vcfFile.getFile() + " > " + outputFile
        self.execute(cmd,"vcfutils varFilter", vcfFile)
        vcfFile.filtered = True
        vcfFile.setFile(outputFile)
    
    def _gatk(self, inputFiles):
        """The method gatk calls all single nucleotide variations of a bam file with GATK.
        If the bam file does not contain a header value with the information about the master, platform and library, this header first will be added.
        
        :param inputFile: the sorted and indexed bam file with an information header where the SNV calling has to be called on
        :type inputFile: str. -- the path to this file
        :returns: str. -- the vcf file with all SNV's
        
        """
        
        if type(inputFiles) == list or inputFiles.endswith("Wh.bam") == False:
            converter = ConversionTools.ConversionTools(self.outputDir, self.refGenome, self.libName)
            inputFiles = converter.addHeaderLine(inputFiles)
            converter.createBamIndex(inputFiles)
        
        outputFile = self.getOutputFile(".vcf")
        cmd = "java -jar " + self.pool.config.getProgramPath("gatk") + " -T UnifiedGenotyper -R " + self.pool.refGenome + " -I " + inputFiles + " -o " + outputFile
        self.execute(cmd, "GATK", outputFile)
        return self._convertToBcf(outputFile)
