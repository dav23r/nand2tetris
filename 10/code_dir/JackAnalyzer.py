#!/usr/bin/env python3

import os
import sys
from JackTokenizer import JackTokenizer
from CompilationEngine import CompilationEngine
from XmlKeywords import xmlKeywordsConvert

if __name__ == '__main__':
    folderName = sys.argv[1]
    print ("Got folder: {0}".format(folderName))
    for fileName in os.listdir(folderName):
        if fileName.endswith('.jack'):
            baseName = fileName[:-5]
            path = folderName + '/'
            print ('Compiled to xml: ' + fileName)

            # Print raw tokens
            tokenizer = JackTokenizer(open( folderName + '/' + fileName, 'r'))
            rawTokensFile = open(path + baseName + 'T' + '.xml', 'w')
            print ('<tokens>', file=rawTokensFile)
            while tokenizer.hasMoreTokens():
                tokenizer.advance()
                tokType = tokenizer.tokenType()

                if not tokType in \
                    ['keyword', 'symbol', 'identifier', 'integerConstant', 'stringConstant']:
                    raise Exception('Unrecognized token type {0}'.format(tokType))
                value = tokenizer.getToken()
                if tokType == 'symbol':
                    value = xmlKeywordsConvert(tokenizer.getToken())
                print ('<{0}> {1} </{0}>'.format(tokType, value), file=rawTokensFile)
            print ('</tokens>', file=rawTokensFile)
            rawTokensFile.close()

            # Printf parsed (formatted) tokens
            tokenizer = JackTokenizer(open( folderName + '/' + fileName, 'r'))
            parsedFile = open(path + baseName + '.xml', 'w')
            engine = CompilationEngine(tokenizer, parsedFile)
            engine.CompileClass()
            parsedFile.close()
            
