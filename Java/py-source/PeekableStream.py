class PeekableStream:

    def __init__(self, stream): # Class Constructor
        # attribute
        self.stream = stream #this.stream = Strting stream (vis -)
        self.pos = 0        #this.pos = int (vis -)
        self.posStack = [] # this.posStack ArrayList (vis -)
        self.currentElem = self.stream[self.pos] # holds the current char (vis +)


    def nextElem(self):
        # Returns currentElem
        ret = self.currentElem

        # update the currentElem +1
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
