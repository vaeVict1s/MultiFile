#! /usr/bin/env python3

import argparse
import logging
import numpy as np
import sys


class MultiFile(object):
    """
    This class is meant to be used to read lines 
    from an arbitrary number of files in parallel.
    
    Attributes:
    -----------
    _logging: bool
        A bool which switches on/off logging to stderr.
    _permissive: bool
        A bool which indicates whether 
        the iteration should go on when a file in the list ends.
    _files: list of file objects
        The list of file objects open in read mode.
    _filesToIterate: list of file objects
        The list of files objects open in read mode,
        over which the MultiFile iterates.
        This list is different from the other 
        because it does not include the consumed files
    _IOErrStrings: str
        This string is used to record IOError
        while opening files in read mode.
    """
    
    _Log_Format = "%(levelname)s %(asctime)s - %(message)s"
    logging.basicConfig(stream = sys.stderr, format = _Log_Format, level = logging.INFO)
    _class_logger = logging.getLogger(__name__).getChild(__qualname__)
    
    def __init__(self, *files, logging = False, permissive = False):
        """
        Parameters:
        -----------
        files: str
            An arbitrary number of single file paths.
            At any iteration, 
            MultiFile object reads a line from any single file,
            in the same order as they are passed to the object construction.
            For the exact procedure, see __iter__.
        logging: bool, optional
            This parameter handles the logging to the stderr.
            If set to True, information about consumed files
            is produced on the stderr after normal stdout is printed.
            The logging level is INFO.
            Default value is False.
        permissive: bool, optional
            This parameter handles the behaviour of the iteration,
            when a file is consumed.
            If set to False, the iteration breaks when the firt file ends.
            If seto to True, the itereation goes on.
            Default value is False.
        """
        
        self._logging = logging
        self._permissive = permissive
        self._files = []
        self._filesToIterate = []
        self._IOErrStrings = []
        for filePath in list(files):
            try:
                tempFile = open(filePath)
                self._files.append(tempFile)
                self._filesToIterate.append(tempFile)
            except IOError as e:
                IOerror = "I/O error({0}): {1} : '{2}'"
                self._IOErrStrings.append(IOerror.format(e.errno, e.strerror, filePath))
        if self._IOErrStrings:
            self._class_logger.error('\n'.join(self._IOErrStrings))
            raise IOError

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
       for stillOpenFile in self._files:
           stillOpenFile.close()

    def __iter__(self):
        """
        At any iteration,
        the MultiFile object reads a line from any single file,
        in the same order as they are passed to the object construction.
        If all readings produce a line,
        the iteration yelds a list whose elements are the read lines.
        Otherwise, if any file is finished, the behaviour is as follow.
        If logging is set to True,
        a log to stderr signals the finished files.
        If permissive is set to True,
        the MultiFile object yelds a list 
        containing only the lines read from non consumed files,
        and the iteration continues on these files only.
        If permissive is set to False, the iteration stops.
        """
        
        while True:
            if not self._filesToIterate:
                raise StopIteration
            lines = [ next(f,'') for f in self._filesToIterate ]
            if all(lines):
                yield lines
            else:
                overFilesNames = [ overFile.name for overFile, line in zip(self._filesToIterate, lines) if line == '' ]
                if self._logging:
                    self._class_logger.info("over: " + ', '.join(overFilesNames))
                if self._permissive:
                    lines = [ line for line in lines if line ]
                    if lines:
                        yield lines
                    self._filesToIterate = [ myFile for myFile in self._filesToIterate if myFile.name not in overFilesNames ]
                else:
                    self._filesToIterate = []

    def close(self):
        for stillOpenFile in self._files:
            stillOpenFile.close()
