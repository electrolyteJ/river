from enum import Enum, unique


@unique
class OutputFormat(Enum):
    TS = 0
    FLV = 1


class Muxer():
    def __init__(self, o, f):
        self.output = o
        self.output_format = f

    def addTrack(self, f):
        pass

    def start(self):
        pass

    def stop(self):
        pass

    def release(self):
        pass

    def writeSampleData(self):
        pass


def getInputBuffer():
    return True


def main():
    muxer = Muxer('xxx.mp3', OutputFormat.TS)
    muxer.start()
    finished = False
    while (not finished):
        finished = getInputBuffer()
    muxer.stop()
    muxer.release()


if __name__ == '__main__':
    main()
