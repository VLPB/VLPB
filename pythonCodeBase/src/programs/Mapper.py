from programs import Program, QualityControl
from model import BamFile
import os

class Mapper(Program.Program):
    """The class Mapper regulates all mapping processes, available mapper: BWA
    
    """
    
    def map(self, sample):
        """The method map checks which mapper has to be executed from the :class:`Configuration` object.
        First the quality control has to be done to the samples, after the quality control, the mapping will be executed.
        
        :param sample: The sample to map against his reference genome
        :type sample: an instance of :py:class:`Sample.Sample`
        
        """
        
        QualityControl.QualityControl().doQualityControl(sample)
        
        mapper = sample.pool.config.getProgram(["BWA"])
        if mapper == "BWA":
            self._executeBwa(sample.forwardFq, sample.reversedFq)
    
    def _executeBwa(self,forwardFq, reversedFq=None):
        """The method executeBwa executes the mapping with BWA.
        
        :param forwardFq: The forward fastq file to map against the reference genome
        :type forwardFq: an instance of :py:class:`FastqFile.FastqFile`
        :param reversedFq: The reversed fastq file to map against the reference genome
        :type reversedFq: an instance of :py:class:`FastqFile.FastqFile`, None if the data has no paired end reads.
        
        """
        
        ##Build the command
        cmd = forwardFq.pool.config.getProgramPath("bwa")  # @UndefinedVariable
        if reversedFq == None:
            cmd = cmd + " samse "
        else:
            cmd = cmd + " sampe " + self.getProgramArguments("BWA", forwardFq.pool.config)
            
        cmd = cmd + forwardFq.pool.refGenome

        #add the .sai files to the command
        forwardMapped = self._bwaAlign(forwardFq)
        cmd = cmd + " " + forwardMapped
        if reversedFq != None:
            reversedMapped = self._bwaAlign(reversedFq)
            cmd = cmd + " " + reversedMapped
        
        #add the high quality reads to the command
        cmd = cmd + " " + forwardFq.fileName
        if reversedFq != None:
            cmd = cmd + " " + reversedFq.fileName
        
        #add the output file to the command
        forwardFq.sample.bam = BamFile.BamFile(forwardFq.pool, forwardFq.sample, sam=True)
        cmd = cmd +  " > " + forwardFq.sample.bam.getFile()
        
        ##Execute the command
        self.execute(cmd, "BWA", forwardFq.sample.bam)
        
        ##Cleanup the mess
        os.unlink(forwardMapped)
        if reversedFq != None:
            os.unlink(reversedMapped)

    def _bwaAlign(self, inputFile):
        """The method bwaAlign aligns the reads with bwa aln to the reference genome
        
        :param inputFile: The file to map against the reference genome
        :type inputFile: an instance of :py:class:`FastqFile.FastqFile`

        """
        
        outputFile = inputFile.sample.outputDir + inputFile.sample.libName  + "_0.sai"
        if inputFile.forward == False:
            outputFile = inputFile.sample.outputDir + inputFile.sample.libName  + "_1.sai"
            
        cmd = inputFile.pool.config.getProgramPath("bwa") + " aln " + self.getProgramArguments("BWA aln", inputFile.pool.config) + inputFile.pool.refGenome + " " + inputFile.getFile() + " > " + outputFile  # @UndefinedVariable
        self.execute(cmd, "BWA aln", inputFile)
        return outputFile
    
    
    
    
