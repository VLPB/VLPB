import unittest, shutil, os, sys 
sys.path.append("../../src")
from programs import Haplotyper
from model import Pool, VcfFile

class TestHaplotyper(unittest.TestCase):

    inputVcf = "../testFiles/input/testFiltered.vcf"

    def setUp(self):
        for file in os.listdir("../testFiles/output/"):
            file_path = os.path.join("../testFiles/output/", file)
            if os.path.isdir(file_path):
                shutil.rmtree(file_path)
            else: os.unlink(file_path)
            
        TestHaplotyper.testPool = Pool.Pool("testPool", "../testFiles/output/", "../testFiles/input/smallRefGenome.fa", configFile="../../src/VlpbConfig/config.ini")
        TestHaplotyper.testPool.vcf = VcfFile.VcfFile(TestHaplotyper.testPool, TestHaplotyper.inputVcf, bcf=False)
        TestHaplotyper.haplotyper = Haplotyper.Haplotyper()

    def testCreateBeagleInput(self):
        expOutFile = "../testFiles/output/testPool/testPoolSL2.40ch11:22900-24100.BEAGLE.PL"
        expSize = 185
        outPrefix = TestHaplotyper.haplotyper._createBeagleInput(TestHaplotyper.testPool)[0]
        self.assertEqual(os.path.abspath(outPrefix + ".BEAGLE.PL"),os.path.abspath(expOutFile) , os.path.abspath(outPrefix + ".BEAGLE.PL") + " not is " +  os.path.abspath(expOutFile))
        self.assertEqual(expSize, os.path.getsize(expOutFile), "filesize: " +  str(os.path.getsize(expOutFile)) + " is not " + str(expSize))
          
    def testChromosomeExtraction(self):
        self.assertEqual("SL2.40ch11:22900-24100", TestHaplotyper.haplotyper._getChromosomes(TestHaplotyper.testPool)[0], "chromosome not extracted from reference genome index")

    def testExecuteBeagle(self):
        expOutFile = "../testFiles/output/testPool/out.testPoolSL2.40ch11:22900-24100.BEAGLE.PL.phased.gz"
        expSize = 91
        outPrefix = TestHaplotyper.haplotyper._executeBeagle(TestHaplotyper.testPool)[0]
        self.assertEqual(os.path.abspath(outPrefix + ".BEAGLE.PL.phased.gz"),os.path.abspath(expOutFile) , os.path.abspath(outPrefix + ".BEAGLE.PL.phased.gz") + " not is " +  os.path.abspath(expOutFile))
        self.assertEqual(expSize, os.path.getsize(expOutFile), "filesize: " +  str(os.path.getsize(expOutFile)) + " is not " + str(expSize))

if __name__ == '__main__':        
    unittest.main()