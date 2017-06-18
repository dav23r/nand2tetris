
class VMWriter(object):

    def __init__(self, outstream):
        self.out = outstream

    def writePush(self, segment, index):
        print('push {0} {1}'.format(segment, index), file=self.out)

    def writePop(self, segment, index):
        print('pop {0} {1}'.format(segment, index), file=self.out)

    def writeArithmetic(self, command):
        print('{0}'.format(command), file=self.out)

    def writeLabel(self, label):
        print('label {0}'.format(label), file=self.out)

    def writeGoto(self, label):
        print('goto {0}'.format(label), file=self.out)

    def writeIf(self, label):
        print('if-goto {0}'.format(label), file=self.out)

    def writeCall(self, name, nArgs):
        print('call {0} {1}'.format(name, nArgs), file=self.out)

    def writeFunction(self, name, nLocals):
        print('function {0} {1}'.format(name, nLocals), file=self.out)

    def writeReturn(self):
        print('return', file=self.out)

    def close(self):
        self.out.close()
