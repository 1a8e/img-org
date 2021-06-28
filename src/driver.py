import collections
import hashlib
import io
import os
import tqdm
import shutil
from PIL import Image, ExifTags, UnidentifiedImageError
from PIL.Image import DecompressionBombWarning

import warnings
warnings.filterwarnings("error")

Image.MAX_IMAGE_PIXELS = None


def get_image_size(img):
    """
    The function return REAL size of image
    """

    # Lets get exif information in a form of nice dict:
    # It will be something like: {'ResolutionUnit': 2, 'Orientation': 6, 'YCbCrPositioning': 1}

    if img._getexif():
        exif = {
            ExifTags.TAGS[k]: v
            for k, v in img._getexif().items()
            if k in ExifTags.TAGS
        }
    else:
        exif = {}

    size = img.size

    # If orientation is horizontal, lets swap width and height:
    if exif.get("Orientation", 0) > 4:
        size = (size[1], size[0])

    return size, 'w' if size[0]/size[1] > 1 else 't'


src_dir = 'D:\\Wall3\\'
dst_dir = 'D:\\Wall4\\'

filenames = os.listdir(src_dir)

file_hash_name_map = collections.defaultdict(list)

for filename in tqdm.tqdm(filenames):
    with open(os.path.join(src_dir, filename), 'rb') as image_file:
        try:
            extension = filename.split('.')[-1]
            read_image = image_file.read()
            file_hash = hashlib.sha1(read_image).hexdigest()
            image = Image.open(io.BytesIO(read_image))
            size, ratio = get_image_size(image)
            file_hash_name_map[f'{ratio}_{size[0]}_{file_hash}.{extension}'].append(filename)
        except (UnidentifiedImageError, DecompressionBombWarning) as err:
            print(f'Skipping {filename}: {file_hash}')
            continue


for file_hash, filenames in tqdm.tqdm(file_hash_name_map.items()):
    shutil.copy(os.path.join(src_dir, filenames[0]), os.path.join(dst_dir, file_hash))
