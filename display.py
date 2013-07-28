#!/usr/bin/python

import argparse
import time

from trezor.display_buffer import DisplayBuffer
from trezor.display import Display
from trezor.layout import Layout
from trezor import DISPLAY_WIDTH, DISPLAY_HEIGHT

def parse_args():
    parser = argparse.ArgumentParser(description='Show message on SPI display.')

    parser.add_argument('-t', '--text', dest='text', default='', help='Message to display.Use pipe as a line delimiter.')
    parser.add_argument('-p', '--pygame', dest='pygame', action='store_true', help='Use pygame for rendering')
    parser.add_argument('-s', '--noquestion', dest='noquestion', action='store_true', help="Don't print the question bottom line")
    parser.add_argument('-y', '--yestext', dest='yestext', default='Confirm }', help="Text for 'Confirm'")
    parser.add_argument('-n', '--notext', dest='notext', default='', help="Text for 'Cancel'")
    return parser.parse_args()

def formatHexChars(txt):
    return ''.join(map(lambda x:x[1] if x[0]==0 else x[1][:2].decode('hex')+x[1][2:], enumerate(txt.split('\\x'))))

def main():
    args = parse_args()

    buff = DisplayBuffer(DISPLAY_WIDTH, DISPLAY_HEIGHT)
    display = Display(buff, spi=not args.pygame, virtual=args.pygame)
    display.init()

    # Initialize layout driver
    layout = Layout(buff)
    texts = map(formatHexChars, [args.yestext, args.notext])
    layout.show_message(formatHexChars(args.text).split('|'), question=not args.noquestion, options=texts)
    display.refresh()

    if args.pygame:
        while True:
            time.sleep(1)

if __name__ == '__main__':
    main()
