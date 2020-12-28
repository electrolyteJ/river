import sys
#求最简质因数
def cacl(a, b):
    for i in range(2, 10):
        if (a % i == 0) and (b % i == 0):
            return cacl(a//i, b//i)
    return a, b


nums = [
    (2244, 1080), (2340, 1080), (1920, 1080), (1440, 1080),(0,0),
    (1560, 720),(1280, 720), (960, 720),(0,0),
    (960, 544), (720, 544),(0,0),
    (848, 480), (640, 480),(0,0),
    (424, 240), (320, 240),(0,0),
]
if __name__ == "__main__":
    # for n in nums:
    #     h, w = n
    #     if h  == 0 and w==0:
    #         print('='*20)
    #     else:
    #         print(cacl(h, w))
    print(sys.maxsize)
