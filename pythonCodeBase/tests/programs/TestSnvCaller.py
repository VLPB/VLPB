import unittest, sys,os,shutil
sys.path.append("../../src")
from programs import SnvCaller
from model import Pool, Sample, BamFile

class TestSnvCaller(unittest.TestCase):
    inputWithMd = "../testFiles/input/testMD.bam"
    inputWithSam = "../testFiles/input/test.sam"
    inputBam = "../testFiles/input/test.bam"
    
    expVcfFile = "../testFiles/output/testPool/testPool.vcf"
    expBcfFile = "../testFiles/output/testPool/testPool.bcf"
        
    def setUp(self):
        for file in os.listdir("../testFiles/output/"):
            file_path = os.path.join("../testFiles/output/", file)
            if os.path.isdir(file_path):
                shutil.rmtree(file_path)
            else: os.unlink(file_path)
        TestSnvCaller.testPool = Pool.Pool("testPool", "../testFiles/output/", "../testFiles/input/smallRefGenome.fa", configFile="../../src/VlpbConfig/config.ini")
        TestSnvCaller.sample = Sample.Sample(TestSnvCaller.testPool, "testLib")
        TestSnvCaller.testPool.addSample(TestSnvCaller.sample)
        TestSnvCaller.sample.bam = BamFile.BamFile(TestSnvCaller.testPool, TestSnvCaller.sample, TestSnvCaller.inputWithMd)
        TestSnvCaller.snvCaller = SnvCaller.SnvCaller()
            
    def testSamtoolsMpileup(self):
        expFileSize = 3557
        TestSnvCaller.snvCaller._samtoolsMpileup(TestSnvCaller.testPool)
        outputFile = TestSnvCaller.testPool.vcf.fileName
        self.assertEqual(os.path.abspath(outputFile),os.path.abspath(TestSnvCaller.expVcfFile) , os.path.abspath(outputFile) + " not is " +  os.path.abspath(TestSnvCaller.expVcfFile))
        self.assertEqual(expFileSize, os.path.getsize(outputFile), "filesize: " +  str(os.path.getsize(outputFile)) + " is not " + str(expFileSize))
       
    def testSamtoolsPath(self):
        expFileSize = 3538
        TestSnvCaller.testPool.vcf = None
        TestSnvCaller.sample.bam = BamFile.BamFile(TestSnvCaller.testPool, TestSnvCaller.sample, TestSnvCaller.inputWithSam, sam=True)
        TestSnvCaller.snvCaller.callSNVs(TestSnvCaller.testPool)
        outputFile = TestSnvCaller.testPool.vcf.fileName
        self.assertEqual(os.path.abspath(outputFile),os.path.abspath(TestSnvCaller.expVcfFile) , os.path.abspath(outputFile) + " not is " +  os.path.abspath(TestSnvCaller.expVcfFile))
        self.assertEqual(expFileSize, os.path.getsize(outputFile), "filesize: " +  str(os.path.getsize(outputFile)) + " is not " + str(expFileSize))
        
    def testSamtoolsMultiple(self):
        #add an extra sample to the pool
        TestSnvCaller.sample2 = Sample.Sample(TestSnvCaller.testPool, "testLib2")
        TestSnvCaller.sample2.bam = BamFile.BamFile(TestSnvCaller.testPool, TestSnvCaller.sample2, TestSnvCaller.inputBam)
        TestSnvCaller.testPool.addSample(TestSnvCaller.sample2)
        
        #Execute and check execution output
        expFileSize = 3602
        TestSnvCaller.snvCaller._samtoolsMpileup(TestSnvCaller.testPool)
        outputFile = TestSnvCaller.testPool.vcf.fileName
        self.assertEqual(os.path.abspath(outputFile),os.path.abspath(TestSnvCaller.expVcfFile) , os.path.abspath(outputFile) + " not is " +  os.path.abspath(TestSnvCaller.expVcfFile))
        self.assertEqual(expFileSize, os.path.getsize(outputFile), "filesize: " +  str(os.path.getsize(outputFile)) + " is not " + str(expFileSize))
    
#     def testGatk(self):
#         expVcfFile = "../testFiles/output/test/test.bcf"
#         expFileSize = 3050
#         outputFile = TestMapper.snvCaller._gatk(self.inputWithWh)
#         self.assertEqual(os.path.abspath(outputFile),os.path.abspath(expVcfFile) , os.path.abspath(outputFile) + " not is " +  os.path.abspath(expVcfFile))
#         self.assertEqual(expFileSize, os.path.getsize(outputFile), "filesize: " +  str(os.path.getsize(outputFile)) + " is not " + str(expFileSize))
#      
#     def testGatkPath(self):
#         expVcfFile = "../testFiles/output/test/test.bcf"
#         expFileSize = 3055
#         outputFile = TestMapper.snvCaller._gatk(self.inputWithSam)
#         self.assertEqual(os.path.abspath(outputFile),os.path.abspath(expVcfFile) , os.path.abspath(outputFile) + " not is " +  os.path.abspath(expVcfFile))
#         self.assertEqual(expFileSize, os.path.getsize(outputFile), "filesize: " +  str(os.path.getsize(outputFile)) + " is not " + str(expFileSize))
    
    
    
if __name__ == '__main__':        
    unittest.main()
