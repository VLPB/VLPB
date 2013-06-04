import ConfigParser
import os

class Config:
    """The Config class regulates everything of the configuration of the programs.
    This information is read from the iniFile config.ini which is located in this directory.

    """
    def __init__(self):
        """The constructor opens the ini file for easy access in this object to the ini file.
        
        """
        self.parser = ConfigParser.ConfigParser()
        self.parser.readfp(open("VlpbConfig/config.ini"))
        
    def getProgramPath(self, program):
        """The method getProgramPath retrieves the path of a program from the ini file.
        
        """
        return self.parser.get("programs", program)
