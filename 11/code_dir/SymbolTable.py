
class SymbolTable(object):

    class Scopes(object):

        def __init__(self, numTables, auxConstructor, auxGetCb, auxSetCb):
            # list of tuples (dictionary, min free index)
            self.auxConstructor = auxConstructor
            self.auxGetCb = auxGetCb
            self.auxSetCb = auxSetCb
            self.tables = [self._newTable() for i in range(numTables)]

        def _newTable(self):
            return [dict(), self.auxConstructor()]

        def __getitem__(self, key):
            tables = self.tables
            for i in range(0, len(tables)):
                table, auxData = tables[i]
                curValue = table.get(key)
                if (curValue == None):
                    continue
                self.tables[i] = [table, self.auxGetCb(auxData)]
                return curValue
            raise KeyError(key)

        def putItem(self, key, value, tableIndex):
            tableData = self.tables[tableIndex]
            table, aux = tableData
            table[key] = value
            self.tables[tableIndex] = table, self.auxSetCb(aux, value)

        def getAuxData(self, tableIndex):
            _, aux = self.tables[tableIndex]
            return aux

        def resetTable(self, tableIndex):
            self.tables[tableIndex] = self._newTable()
            
    identifier_kinds = ['static', 'field', 'arg', 'var']

    def __init__(self):
        auxConstructor = lambda: [0, 0]
        auxGetCb = lambda x: x
        def auxSetCb(x, val): 
            y = x[:]
            y[self._freeLsIndex(val[1])] += 1
            return y
        # subroutine scope -> class scope
        self.scopes = SymbolTable.Scopes(2, auxConstructor, 
                                         auxGetCb, auxSetCb)

    def startSubroutine(self):
        # reset names in subroutine scope
        self.scopes.resetTable(0)

    def define(self, name, type, kind):
        tableIndex = self._getTableIndex(kind)
        freeIndexLs = self.scopes.getAuxData(tableIndex)
        if kind in ['field', 'var']:
            freeIndex = freeIndexLs[1]
        else:
            freeIndex = freeIndexLs[0]
        value = (type, kind, freeIndex)
        self.scopes.putItem(name, value, tableIndex)

    def _getTableIndex(self, kind):
        if kind in SymbolTable.identifier_kinds[:2]:
            tableIndex = 1
        elif kind in SymbolTable.identifier_kinds[2:]:
            tableIndex = 0
        else:
            raise Exception("Unlisted kind of variable: {0}".format(kind))
        return tableIndex

    def _freeLsIndex(self, kind):
        if kind in ['field', 'var']:
            return 1
        elif kind in ['static', 'arg']:
            return 0

    def numVars(self, kind):
        tableIndex = self._getTableIndex(kind)
        freeLs = self.scopes.getAuxData(tableIndex)
        return freeLs[self._freeLsIndex(kind)]

    def kindOf(self, name):
        _, kind, _ = self.scopes[name]
        return self._convert(kind)

    def _convert(self, kind):
        if kind == 'var':
            kind = 'local'
        elif kind == 'arg':
            kind = 'argument'
        return kind

    def typeOf(self, name):
        type, _, _ = self.scopes[name]
        return type

    def indexOf(self, name):
        _, _, index = self.scopes[name]
        return index
