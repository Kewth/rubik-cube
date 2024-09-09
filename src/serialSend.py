import serial
import time

def trans(algorithm: str):
    res: bytes = b''
    for step in algorithm.split(' '):
        # clockwise
        if step == "L": res += b'l'
        if step == "R": res += b'r'
        if step == "U": res += b'u'
        if step == "D": res += b'd'
        if step == "F": res += b'f'
        if step == "B": res += b'b'
        # anti clockwise
        if step == "L'": res += b'L'
        if step == "R'": res += b'R'
        if step == "U'": res += b'U'
        if step == "D'": res += b'D'
        if step == "F'": res += b'F'
        if step == "B'": res += b'B'
        # twise
        if step == "L2": res += b'll'
        if step == "R2": res += b'rr'
        if step == "U2": res += b'uu'
        if step == "D2": res += b'dd'
        if step == "F2": res += b'ff'
        if step == "B2": res += b'bb'
    return res

def __send(solution: bytes):
    s = serial.Serial("COM15", 115200)
    time.sleep(1) # 非常重要！
    while not s.is_open:
        print('serial not open')
        time.sleep(1)
    s.write(solution)
    time.sleep(1)
    s.close()

def send(solution: bytes):
    print(solution)
    s = serial.Serial("COM15", 115200)
    time.sleep(1) # 非常重要！
    while not s.is_open:
        print('serial not open')
        time.sleep(1)
    s.write(solution)
    a = input('try again?')
    s.close()
    if a.strip() == 'yes':
        send(solution)

if __name__ == '__main__':
    send(b'flubdr')
    send(b'lufdrb')