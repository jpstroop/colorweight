# ColorWeight

Visualize (and eventually index) images by their dominant colors.

Right now, given an image like this:

![some book cover](https://raw.githubusercontent.com/jpstroop/colorweight/master/samples/01_in.jpg)

You can get this:

![sample output](https://raw.githubusercontent.com/jpstroop/colorweight/master/samples/01_out.png)

or the data it took to make that image, for further processing, indexing, etc.

```json
[
  {
    "relative_volume": 0.4103605514316013,
    "rgb": [ 92, 112, 117 ]
  },
  {
    "relative_volume": 0.3718001060445387,
    "rgb": [ 45, 39, 28 ]
  },
  {
    "relative_volume": 0.14360683987274656,
    "rgb": [ 168, 84, 44 ]
  },
  {
    "relative_volume": 0.07423250265111347,
    "rgb": [ 195, 171, 129 ]
  }
]

```


See `util/color_analysis.py` for details and options.

## Installation

 * Install [Pipenv](https://packaging.python.org/tutorials/managing-dependencies/#installing-pipenv): `brew install pipenv`
 * Install dependencies: `pipenv install`
 * Activate the environment: `pipenv shell`
 * Check out the command line interface in `cw/utils/colorweight.py`

    ```
     usage: cw/utils/colorweight.py [-h] [-f {png,json} | -o PATH] [-g WxH]
                                    [-c NUMBER]
                                    image

     A simple command line utility for analyzing images by their color.

     positional arguments:
       image                 The path to an image on the file system or an HTTP(S)
                             URI. If the arguement is a URI and does not appear to
                             resolve to an image (by file extension), an IIIF Image
                             API service is assumed.

     optional arguments:
       -h, --help            show this help message and exit
       -f {png,json}, --format {png,json}
                             If --output is not specified, the format to dump to
                             stdout. 'json' (default) or 'png' are supported.
       -o PATH, --output PATH
                             The path for the output file. The format will be
                             determined by the file extenstion. '.json' or '.png'
                             are supported.
       -g WxH, --geometry WxH
                             The width and height of the output image. Ignored if
                             --output is json. (default: 400x100)
       -c NUMBER, --colors NUMBER
                             The number of colors to report, e.g. -c 3 will report
                             the top three colors. If this number is not provided,
                             numbers 1-12 will be tried in order to determine an
                             optimal number. This number of colors will be
                             reported. This can take a long time.
    ```
    ... or import and play with `cw/utils/color_analysis.py`
