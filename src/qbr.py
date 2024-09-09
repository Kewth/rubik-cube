#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# vim: fenc=utf-8 ts=4 sw=4 et

import sys
import kociemba
import argparse
from video import webcam
import i18n
import os
import serialSend
from config import config
from constants import (
    ROOT_DIR,
    E_INCORRECTLY_SCANNED,
    E_ALREADY_SOLVED
)

# Set default locale.
locale = config.get_setting('locale')
if not locale:
    config.set_setting('locale', 'en')
    locale = config.get_setting('locale')

# Init i18n.
i18n.load_path.append(os.path.join(ROOT_DIR, 'translations'))
i18n.set('filename_format', '{locale}.{format}')
i18n.set('file_format', 'json')
i18n.set('locale', locale)
i18n.set('fallback', 'en')

class Qbr:

    def __init__(self, normalize):
        self.normalize = normalize

    def run(self):
        """The main function that will run the Qbr program."""
        state = webcam.run()
        print(state)

        # If we receive a number then it's an error code.
        if isinstance(state, int) and state > 0:
            if state == E_ALREADY_SOLVED:
                self.print_E_and_exit(state)
            print('Please input color in the console.')
            print('''
             |************|
             |*U1**U2**U3*|
             |************|
             |*U4**U5**U6*|
             |************|
             |*U7**U8**U9*|
             |************|
 ************|************|************|************
 *L1**L2**L3*|*F1**F2**F3*|*R1**R2**R3*|*B1**B2**B3*
 ************|************|************|************
 *L4**L5**L6*|*F4**F5**F6*|*R4**R5**R6*|*B4**B5**B6*
 ************|************|************|************
 *L7**L8**L9*|*F7**F8**F9*|*R7**R8**R9*|*B7**B8**B9*
 ************|************|************|************
             |************|
             |*D1**D2**D3*|
             |************|
             |*D4**D5**D6*|
             |************|
             |*D7**D8**D9*|
             |************|''')
            newState = ''
            def getFaceInput():
                while True:
                    res = input('>')
                    if len(res) == 8 and all([x in 'rgbwoy' for x in res]):
                        return res[:4] + '#' + res[4:]
            print('Input U-color (rgbwoy, skip center):')
            newState += getFaceInput().replace('#', 'U')
            print('Input R-color (rgbwoy, skip center):')
            newState += getFaceInput().replace('#', 'R')
            print('Input F-color (rgbwoy, skip center):')
            newState += getFaceInput().replace('#', 'F')
            print('Input D-color (rgbwoy, skip center):')
            newState += getFaceInput().replace('#', 'D')
            print('Input L-color (rgbwoy, skip center):')
            newState += getFaceInput().replace('#', 'L')
            print('Input B-color (rgbwoy, skip center):')
            newState += getFaceInput().replace('#', 'B')
            state = newState.replace('r', 'F').replace('y', 'U').replace('b', 'L').replace('o', 'B').replace('g', 'R').replace('w', 'D')

        try:
            algorithm = kociemba.solve(state)
            length = len(algorithm.split(' '))
        except Exception:
            self.print_E_and_exit(E_INCORRECTLY_SCANNED)

        solution = serialSend.trans(algorithm)
        print(solution)
        a = input('type ENTER to start')
        serialSend.send(solution)

        print(i18n.t('startingPosition'))
        print(i18n.t('moves', moves=length))
        print(i18n.t('solution', algorithm=algorithm))

        if self.normalize:
            for index, notation in enumerate(algorithm.split(' ')):
                text = i18n.t('solveManual.{}'.format(notation))
                print('{}. {}'.format(index + 1, text))

    def print_E_and_exit(self, code):
        """Print an error message based on the code and exit the program."""
        if code == E_INCORRECTLY_SCANNED:
            print('\033[0;33m[{}] {}'.format(i18n.t('error'), i18n.t('haventScannedAllSides')))
            print('{}\033[0m'.format(i18n.t('pleaseTryAgain')))
        elif code == E_ALREADY_SOLVED:
            print('\033[0;33m[{}] {}'.format(i18n.t('error'), i18n.t('cubeAlreadySolved')))
        sys.exit(code)

if __name__ == '__main__':
    # Define the application arguments.
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-n',
        '--normalize',
        default=False,
        action='store_true',
        help='Shows the solution normalized. For example "R2" would be: \
              "Turn the right side 180 degrees".'
    )
    args = parser.parse_args()

    # Run Qbr with all arguments.
    Qbr(args.normalize).run()
