#!/usr/bin/env python3

#
# Command line interface for ./color_analysis.py
#

from argparse import Action
from argparse import ArgumentError
from argparse import ArgumentParser
from argparse import SUPPRESS
from color_analysis import ImageAnalyzer # TODO: shoud be utils.color_analysis
from cv2 import imwrite
from errno import EACCES
from json import dumps
from os.path import abspath
from os.path import dirname
from os.path import isdir
from sys import stdout
from tempfile import TemporaryFile

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

    'geometry' : f"""The width and height of the output image. Ignored if
--output is json. (default: {DEFAULT_WIDTH}x{DEFAULT_HEIGHT})""",

    'colors' : """The number of colors to report, e.g. -c 3 will report the top
three colors (default: 5)"""
}

class GeometryAction(Action):
    'Parse the WxH geometry into width and height'
    DEFAULT = f'{DEFAULT_WIDTH}x{DEFAULT_HEIGHT}'

    def __init__(self, option_strings, dest, **kwargs):
        # TODO: can we set defaults here, and will __call__ then override?
        super(GeometryAction, self).__init__(option_strings, dest,
            default=GeometryAction.DEFAULT, type=str, metavar='WxH',
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
            m = f'{fmt} format is not supported ({FORMAT_CHOICES !r})'
            raise ArgumentError(self, m)
        self._check_exists_and_writable(abspath(values))
        setattr(namespace, 'format', fmt)
        setattr(namespace, 'output', values)

    def _check_exists_and_writable(self, path):
        d = dirname(path)
        if not isdir(d):
            m = f'Specified output directory ({d}/) does not exist or is not a directory'
            raise ArgumentError(self, m)
        if not OutputFormatAction._is_writeable(d):
            m = f'Specified output directory ({d}/) is not writeable'
            raise ArgumentError(self, m)

    @staticmethod
    def _is_writeable(path):
        try:
            testfile = TemporaryFile(dir=path)
            testfile.close()
        except OSError as e:
            if e.errno == EACCES:
                return False
            else:
                raise # unhandled until we know what else might come up
        return True

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
        # TODO: is there a way that we can make sure that the GeometryAction is
        # always called? Seems we don't have access to the namespace until
        # __call__ (i.e. not at __init__)
        # Update: See https://stackoverflow.com/questions/21583712/cause-pythons-argparse-to-execute-action-for-default
        parser.add_argument('--width', default=DEFAULT_WIDTH, help=SUPPRESS)
        parser.add_argument('--height', default=DEFAULT_HEIGHT, help=SUPPRESS)
        parser.add_argument('--debug', action='store_true', default=False, help=SUPPRESS)

        # Optional
        parser.add_argument('-g', '--geometry', action=GeometryAction)
        parser.add_argument('-c', '--colors', metavar='NUMBER', dest='n_colors', type=int, default=5, help=HELP['colors'])

        args = parser.parse_args()
        del args.geometry # use args.width and args.height going forward

        if args.debug:
            print(f'[DEBUG] raw args: {args}')

        self.args = args

    def execute(self):
        analyzer = ImageAnalyzer(self.args.image)
        # Args is an argparse.Namespace object. E.g.:
        # Namespace(debug=True, format='json', height=100, image='foo.png',
        #    n_colors=5, output=None, width=400)
        if self.args.format == 'json':
            outstream = stdout
            if self.args.output is not None:
                outstream = open(self.args.output, 'w')
            data = analyzer.list(n_colors=self.args.n_colors)
            json_s = dumps(data, indent=2, sort_keys=True)
            print(json_s, file=outstream)
        else:
            image_data = analyzer.viz(n_colors=self.args.n_colors,
                height=self.args.height, width=self.args.width)
            if self.args.output is not None:
                imwrite(self.args.output, image_data)
            else: # Probably useless, but keeps CLI the API easy :-)
                print(image_data.tostring())

        # JSON or Image?

if __name__ == '__main__':
    cli = ColorWeightCLI()
    cli.execute()
