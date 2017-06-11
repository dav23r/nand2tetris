from XmlKeywords import xmlKeywordsConvert

class CompilationEngine(object):
    
    class TokensDecorator(object):

        def __init__(self, tokenizer):
            self.stack = []
            self.tokens = tokenizer

        def hasMoreTokens(self):
            return self.stack or self.tokens.hasMoreTokens()

        def advance(self):
            if self.stack:
                self.stack.pop()
            else:
                self.tokens.advance()

        def tokenType(self):
            if self.stack:
                return self.stack[-1](0)
            return self.tokens.tokenType()

        def getToken(self):
            if self.stack:
                return self.stack[-1](1)
            return str(self.tokens.getToken())

        def putBack(self, tp):
            self.stack.append(tp)

    def _indent(self):
        self.indentLevel += 3

    def _unindent(self):
        self.indentLevel -= 3

    def printTerminal(self):
        type = self.tokens.tokenType()
        value = self.tokens.getToken()
        if type == 'symbol':
            value = xmlKeywordsConvert(value)
        xmlTemplate = '{2}<{0}> {1} </{0}>'
        self._indent()
        spaces = ' ' * self.indentLevel
        print(xmlTemplate.format(type, value, spaces), file=self.outstream)
        self._unindent()

    def printNonTermOpen(self, type):
        self._indent()
        spaces = ' ' * self.indentLevel
        print('{1}<{0}>'.format(type, spaces), file=self.outstream)

    def printNonTermClose(self, type):
        spaces = ' ' * self.indentLevel
        print('{1}</{0}>'.format(type, spaces), file=self.outstream)
        self._unindent()

    def __init__(self, tokenizer, outstream):
        self.tokens = CompilationEngine.TokensDecorator(tokenizer)
        self.outstream = outstream
        self.indentLevel = 0

    def CompileClass(self):
        tokens = self.tokens
        print('<class>', file=self.outstream)
        assert(self.tokens.hasMoreTokens()); self.tokens.advance();
        self.printTerminal()
        assert(self.tokens.hasMoreTokens()); self.tokens.advance();
        self.printTerminal()
        assert(self.tokens.hasMoreTokens()); self.tokens.advance();
        self.printTerminal()
        assert(self.tokens.hasMoreTokens()); self.tokens.advance();
        while (True):
            if self.tokens.getToken() not in ['static', 'field']:
                break
            self.CompileClassVarDec()
        while (True):
            if self.tokens.tokenType() != 'keyword':
                break
            self.CompileSubroutineDec()

        self.printTerminal()
        print('</class>', file=self.outstream)

    def CompileClassVarDec(self):
        self.printNonTermOpen('classVarDec')
        self.printTerminal()
        assert(self.tokens.hasMoreTokens()); self.tokens.advance();
        self.printTerminal()
        assert(self.tokens.hasMoreTokens()); self.tokens.advance();
        self.printTerminal()
        assert(self.tokens.hasMoreTokens()); self.tokens.advance();
        while (self.tokens.getToken() == ','):
            self.printTerminal()
            assert(self.tokens.hasMoreTokens()); self.tokens.advance();
            self.printTerminal()
            assert(self.tokens.hasMoreTokens()); self.tokens.advance();
        self.printTerminal()
        assert(self.tokens.hasMoreTokens()); self.tokens.advance();
        self.printNonTermClose('classVarDec')

    def CompileSubroutineDec(self):
        self.printNonTermOpen('subroutineDec')
        self.printTerminal()
        assert(self.tokens.hasMoreTokens()); self.tokens.advance();
        self.printTerminal()
        assert(self.tokens.hasMoreTokens()); self.tokens.advance();
        self.printTerminal()
        assert(self.tokens.hasMoreTokens()); self.tokens.advance();
        self.printTerminal()
        assert(self.tokens.hasMoreTokens()); self.tokens.advance();
        self.compileParameterList()
        self.printTerminal()
        assert(self.tokens.hasMoreTokens()); self.tokens.advance();
        self.compileSubroutineBody()
        self.printNonTermClose('subroutineDec')

    def compileSubroutineBody(self):
        self.printNonTermOpen('subroutineBody')
        self.printTerminal()
        assert(self.tokens.hasMoreTokens()); self.tokens.advance();
        while self.tokens.getToken() == 'var':
            self.compileVarDec()
        self.compileStatements()
        self.printTerminal()
        assert(self.tokens.hasMoreTokens()); self.tokens.advance();
        self.printNonTermClose('subroutineBody')

    def compileParameterList(self):
        self.printNonTermOpen('parameterList')
        if self.tokens.tokenType() != 'symbol':
            self.printTerminal()
            assert(self.tokens.hasMoreTokens()); self.tokens.advance();
            self.printTerminal()
            assert(self.tokens.hasMoreTokens()); self.tokens.advance();
            while self.tokens.getToken() == ',':
                self.printTerminal()
                assert(self.tokens.hasMoreTokens()); self.tokens.advance();
                self.printTerminal()
                assert(self.tokens.hasMoreTokens()); self.tokens.advance();
                self.printTerminal()
                assert(self.tokens.hasMoreTokens()); self.tokens.advance();
        self.printNonTermClose('parameterList')

    def compileVarDec(self):
        self.printNonTermOpen('varDec')
        self.printTerminal()
        assert(self.tokens.hasMoreTokens()); self.tokens.advance();
        self.printTerminal()
        assert(self.tokens.hasMoreTokens()); self.tokens.advance();
        self.printTerminal()
        assert(self.tokens.hasMoreTokens()); self.tokens.advance();
        while self.tokens.getToken() == ',':
            self.printTerminal()
            assert(self.tokens.hasMoreTokens()); self.tokens.advance();
            self.printTerminal()
            assert(self.tokens.hasMoreTokens()); self.tokens.advance();
        self.printTerminal()
        assert(self.tokens.hasMoreTokens()); self.tokens.advance();
        self.printNonTermClose('varDec')

    def compileStatements(self):
        self.printNonTermOpen('statements')
        while True:
            if self.tokens.getToken() == 'let':
                self.compileLet()
            elif self.tokens.getToken() == 'do':
                self.compileDo()
            elif self.tokens.getToken() == 'while':
                self.compileWhile()
            elif self.tokens.getToken() == 'return':
                self.compileReturn()
            elif self.tokens.getToken() == 'if':
                self.compileIf()
            else:
                break
        self.printNonTermClose('statements')

    def compileDo(self):
        self.printNonTermOpen('doStatement')
        self.printTerminal()
        assert(self.tokens.hasMoreTokens()); self.tokens.advance();
        self.printTerminal()
        assert(self.tokens.hasMoreTokens()); self.tokens.advance();
        self.printTerminal()
        if (self.tokens.getToken() == '('):
            assert(self.tokens.hasMoreTokens()); self.tokens.advance();
            self.CompileExpressionList()
            self.printTerminal()
        else:
            assert(self.tokens.hasMoreTokens()); self.tokens.advance();
            self.printTerminal()
            assert(self.tokens.hasMoreTokens()); self.tokens.advance();
            self.printTerminal()
            assert(self.tokens.hasMoreTokens()); self.tokens.advance();
            self.CompileExpressionList()
            self.printTerminal()
        assert(self.tokens.hasMoreTokens()); self.tokens.advance();
        self.printTerminal()
        assert(self.tokens.hasMoreTokens()); self.tokens.advance();
        self.printNonTermClose('doStatement')

    def compileLet(self):
        self.printNonTermOpen('letStatement')
        self.printTerminal()
        assert(self.tokens.hasMoreTokens()); self.tokens.advance();
        self.printTerminal()
        assert(self.tokens.hasMoreTokens()); self.tokens.advance();
        if self.tokens.getToken() == '[':
            self.printTerminal()
            assert(self.tokens.hasMoreTokens()); self.tokens.advance();
            self.CompileExpression()
            self.printTerminal()
            assert(self.tokens.hasMoreTokens()); self.tokens.advance();
        self.printTerminal()
        assert(self.tokens.hasMoreTokens()); self.tokens.advance();
        self.CompileExpression()
        self.printTerminal()
        assert(self.tokens.hasMoreTokens()); self.tokens.advance();
        self.printNonTermClose('letStatement')

    def compileWhile(self):
        self.printNonTermOpen('whileStatement')
        self.printTerminal()
        assert(self.tokens.hasMoreTokens()); self.tokens.advance();
        self.printTerminal()
        assert(self.tokens.hasMoreTokens()); self.tokens.advance();
        self.CompileExpression()
        self.printTerminal()
        assert(self.tokens.hasMoreTokens()); self.tokens.advance();
        self.printTerminal()
        assert(self.tokens.hasMoreTokens()); self.tokens.advance();
        self.compileStatements()
        self.printTerminal()
        assert(self.tokens.hasMoreTokens()); self.tokens.advance();
        self.printNonTermClose('whileStatement')

    def compileReturn(self):
        self.printNonTermOpen('returnStatement')
        self.printTerminal()
        assert(self.tokens.hasMoreTokens()); self.tokens.advance();
        if self.tokens.getToken() != ';':
            self.CompileExpression()
        self.printTerminal()
        assert(self.tokens.hasMoreTokens()); self.tokens.advance();
        self.printNonTermClose('returnStatement')

    def compileIf(self):
        self.printNonTermOpen('ifStatement')
        self.printTerminal()
        assert(self.tokens.hasMoreTokens()); self.tokens.advance();
        self.printTerminal()
        assert(self.tokens.hasMoreTokens()); self.tokens.advance();
        self.CompileExpression()
        self.printTerminal()
        assert(self.tokens.hasMoreTokens()); self.tokens.advance();
        self.printTerminal()
        assert(self.tokens.hasMoreTokens()); self.tokens.advance();
        self.compileStatements()
        self.printTerminal()
        assert(self.tokens.hasMoreTokens()); self.tokens.advance();
        if self.tokens.getToken() == 'else':
            self.printTerminal()
            assert(self.tokens.hasMoreTokens()); self.tokens.advance();
            self.printTerminal()
            assert(self.tokens.hasMoreTokens()); self.tokens.advance();
            self.compileStatements()
            self.printTerminal()
            assert(self.tokens.hasMoreTokens()); self.tokens.advance();
        self.printNonTermClose('ifStatement')

    def CompileExpression(self):
        self.printNonTermOpen('expression')
        self.CompileTerm()
        while self.tokens.getToken() in '+-*/&|<>=':
            self.printTerminal()
            assert(self.tokens.hasMoreTokens()); self.tokens.advance();
            self.CompileTerm()
        self.printNonTermClose('expression')

    def CompileTerm(self):
        self.printNonTermOpen('term')
        self.printTerminal()
        if self.tokens.getToken() in '-~':
            assert(self.tokens.hasMoreTokens()); self.tokens.advance();
            self.CompileTerm()
        elif self.tokens.getToken() == '(':
            assert(self.tokens.hasMoreTokens()); self.tokens.advance();
            self.CompileExpression()
            self.printTerminal()
            assert(self.tokens.hasMoreTokens()); self.tokens.advance();
        else:
            assert(self.tokens.hasMoreTokens()); self.tokens.advance();
            if self.tokens.getToken() == '(':
                self.printTerminal()
                assert(self.tokens.hasMoreTokens()); self.tokens.advance();
                self.CompileExpressionList()
                self.printTerminal()
                assert(self.tokens.hasMoreTokens()); self.tokens.advance();
            elif self.tokens.getToken() == '[':
                self.printTerminal()
                assert(self.tokens.hasMoreTokens()); self.tokens.advance();
                self.CompileExpression()
                self.printTerminal()
                assert(self.tokens.hasMoreTokens()); self.tokens.advance();
            elif self.tokens.getToken() == '.':
                self.printTerminal()
                assert(self.tokens.hasMoreTokens()); self.tokens.advance();
                self.printTerminal()
                assert(self.tokens.hasMoreTokens()); self.tokens.advance();
                self.printTerminal()
                assert(self.tokens.hasMoreTokens()); self.tokens.advance();
                self.CompileExpressionList()
                self.printTerminal()
                assert(self.tokens.hasMoreTokens()); self.tokens.advance();
        self.printNonTermClose('term')

    def CompileExpressionList(self):
        self.printNonTermOpen('expressionList')
        if self.tokens.getToken() != ')':
            self.CompileExpression()
            while self.tokens.getToken() == ',':
                self.printTerminal()
                assert(self.tokens.hasMoreTokens()); self.tokens.advance();
                self.CompileExpression()
        self.printNonTermClose('expressionList')
