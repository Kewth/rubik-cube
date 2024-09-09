import kociemba
import magiccube
from magiccube.cube_base import Color, Face
import random
import serialSend

if __name__ == '__main__':
    cube = magiccube.Cube(3,"YYYYYYYYYBBBBBBBBBRRRRRRRRRGGGGGGGGGOOOOOOOOOWWWWWWWWW")
    shuffle_length = 30
    shuffle_algorithm = ' '.join([random.choice("LRBFUD") for _ in range(shuffle_length)])
    cube.rotate(shuffle_algorithm)
    shuffle_steps = serialSend.trans(shuffle_algorithm)
    print(shuffle_steps)
    serialSend.send(shuffle_steps)
    oState = ''
    for f in [Face.U, Face.R, Face.F, Face.D, Face.L, Face.B]:
        for c in cube.get_face_flat(f):
            oState += c.name
    cubeState = oState.replace(' ', '').replace('\n', '').lower()
    state = cubeState.replace('r', 'F').replace('y', 'U').replace('b', 'L').replace('o', 'B').replace('g', 'R').replace('w', 'D')
    print(state)
    sol_algorithm = kociemba.solve(state)
    print(sol_algorithm)
    cube.rotate(sol_algorithm)
    print(cube)
    sol_steps = serialSend.trans(sol_algorithm)
    print(sol_steps)
    serialSend.send(sol_steps)