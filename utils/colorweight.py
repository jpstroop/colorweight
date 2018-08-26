#!/usr/bin/env python3

#
# Command line interface for ./color_analysis.py
#

from argparse import ArgumentParser
from argparse import SUPPRESS
from color_analysis import ImageAnalyzer

DESCRIPTION="""
A simple utility for analyzing images by their color.
"""

HELP = {

    'image' : """ The path to an image on the file system or an HTTP(S) URI.
If the arguement is a URI and does not appear to resolve to an image (by file
extension), an IIIF Image API service is assumed.""",

    'output' : """The path for the output file. The format will be determined by the file
extenstion: '.json' or '.png' are supported.""",

    'format' : """If --output is not specified, the format to dump to stdout.
'json' (default) or 'png' are supported.""",

    'geometry' : """The width and height of the output image. Ignored if
--output is json. (default: 400x100)""",

    'colors' : """The number of colors to report, e.g. 3 will report the top
three colors (default: 5)"""

#   -f, --format
#   -g, --geometry  "[W]x[H]" the width and height of the output image. Ignored
#                   if output is json. (default: 400x100)
#   -c, --colors


}

class ColorWeightCLI(object):

    def __init__(self):
        parser = ArgumentParser(description=DESCRIPTION, prog=__file__)
        # Positional
        parser.add_argument('image', type=str, help=HELP['image'])

        # Optional, mutually exclusive:
        group = parser.add_mutually_exclusive_group()
        group.add_argument('-o', '--output', metavar='PATH', help=HELP['output'])
        group.add_argument('-f', '--format', default='json', choices=['png', 'json'], help=HELP['format'])

        # Optional
        parser.add_argument('-g', '--geometry', metavar='WxH', type=str, default='400x100', help=HELP['geometry'])
        parser.add_argument('-c', '--colors', metavar='NUMBER', dest='n_colors', type=int, default=5, help=HELP['colors'])
        parser.add_argument('--debug', action='store_true', default=False, help=SUPPRESS)

        args = parser.parse_args()

        args.w, args.h = map(int, map(str.strip, args.geometry.split('x')))
        
        if args.debug:
            print('[DEBUG] raw args: {}'.format(args))
    #     self._set_props_from_args(args)
    #     print(args.w)
    #
    # def _set_props_from_args(self, args):
    #     'All the logic we explain in help'





if __name__ == '__main__':
    ColorWeightCLI()
