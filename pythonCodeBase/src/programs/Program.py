from subprocess import Popen, PIPE

class Program(object):
    """The Program is a class which represents an executable program.

    """

    def execute(self, command, programName, file):
        """This method executes the command created by its children
        
        :param command: The command to execute
        :type command: str.
        :param programName: The name of the program to execute
        :type programName: str
        :param file: the file this commands is executed on, #TODO create per file object a check if the output is valid
        :type file: an instance of a :py:class:`File.File` object
        
        """
        
        file.pool.logger.nextProgram(programName, command)

        print("executing: " + programName)
        error,output = Popen(command, shell=True, stdout=PIPE, stderr=PIPE).communicate()
        file.pool.logger.logOut(output)
        file.pool.logger.logError(error)
        print("Finished!\n")

    def getProgramArguments(self, programName, config):
        """The method getProgramArguments asks the configuration object for all arguments and parses these to one space separated string.
        When the program needs the arguments in a different way, this method can be overrided.
        
        :param programName: The name of the program where to retrieve the options from
        :type programName: str.
        :param config: The configuration object which holds the arguments of the programs
        :type config: an instance of a :py:class:`Configuration.Configuration` object
        :returns: The program arguments as a <space> separated string.
        
        """
        args = config.getProgramOptions(programName)
        argsCmd = " "
        for arg in args:
            argsCmd = argsCmd + arg + " "
            if args[arg]:
                argsCmd = argsCmd + args[arg] + " "
        return argsCmd


