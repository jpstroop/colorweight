from dataclasses import asdict
from dataclasses import dataclass
from json import dumps
from json import loads
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
        return dumps(self.to_dict())

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
    # {
    #   "relative_volume": 0.18552781289506953,
    #   "rgb": [107,90,63]
    # }
    relative_volume: float
    rgb: List[int] # May want this to be an object: Color(r,g,b)

@dataclass
class Image(_CWClass):
    __slots__ = ('colors', 'palette_image', 'source_image') #, '_color_variance')
    # {
    #   "colors": [
    #     { "relative_volume": 0.7999939143135346, "rgb": [98, 107, 103] },
    #     { "relative_volume": 0.10508763388510224, "rgb": [53, 25, 22] },
    #     { "relative_volume": 0.0949184518013632, "rgb": [186, 166, 138] }
    #   ],
    #   "palette_image": "0038.png",
    #   "source_image": "0038.jpg"
    # }
    colors: List[ColorVolume]
    palette_image: str
    source_image: str
    # _color_variance: float = None

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
    images: List[Image]

    # We could probably make the superclass handle lists; hack in the meantime:
    def to_jsons(self):
        return dumps(self.to_dict()['images'])

    @classmethod
    def from_dict_or_list(cls, l):
        images = [Image.from_dict_or_list(d) for d in l]
        return cls(images)

    @staticmethod
    def from_file(path):
        pass

# re: dataclasses:
# https://realpython.com/python-data-classes/
# https://docs.python.org/3/library/dataclasses.html

if __name__ == "__main__":
    # jsons = '{"relative_volume": 0.18552781289506953, "rgb": [107,90,63]}'
    # print(ColorVolume.from_jsons(jsons))

    jsons = '''[
      {
        "colors": [
          { "relative_volume": 0.7175252844500632, "rgb": [138, 118, 85] },
          { "relative_volume": 0.18552781289506953, "rgb": [107, 90, 63] },
          { "relative_volume": 0.058847977243994945, "rgb": [46, 37, 33] },
          { "relative_volume": 0.038098925410872314, "rgb": [195, 170, 144] }
        ],
        "palette_image": "0001.png",
        "source_image": "0001.jpg"
      },
      {
        "colors": [
          { "relative_volume": 0.5946930555555555, "rgb": [203, 173, 113] },
          { "relative_volume": 0.22485555555555556, "rgb": [158, 102, 55] },
          { "relative_volume": 0.1804513888888889, "rgb": [46, 34, 21] }
        ],
        "palette_image": "0002.png",
        "source_image": "0002.jpg"
      }
    ]'''
    i = ImageSet.from_jsons(jsons)
    print(i)
    print()
    print()
    print(i.to_jsons())


    # TODO: is there a way to inspect the __dataclass_fields__ so that
    # we can do from_dict_or_list in the superclass without knowing the class?
    # print(ColorVolume.__dataclass_fields__['relative_volume'].type == float)
    # print(ColorVolume.__dataclass_fields__['rgb'].type == List[int])
    # print(Image.__dataclass_fields__['colors'].type.__origin__ == list) # True
    # print(Image.__dataclass_fields__['colors'].type == List[ColorVolume]) # True
    # print(Image.__dataclass_fields__['colors'].type._name) #  string "List"
