class PeekableStream:

    def __init__(self, stream):
        self.stream = stream
        self.pos = 0
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
            raise "End Of Stream"

        return ret