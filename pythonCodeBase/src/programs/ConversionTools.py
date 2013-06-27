from programs import Program, Mapper

class ConversionTools(Program.Program):
    """The class ConvertionTools regulates the support between the mappers and the programs for SV calling.
    
    """
    
    def sortBam(self, bamFile):
        """The method sortBam sorts a bam file of a given sample.
        The bam file can only be sorted when this is a bam file. If it is not a bam file, the file first will be converted to a bam file.
        
        :param sample: The sample which contains the bam file to be sorted
        :type sample: an instance of a Sample object
        
        """
        
        if bamFile == None or bamFile.sam == True:
            self.convertToBam(bamFile) 
            
        if bamFile.sorted == True:
            return

        outputFile = bamFile.getNewFileName()
        cmd = bamFile.pool.config.getProgramPath("samtools") + " sort -o " + bamFile.getFile() + " " + outputFile + " > " + outputFile
        self.execute(cmd, "samtools sort", bamFile)
        bamFile.sorted = True
        bamFile.setFile(outputFile)
        
    def convertToBam(self, bamFile):
        """The method convertToBam converts a sam file to a bam file of a given sample, if the file is not a sam file, the file first will be mapped
        by calling the :meth:`Mapper.Mapper.map` function.
        
        :param sample: The sample which contains the sam file to be converted to a bam file
        :type sample: an instance of a Sample object
        
        """
        
        if bamFile == None:
            Mapper.Mapper().map(bamFile.sample)
            
        if bamFile.sam == False:
            return

        outputFile = bamFile.getNewFileName()
        cmd = bamFile.pool.config.getProgramPath("samtools") + " view "+ self.getProgramArguments("samtools view", bamFile.pool.config) + " " + bamFile.getFile() + " > " + outputFile
        self.execute(cmd, "samtools view", bamFile)
        bamFile.sam = False
        bamFile.setFile(outputFile)
        
    def createBamIndex(self, bamFile):
        """creates a bam index file for the bam file of a given sample.
        
        :param sample: The sample which contains the bam file to create an index for
        :type sample: an instance of a Sample object
        :raises: A typeError when the sample contains no bam file
        
        """
        
        if bamFile == None:
            self.convertToBam(bamFile)

        cmd = bamFile.pool.config.getProgramPath("samtools") + " index " + bamFile.getFile()
        self.execute(cmd, "samtools index", bamFile)
        bamFile.index = True
    
    def addHeaderLine(self, bamFile):
        """Adds a header line to the bam file of a given sample, if the input is not a sorted bam file, first the method :meth:`sortBam` will be executed.
        
        :param sample: The sample which contains the bam file to add the headerline to
        :type sample: an instance of a Sample object
        
        """
        
        if bamFile == None or bamFile.sam == True:
            self.convertToBam(bamFile)
            
        if bamFile.headerLine == True:
            return
        
        outputFile = bamFile.getNewFileName()
        cmd = "java -jar " + bamFile.pool.config.getProgramPath("picardTools") + "AddOrReplaceReadGroups.jar I=" + bamFile.getFile() + " O=" + outputFile + " LB=" + bamFile.sample.libName + " PL=illumina PU=lane SM=samplename"
        self.execute(cmd, "picardtools AddOrReplaceReadGroups", bamFile)
        bamFile.headerLine = True
        bamFile.setFile(outputFile)
        
    def removeDuplicates(self, bamFile):
        """The method removeDuplicates removes all possible PCR duplicates of the bam file of a given sample. If the input file is not a sorted bam file, 
        first the method :meth:`sortBam` will be executed.
        
        :param sample: The sample which contains the bam file to remove the duplicates from
        :type sample: an instance of a Sample object
        
        """
        
        if bamFile == None or bamFile.sam == True or bamFile.sorted == False:
            self.sortBam(bamFile)
            
        if bamFile.duplicates == False:
            return
        
        outputFile = bamFile.getNewFileName()
        cmd = bamFile.pool.config.getProgramPath("samtools") + " rmdup " + bamFile.getFile() + " " + outputFile
        self.execute(cmd, "samtools rmdup", bamFile)
        bamFile.duplicates = False
        bamFile.setFile(outputFile)
    
    def addMdTag(self, bamFile):
        """The method addMdTag adds a md tag to the bam file of a given sample. If the file is not a bam file without duplicates, first the bam file will be converted to bam
        
        :param sample: The sample which contains the bam file to add the md tags to
        :type sample: an instance of a Sample object
        
        """
        
        if bamFile == None or bamFile.sam == True:
            self.convertToBam(bamFile)
            
        if bamFile.mdTag == True:
            return
        
        outputFile = bamFile.getNewFileName()
        cmd = bamFile.pool.config.getProgramPath("samtools") + " calmd " + self.getProgramArguments("samtools calmd",bamFile.pool.config) + " " + bamFile.getFile() + " " + bamFile.pool.refGenome + " > " + outputFile
        self.execute(cmd, "samtools calmd", bamFile)
        bamFile.mdTag = True
        bamFile.setFile(outputFile)
        
