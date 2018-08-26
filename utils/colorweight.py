#!/usr/bin/env python3

#
# Command line interface for ./color_analysis.py
#
# Positional arguments:
#  image            The path to an image on the file system or an HTTP(S) URI.
#                   If the arguement is a URI and does not appear to resolve
#                   to an image (by file extension), an IIIF Image API service
#                   is assumed.
#
#
# Optional arguments:
#   -h, --help      Show help and exit.
#   -o, --output    The path for the output file. The format will be determined
#                   by the file extenstion: '.json' or '.png' are supported
#   -f, --format    If --output is not specified, the format to dump to stdout.
#                   'json' (default) or 'png' are supported.
#   -g, --geometry  "[W]x[H]" the width and height of the output image. Ignored
#                   if output is json. (default: 400x100)
#   -c, --colors    The number of colors to report (default: 5)
#

from utils.color_analysis import ImageAnalyzer
