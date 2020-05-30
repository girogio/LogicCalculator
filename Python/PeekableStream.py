class PeekableStream:

    def __init__(self, stream):
        self.stream = stream
        self.pos = 0
        self.posStack = []
        self.currentElem = self.stream[self.pos]


    def nextElem(self):
        ret = self.currentElem

        if self.pos < len(self.stream):
            self.pos += 1

            try:
                self.currentElem = self.stream[self.pos]
            except IndexError:
                self.currentElem = None

        else:
            raise "End Of Stream."

        return ret


    def prevElem(self):
        ret = self.currentElem
        self.pos -= 1

        if self.pos >= 0:
            self.currentElem = self.stream[self.pos]
        else:
            self.pos += 1
            raise "Beginning Of Stream."

        return ret


    def pushPos(self):
        self.posStack.append(self.pos)

    def popPos(self):
        pos = self.posStack.pop()
        self.pos = pos
        self.currentElem = self.stream[self.pos]
