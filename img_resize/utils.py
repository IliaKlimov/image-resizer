from io import BytesIO
from PIL import Image as PIL_Image
from urllib.error import HTTPError
from urllib.request import urlretrieve
from urllib.parse import urlparse

from django.core.files.uploadedfile import SimpleUploadedFile
from django.shortcuts import HttpResponse

def get_image_by_url(url):
    try:
        tmp_file = urlretrieve(url)[0]
    except HTTPError:
        return None

    basename = urlparse(url).path.split('/')[-1]
    img_file = SimpleUploadedFile(basename, open(tmp_file, "rb").read())
    return img_file

def get_resized_image(img_path, width, height):
    img = PIL_Image.open(img_path)

    width_orig, height_orig = img.size
    if not width:
        multiplier = height / height_orig
    elif not height:
        multiplier = width / width_orig
    else:
        multiplier = min(height / height_orig, width / width_orig)

    newsize = (int(width_orig * multiplier) or 1, int(height_orig * multiplier) or 1)
    resized_img = img.resize(newsize)
    output_io = BytesIO()
    print("griiiiiing", img.format)
    resized_img.save(output_io, format=img.format, quality=90
                     )
    return output_io

