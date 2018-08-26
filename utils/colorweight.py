#!/usr/bin/env python3

#
# Command line interface for ./color_analysis.py
#

from argparse import Action
from argparse import ArgumentParser
from argparse import SUPPRESS
from color_analysis import ImageAnalyzer

DESCRIPTION="""
A simple utility for analyzing images by their color.
"""

DEFAULT_WIDTH = 400
DEFAULT_HEIGHT = 100

HELP = {

    'image' : """ The path to an image on the file system or an HTTP(S) URI.
If the arguement is a URI and does not appear to resolve to an image (by file
extension), an IIIF Image API service is assumed.""",

    'output' : """The path for the output file. The format will be determined by the file
extenstion: '.json' or '.png' are supported.""",

    'format' : """If --output is not specified, the format to dump to stdout.
'json' (default) or 'png' are supported.""",

    'geometry' : """The width and height of the output image. Ignored if
--output is json. (default: {}x{})""".format(DEFAULT_WIDTH, DEFAULT_HEIGHT),

    'colors' : """The number of colors to report, e.g. 3 will report the top
three colors (default: 5)"""
}

class WHAction(Action):

    DEFAULT = '{}x{}'.format(DEFAULT_WIDTH, DEFAULT_HEIGHT)

    def __init__(self, option_strings, dest, **kwargs):
        super(WHAction, self).__init__(option_strings, dest,
            default=WHAction.DEFAULT, type=str, metavar='WxH',
            help=HELP['geometry'], **kwargs)

    def __call__(self, parser, namespace, values, option_string=None):
        w, h = map(int, map(str.strip, values.split('x')))
        setattr(namespace, 'width', w)
        setattr(namespace, 'height', h)

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
        parser.add_argument('-g', '--geometry', action=WHAction)
        parser.add_argument('-c', '--colors', metavar='NUMBER', dest='n_colors', type=int, default=5, help=HELP['colors'])
        parser.add_argument('--debug', action='store_true', default=False, help=SUPPRESS)

        args = parser.parse_args()

        self._tidy_and_default_geometry(args)

        if args.debug:
            print('[DEBUG] raw args: {}'.format(args))


    def _tidy_and_default_geometry(self, args):
        # TODO:
        # Seems lame that we have to do this but WHAction is only __call__ed if
        # a -g / --geometry arg is passed. Confirm there's not a way to always
        # have this called WHAction called. Custom actions seem kind of
        # pointless otherwise.
        if not(hasattr(args, 'width')): args.width = DEFAULT_WIDTH
        if not(hasattr(args, 'height')): args.height = DEFAULT_HEIGHT
        del args.geometry





if __name__ == '__main__':
    ColorWeightCLI()
