# ColorWeight

Visualize (and eventually index) images by their dominant colors.

Right now, given an image like this:

![some book cover](https://raw.githubusercontent.com/jpstroop/colorweight/master/samples/01_in.jpg)

You can get this:

![sample output](https://raw.githubusercontent.com/jpstroop/colorweight/master/samples/01_out.png)

or the data it took to make that image, for further processing, indexing, etc. See `util/color_analysis.py` for details and options.

## Installation

 * Install [Pipenv](https://packaging.python.org/tutorials/managing-dependencies/#installing-pipenv): `brew install pipenv`
 * Install dependencies: `pipenv install`
 * Activate the environment: `pipenv shell`
 * Play with `utils/color_analysis.py`

## Download some Images

See `__main__` in `utils/image_fetch.py`.
