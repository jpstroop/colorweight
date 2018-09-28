from dataclasses import asdict
from dataclasses import dataclass
from json import dumps
from json import loads
from json import load
from statistics import pvariance
from typing import List

# NB: This is a set of models that make it easy to work w/ JSON files. They
# may need to be re-implemented for SQL or some other persistent storage at
# some point (e.g. doing the K-Means clustering on image is time intensive,
# and it would be nice to put those on a job queue.)

@dataclass
class _CWClass:
    def to_dict(self):
        return asdict(self)

    def to_jsons(self):
        return dumps(self.to_dict(), sort_keys=True, indent=2)

    @classmethod
    def fields(cls):
        return list(cls.__dataclass_fields__.keys())

    @classmethod
    def from_dict_or_list(cls, d):
        return cls(*d.values())

    @classmethod
    def from_jsons(cls, jsons):
        json_obj = loads(jsons)
        if isinstance(json_obj, list):
            constructor = json_obj
        else:
            constructor = dict([(f, json_obj[f]) for f in cls.fields()]) # ensure order
        return cls.from_dict_or_list(constructor)

@dataclass
class ColorVolume(_CWClass):
    __slots__ = ('relative_volume', 'rgb')
    relative_volume: float
    rgb: List[int] # May want this to be an object: Color(r,g,b)

@dataclass
class Image(_CWClass):
    __slots__ = ('colors', 'palette_image', 'source_image')
    colors: List[ColorVolume]
    palette_image: str
    source_image: str

    @property
    def color_variance(self):
        # TODO: figure out how to memoize w/ dataclass & slots
        return pvariance([c.relative_volume for c in self.colors])

    @classmethod
    def from_dict_or_list(cls, d):
        colors = [ColorVolume(*c.values()) for c in d['colors']]
        return cls(colors, *list(d.values())[1:])

@dataclass
class ImageSet(_CWClass):
    __slots__ = ('_images',)
    # TODO: also make this a subclass of list, or else find a way to
    # delegate some or all list-like methods to ._images, as below with
    # __getitem__
    _images: List[Image]

    def __getitem__(self, position):
        return self._images[position]
    def __len__(self):
        return len(self._images)
    def __reversed__(self):
        return self._images[::-1]

    # We could probably make the superclass handle lists; hack in the
    # meantime. See above also.
    def to_jsons(self):
        return dumps(self.to_dict()['_images'])

    @classmethod
    def from_dict_or_list(cls, l):
        images = [Image.from_dict_or_list(d) for d in l]
        return cls(images)

    @staticmethod
    def from_file(path):
        with open(path, 'r') as f:
            d = load(f)
            set = ImageSet.from_dict_or_list(d)
        return set

if __name__ == "__main__":
    set = ImageSet.from_file('/Users/jstroop/workspace/colorweight/data.json')
    print(reversed(set))
