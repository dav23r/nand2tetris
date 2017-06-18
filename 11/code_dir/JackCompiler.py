#!/usr/bin/env python3

import os
import sys

from JackTokenizer import JackTokenizer
from CompilationEngine import CompilationEngine
from VMWriter import VMWriter

if __name__ == '__main__':
    folderName = sys.argv[1]
    print ("Got folder: {0}".format(folderName))

    for fileName in os.listdir(folderName):
        if fileName.endswith('.jack'):
            baseName = fileName[:-5]
            path = folderName + '/'
            print ('Translating to vm code: ' + fileName)

            tokenizer = JackTokenizer(open(folderName + '/' + fileName, 'r'))
            vmWriter = VMWriter(open(folderName + '/' + baseName + '.vm', 'w'))

            engine = CompilationEngine(tokenizer, vmWriter)
            engine.CompileClass()
            vmWriter.close()
            
