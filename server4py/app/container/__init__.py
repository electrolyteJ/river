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


def print_ts_packet(ts_packet):
    s = ''
    adaptation_field_control = 0x01
    adaptation_field_length = 0
    payload_unit_start_indicator = 0
    for jj in range(0, 188):
        p = ts_packet[jj]
        if jj == 1:
            payload_unit_start_indicator = p >> 6 & 0b01
            print("payload_unit_start_indicator", bin(payload_unit_start_indicator))
        elif jj == 3:
            adaptation_field_control = (p >> 4) & 0b0011
            print('adaptation_field_control', bin(adaptation_field_control))
        if jj == 4 and adaptation_field_control & 0b10 == 0b10:
            adaptation_field_length = p
            print('adaptation_field_length', adaptation_field_length)

        if len(s) == 0:
            s = hex(p)
        elif jj == 4:
            s = s + ',\n' + hex(p)
        elif adaptation_field_control & 0b10 == 0b10 and adaptation_field_length + 4 == jj:
            s = s + ',\n' + hex(p)
        elif payload_unit_start_indicator == 1 and jj == adaptation_field_length + 5:
            s = s + ',\n\u001B[31mpes header:\u001B[0m' + hex(p)
        elif payload_unit_start_indicator == 1 and jj == adaptation_field_length + 5 + 19:
            s = s + ',\n\u001B[31mpes payload:\u001B[0m' + hex(p)
        else:
            s = s + ',' + hex(p)

    print(s)



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
