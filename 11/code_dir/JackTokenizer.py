import operator as op
from functools import reduce
import re

class JackTokenizer(object):

    lexical_element_patterns = {
        'symbol' : ['\{', '\}', '\(', '\)', '\[', '\]', '\.', ',', ';', '\+', '-', '\*', 
                    '/', '&', '\|', '<', '>', '=', '-', '~'],
        'integerConstant' : ['[0-9]{1,5}'],
        'stringConstant' : [r'".*"'],
        'identifier' : [r'[^\W\d_][\w_]*']
    }

    keywords = ['class', 'constructor', 'function', 'method', 'field', 'static',
                 'var', 'int', 'char', 'boolean', 'void', 'true', 'false', 'null',
                 'this', 'let', 'do', 'if', 'else', 'while', 'return']

    def __init__(self, stream):

        content = stream.read()
        stream.close()

        # Remove comments
        content = re.sub(re.compile(r'/\*.*?\*/', re.DOTALL), '', content)
        content = re.sub(re.compile(r'/\*\*.*?\*/', re.DOTALL), '', content)
        content = re.sub(re.compile(r'//.*?\n'), '', content)

        pattern_categories = JackTokenizer.lexical_element_patterns
        global_regex = \
                    '|'.join( 
                            map(
                                lambda patterns_name: '(?P<{}>'.format(patterns_name) + \
                                    '|'.join(pattern_categories[patterns_name]) + ')',
                                pattern_categories.keys()))
                                
        self.tokens_iterator = re.finditer(global_regex, content)

    def hasMoreTokens(self):
        try:
            token = next(self.tokens_iterator)
            groups = token.groupdict()
            for group in groups:
                if groups[group]:
                    self.type = group
                    self.value = groups[group]
            return True
        except StopIteration:
            return False

    def advance(self):
        pass
 
    def tokenType(self):
        if self.type != 'identifier':
            return self.type
        if self.value in JackTokenizer.keywords:
            return 'keyword'
        return 'identifier'

    def getToken(self):
        if self.type == 'integerConstant':
            return int (self.value)
        if self.type == 'stringConstant':
            return self.value[1:-1]
        return self.value
