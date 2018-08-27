#!/usr/bin/env python3

#
# Command line interface for ./color_analysis.py
#

from argparse import Action
from argparse import ArgumentError
from argparse import ArgumentParser
from argparse import SUPPRESS
from color_analysis import ImageAnalyzer
from os.path import abspath
from os.path import dirname
from os.path import isdir

DESCRIPTION='A simple command line utility for analyzing images by their color.'

DEFAULT_WIDTH = 400
DEFAULT_HEIGHT = 100

FORMAT_CHOICES = ['png', 'json']

HELP = {

    'image' : """The path to an image on the file system or an HTTP(S) URI.
If the arguement is a URI and does not appear to resolve to an image (by file
extension), an IIIF Image API service is assumed.""",

    'output' : """The path for the output file. The format will be determined
by the file extenstion. '.json' or '.png' are supported.""",

    'format' : """If --output is not specified, the format to dump to stdout.
'json' (default) or 'png' are supported.""",

    'geometry' : """The width and height of the output image. Ignored if
--output is json. (default: {}x{})""".format(DEFAULT_WIDTH, DEFAULT_HEIGHT),

    'colors' : """The number of colors to report, e.g. 3 will report the top
three colors (default: 5)"""
}

class WHAction(Action):
    'Parse the WxH geometry into width and height'
    DEFAULT = '{}x{}'.format(DEFAULT_WIDTH, DEFAULT_HEIGHT)

    def __init__(self, option_strings, dest, **kwargs):
        # TODO: can we set defaults here, and will __call__ then override?
        super(WHAction, self).__init__(option_strings, dest,
            default=WHAction.DEFAULT, type=str, metavar='WxH',
            help=HELP['geometry'], **kwargs)

    def __call__(self, parser, namespace, values, option_string=None):
        w, h = map(int, map(str.strip, values.split('x')))
        setattr(namespace, 'width', w)
        setattr(namespace, 'height', h)

class OutputFormatAction(Action):
    'Set format based on the output path when --output is specified.'
    def __init__(self, option_strings, dest, **kwargs):
        super(OutputFormatAction, self).__init__(option_strings, dest,
            type=str, metavar='PATH', help=HELP['output'], **kwargs)

    def __call__(self, parser, namespace, values, option_string=None):
        fmt = values.split('.')[-1]
        if fmt not in FORMAT_CHOICES:
            m = '{} format is not supported ({})'.format(fmt, FORMAT_CHOICES)
            raise ArgumentError(self, m)
        # self._check_exists_and_writable(abspath(values))
        setattr(namespace, 'format', fmt)

    # TODO: do we need to check that the path is writable / exists, etc.? Or
    # are upstream errors good enough?
    # def _check_exists_and_writable(self, path):
    #     d = dirname(path)
    #     if not isdir(d):
    #         m = 'Specified output directory ({}/) does not exist or is not a directory'.format(d)
    #         raise ValueError(m)

class ColorWeightCLI(object):

    def __init__(self):
        parser = ArgumentParser(description=DESCRIPTION, prog=__file__)
        # Positional
        parser.add_argument('image', type=str, help=HELP['image'])

        # Optional, mutually exclusive:
        group = parser.add_mutually_exclusive_group()
        group.add_argument('-f', '--format', default='json', choices=FORMAT_CHOICES, help=HELP['format'])
        group.add_argument('-o', '--output', action=OutputFormatAction)

        # Suppressed options; w/h are set by --geometry
        # TODO: is there a way that we can make sure that the WHAction is
        # always called? Seems we don't have access to the namespace until
        # __call__ (i.e. not at __init__)
        parser.add_argument('--width', default=DEFAULT_WIDTH, help=SUPPRESS)
        parser.add_argument('--height', default=DEFAULT_HEIGHT, help=SUPPRESS)
        parser.add_argument('--debug', action='store_true', default=False, help=SUPPRESS)

        # Optional
        parser.add_argument('-g', '--geometry', action=WHAction)
        parser.add_argument('-c', '--colors', metavar='NUMBER', dest='n_colors', type=int, default=5, help=HELP['colors'])

        args = parser.parse_args()
        del args.geometry # use args.width and args.height going forward

        if args.debug:
            print('[DEBUG] raw args: {}'.format(args))

if __name__ == '__main__':
    ColorWeightCLI()
