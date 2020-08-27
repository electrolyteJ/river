from urllib.parse import urlparse
import os
EXTM3U = '#EXTM3U'
EXT_X_VERSION = '#EXT-X-VERSION'
EXT_X_ALLOW_CACHE = '#EXT-X-ALLOW-CACHE'
EXT_X_TARGETDURATION = '#EXT-X-TARGETDURATION'
EXT_X_MEDIA_SEQUENCE = '#EXT-X-MEDIA-SEQUENCE'
EXTINF = '#EXTINF'
VERSION = 3


class M3u8:
    max_duration_per_segment = ''
    segments = list()

    def __init__(self, max_duration_per_segment, segments):
        self.max_duration_per_segment = str(max_duration_per_segment)
        self.segments = segments


class Segment:
    cur_seq_num = -1
    duration = ''
    title = ''
    resource = ''

    def __init__(self, duration, title, resource):
        self.duration = str(duration)
        self.title = title
        self.resource = resource
        # https: // priv.example.com/{}.{:05d}.ts
        filename = os.path.basename(resource)
        self.cur_seq_num = int(filename.split('.')[1])


def gen_live(m3u8_info):
    '''
        # EXTM3U
        # EXT-X-VERSION:3
        # EXT-X-TARGETDURATION:8
        # EXT-X-MEDIA-SEQUENCE:2680

        # EXTINF:7.975,
        https://priv.example.com/fileSequence2680.ts
        # EXTINF:7.941,
        https://priv.example.com/fileSequence2681.ts
        # EXTINF:7.975,
        https://priv.example.com/fileSequence2682.ts
    '''
    if (m3u8_info is None
            or m3u8_info.segments is None
            or len(m3u8_info.segments) == 0):
        return ''
    seq_num = m3u8_info.segments[0].cur_seq_num
    d = m3u8_info.max_duration_per_segment
    m3u8_header = _gen_header_temple(True) % (VERSION, d, seq_num)
    return m3u8_header+_gen_body(m3u8_info.segments)


def gen_vod(m3u8_info):
    '''
        # EXTM3U
        # EXT-X-TARGETDURATION:10
        # EXT-X-VERSION:3
        # EXTINF:9.009,
        http://media.example.com/first.ts
        # EXTINF:9.009,
        http://media.example.com/second.ts
        # EXTINF:3.003,
        http://media.example.com/third.ts
        # EXT-X-ENDLIST
    '''
    if (m3u8_info is None
        or m3u8_info.segments is None
            or len(m3u8_info.segments) == 0):
        return ''
    d = m3u8_info.max_duration_per_segment
    header = _gen_header_temple(False) % (VERSION, d)
    footer = '#EXT-X-ENDLIST'
    body = _gen_body(m3u8_info.segments)
    return header+body+footer


def _gen_body(segments):
    m3u8_body = ''
    for seg in segments:
        m3u8_body = m3u8_body+'#EXTINF:%s,%s\n%s\n' % (seg.duration, seg.title, seg.resource)
    return m3u8_body


def _gen_header_temple(islive):
    m3u8_temple = '#EXTM3U\n#EXT-X-VERSION:%d\n#EXT-X-ALLOW-CACHE:NO\n#EXT-X-TARGETDURATION:%s\n'
    if islive:
        m3u8_temple = m3u8_temple+'#EXT-X-MEDIA-SEQUENCE:%d\n'
    else:
        pass
    return m3u8_temple


def main():
    segs = [
        Segment(10.3, 'cjf', 'https://priv.example.com/abc12.0.ts'),
        Segment(10, 'cjf', 'https://priv.example.com/abc12.1.ts'),
        Segment(10, 'cjf', 'https://priv.example.com/abc12.2.ts'),
        Segment(10, 'cjf', 'https://priv.example.com/abc12.3.ts'),
        Segment(10, 'cjf', 'https://priv.example.com/abc12.4.ts'),
        Segment(10, 'cjf', 'https://priv.example.com/abc12.5.ts'),
        Segment(10, 'cjf', 'https://priv.example.com/abc12.6.ts'),
        ]
    m3u8 = M3u8(15.3, segs)
    print('{:=^30}'.format('live m3u8'))
    m3u8_file = gen_live(m3u8)
    print(m3u8_file)
    print('{:=^30}'.format('vod m3u8'))
    m3u8_file = gen_vod(m3u8)
    print(m3u8_file)


if __name__ == '__main__':
    main()
