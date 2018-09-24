from dataclasses import asdict
from dataclasses import dataclass
from json import dumps
from json import loads
from statistics import pvariance
from typing import List

# TODO: __slots__

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
    def from_dict(cls, d):
        return cls(*d.values())

    @classmethod
    def from_jsons(cls, jsons):
        fields = cls.fields()
        json_d = loads(jsons)
        object_d = dict([(f, json_d[f]) for f in fields]) # we do this to ensure order
        return cls.from_dict(object_d)

@dataclass
class ColorVolume(_CWClass):
    # {
    #   "relative_volume": 0.18552781289506953,
    #   "rgb": [107,90,63]
    # }
    relative_volume: float
    rgb: List[int] # May want this to be an object: Color(r,g,b)

@dataclass
class Image(_CWClass):
    # {
    #   "colors": [
    #     { "relative_volume": 0.7999939143135346, "rgb": [98, 107, 103] },
    #     { "relative_volume": 0.10508763388510224, "rgb": [53, 25, 22] },
    #     { "relative_volume": 0.0949184518013632, "rgb": [186, 166, 138] }
    #   ],
    #   "palette_image": "0038.png",
    #   "source_image": "0038.jpg"
    # },
    colors: List[ColorVolume]
    palette_image: str
    source_image: None
    _color_variance: float = None

    @property
    def color_variance(self):
        if self._color_variance is None:
            volumes = [c.relative_volume for c in self.colors]
            self._color_variance = pvariance(volumes)
        return self._color_variance



# dataclasses:
# https://realpython.com/python-data-classes/
# https://docs.python.org/3/library/dataclasses.html

if __name__ == "__main__":
    jsons = '{"relative_volume": 0.18552781289506953, "rgb": [107,90,63]}'
    print(ColorVolume.from_jsons(jsons))
    # c = ColorVolume([1,2,3], 1.2)
    # print(type(c).__dataclass_fields__.keys())
    # c = Color({'r':1,'g':2,'b':3})
    # print(ColorVolume.__dataclass_fields__.keys())
