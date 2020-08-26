from urllib.error import HTTPError
from urllib.request import urlretrieve
from urllib.parse import urlparse
import os
from PIL import Image as PIL_Image
from io import BytesIO

from django.shortcuts import render, redirect, HttpResponse
from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.files.base import ContentFile

from .models import Image
from .forms import UploadImageForm, SizeForm


def index(request):
    images = Image.objects.all()
    return render(request, 'img_resize/index.html', {'images': images})


def add_new_image_view(request):
    form = UploadImageForm(request.POST or None, request.FILES or None)

    if request.method == 'POST':
        if form.is_valid():
            img_file = form.cleaned_data.get('img')
            img_url = form.cleaned_data.get('url')

            if img_url:
                img_file = _get_image_by_url(img_url)

            new_img = Image(img=img_file)
            new_img.save()
            return redirect(f"img/{new_img.id}")
    return render(request, 'img_resize/img_add.html', {'form': form})


def img_edit(request, img_id):
    img_obj = Image.objects.get(pk=img_id)
    filename = os.path.basename(img_obj.img.name)
    form = SizeForm(request.POST or None)

    if request.method == 'POST':
        if form.is_valid():
            print("valid")
            height = int(request.POST.get('height'))
            width = int(request.POST.get('width'))

            image_io = _resize_image(img_obj.img, width, height)
            img_obj.img_resized.save(
                name=filename,
                content=ContentFile(image_io.getvalue()),
                save=True,
            )

    context = {'img_obj': img_obj,
               'img_filename': filename,
               'form': form,
               'img_id': img_id}
    return render(request, 'img_resize/img_edit.html', context)


def _resize_image(img_path, width, height):
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
    resized_img.save(output_io, format=img.format, quality=100)
    return output_io


def _get_image_by_url(url):
    try:
        tmp_file = urlretrieve(url)[0]
    except HTTPError:
        return HttpResponse("Не удалось скачать изображение")

    basename = urlparse(url).path.split('/')[-1]
    img_file = SimpleUploadedFile(basename, open(tmp_file, "rb").read())
    return img_file
