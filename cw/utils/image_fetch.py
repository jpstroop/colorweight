#!/usr/bin/env python

#
# Grabs all of the thumbnails from an IIIF Collection.
#

from os import makedirs
from os.path import dirname
from os.path import exists
from os.path import join
from os.path import realpath
from requests import get

class ImageCollector(object):

    def __init__(self, manifest_uri, iiif_params='/full/!800,800/0/default.jpg'):
        self.manifest_uri = manifest_uri
        self.iiif_params = iiif_params
        self._iiif_collection = None
        self._images_dir = None

    @property
    def images_dir(self):
        if self._images_dir is None:
            self._images_dir = realpath(join(dirname(realpath(__file__)), '..', 'images', 'ga'))
            makedirs(self._images_dir, exist_ok=True)
        return self._images_dir

    @property
    def iiif_collection(self):
        if self._iiif_collection is None:
            r = get(self.manifest_uri)
            r.raise_for_status()
            self._iiif_collection = IIIF_Collection(r.json())
        return self._iiif_collection

    def download_thumbnails(self):
        i = 1
        for thumbnail in image_collector.iiif_collection.thumbnail_data:
            url = '{}{}'.format(thumbnail[0], self.iiif_params)
            name = '{}.jpg'.format(str(i).zfill(4))
            i+=1
            path = join(self.images_dir, name)
            with open(path, 'wb') as f:
                print('Saving {} to {}'.format(url, path))
                r = get(url)
                f.write(r.content)


class IIIF_Collection(object):
    def __init__(self, iiif_collection_dict):
        self._iiif_collection = iiif_collection_dict
        self._thumbnail_data = None

    @property
    def thumbnail_data(self):
        if self._thumbnail_data is None:
            self._thumbnail_data = self._collect_thumbnail_data()
        return self._thumbnail_data

    def _collect_thumbnail_data(self):
        data = []
        for manifest in self._iiif_collection['manifests']:
            label = manifest.get('label')[0]
            manifest_id = manifest.get('@id')
            thumbnail_id = None
            try:
                thumbnail_id = manifest['thumbnail']['service']['@id']
            except KeyError:
                pass
            else:
                data.append((thumbnail_id, label, manifest_id))
        return data

# TODO: script could take this as an arg.
PUL_COLLECTIONS = "https://figgy.princeton.edu/collections/"
MANIFEST = "/manifest"

ALPHABET_BOOKS = 'deeb2da4-7db2-4514-b9b9-a6c76e164097'
GA = 'b80f8d41-3be5-440e-8bdb-eff6489f3088'
COTSEN = '0a73e8fb-3ab4-4943-9f10-0855b18e7677'
SOVIET_SHEET_MUSIC = '058c1862-30dc-431c-90b5-4e141282c7a1'
SOVIET_CHILDRENS_BOOKS = '0f9c665a-a16c-4cf3-a29e-1c2077222e0b'

def figgy_iiif_uri(id):
    return f'{PUL_COLLECTIONS}{id}{MANIFEST}'

if __name__ == '__main__':
    image_collector = ImageCollector(figgy_iiif_uri(GA))
    image_collector.download_thumbnails()
