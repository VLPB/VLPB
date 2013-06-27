import unittest, os, sys, shutil
sys.path.append("../../src")
from programs import ConversionTools
from model import Pool,Sample, BamFile

class TestConversionTools(unittest.TestCase):
    
    samFile = "../testFiles/input/test.sam"
    bamFile = "../testFiles/input/test.bam"
    sortedBamFile = "../testFiles/input/testSorted.bam"
    gzFile = "../testFiles/input/pairedTest.tar.gz"
    expBamOutFile= "../testFiles/output/testPool/testLib/testLib.bam"
    
    def setUp(self):
        for file in os.listdir("../testFiles/output/"):
            file_path = os.path.join("../testFiles/output/", file)
            if os.path.isdir(file_path):
                shutil.rmtree(file_path)
            else: os.unlink(file_path)
        TestConversionTools.testPool = Pool.Pool("testPool", "../testFiles/output/", "../testFiles/input/smallRefGenome.fa", configFile="../../src/VlpbConfig/config.ini")
        TestConversionTools.sample = Sample.Sample(TestConversionTools.testPool, "testLib")
        TestConversionTools.testPool.addSample(TestConversionTools.sample)
        TestConversionTools.convTools = ConversionTools.ConversionTools()
         
    def testConvertToBam(self):
        expBamSize = 309572
        TestConversionTools.sample.bam = BamFile.BamFile(TestConversionTools.testPool, TestConversionTools.sample, TestConversionTools.samFile, sam=True)
        self.convTools.convertToBam(TestConversionTools.sample.bam)
        outputFile = TestConversionTools.sample.bam.fileName
        self.assertEqual(os.path.abspath(outputFile),os.path.abspath(TestConversionTools.expBamOutFile) , os.path.abspath(outputFile) + " not is " +  os.path.abspath(TestConversionTools.expBamOutFile))
        self.assertEqual(expBamSize, os.path.getsize(outputFile), "filesize: " +  str(os.path.getsize(outputFile)) + " is not " + str(expBamSize))
        
    def testSortBam(self):
        expSortedBamSize = 56790
        TestConversionTools.sample.bam = BamFile.BamFile(TestConversionTools.testPool, TestConversionTools.sample, TestConversionTools.bamFile)
        self.convTools.sortBam(TestConversionTools.sample.bam)
        outputFile = TestConversionTools.sample.bam.fileName
        self.assertEqual(os.path.abspath(outputFile),os.path.abspath(TestConversionTools.expBamOutFile) , os.path.abspath(outputFile) + " not is " +  os.path.abspath(TestConversionTools.expBamOutFile))
        self.assertEqual(expSortedBamSize, os.path.getsize(outputFile), "filesize: " +  str(os.path.getsize(outputFile)) + " is not " + str(expSortedBamSize))
         
    def testCreateBamIndex(self):
        indexFilesize = 96
        TestConversionTools.sample.bam = BamFile.BamFile(TestConversionTools.testPool, TestConversionTools.sample, TestConversionTools.bamFile)
        self.convTools.sortBam(TestConversionTools.sample.bam)
        self.convTools.createBamIndex(TestConversionTools.sample.bam)
        outputFile = TestConversionTools.sample.bam.fileName
        self.assertEqual(os.path.abspath(outputFile), os.path.abspath(TestConversionTools.expBamOutFile) , os.path.abspath(outputFile) + " not is " +  os.path.abspath(TestConversionTools.expBamOutFile))
        self.assertTrue(os.path.isfile(TestConversionTools.expBamOutFile + ".bai") , os.path.abspath(TestConversionTools.expBamOutFile + ".bai") + " is not created")
        self.assertEqual(indexFilesize, os.path.getsize(TestConversionTools.expBamOutFile + ".bai"), "filesize: " +  str(os.path.getsize(TestConversionTools.expBamOutFile + ".bai")) + " is not " + str(indexFilesize))
          
    def testAddHeaderLine(self):
        expBamSize = 58222
        TestConversionTools.sample.bam = BamFile.BamFile(TestConversionTools.testPool, TestConversionTools.sample, TestConversionTools.bamFile)
        self.convTools.addHeaderLine(TestConversionTools.sample.bam)
        outputFile = TestConversionTools.sample.bam.fileName
        self.assertEqual(os.path.abspath(outputFile),os.path.abspath(TestConversionTools.expBamOutFile) , os.path.abspath(outputFile) + " not is " +  os.path.abspath(TestConversionTools.expBamOutFile))
        self.assertEqual(expBamSize, os.path.getsize(outputFile), "filesize: " +  str(os.path.getsize(outputFile)) + " is not " + str(expBamSize))
           
    def testRemoveDuplicates(self):
        expBamSize = 56790
        TestConversionTools.sample.bam = BamFile.BamFile(TestConversionTools.testPool, TestConversionTools.sample, TestConversionTools.bamFile)
        self.convTools.removeDuplicates(TestConversionTools.sample.bam)
        outputFile = TestConversionTools.sample.bam.fileName
        self.assertEqual(os.path.abspath(outputFile),os.path.abspath(TestConversionTools.expBamOutFile) , os.path.abspath(outputFile) + " not is " +  os.path.abspath(TestConversionTools.expBamOutFile))
        self.assertEqual(expBamSize, os.path.getsize(outputFile), "filesize: " +  str(os.path.getsize(outputFile)) + " is not " + str(expBamSize))
         
    def testAddMdTag(self):
        expBamSize = 353441
        TestConversionTools.sample.bam = BamFile.BamFile(TestConversionTools.testPool, TestConversionTools.sample, TestConversionTools.bamFile)
        self.convTools.addMdTag(TestConversionTools.sample.bam)
        outputFile = TestConversionTools.sample.bam.fileName
        self.assertEqual(os.path.abspath(outputFile),os.path.abspath(TestConversionTools.expBamOutFile) , os.path.abspath(outputFile) + " not is " +  os.path.abspath(TestConversionTools.expBamOutFile))
        self.assertEqual(expBamSize, os.path.getsize(outputFile), "filesize: " +  str(os.path.getsize(outputFile)) + " is not " + str(expBamSize))
        
#     def testPath(self):
#         """The method testPath tests whether all previous programs are executed.
#              
#         """
#         expBamFile = "../testFiles/output/test/testWh.bam"
#         expBamSize = 57963
#         outputFile = self.convTools.addHeaderLine([TestConversionTools.gzFile])
#         self.assertEqual(os.path.abspath(outputFile),os.path.abspath(expBamFile) , os.path.abspath(outputFile) + " not is " +  os.path.abspath(expBamFile))
#         self.assertEqual(expBamSize, os.path.getsize(outputFile), "filesize: " +  str(os.path.getsize(outputFile)) + " is not " + str(expBamSize))
if __name__ == '__main__':        
    unittest.main()
    
    