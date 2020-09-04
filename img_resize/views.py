import os

from django.shortcuts import render, redirect
from django.core.files.base import ContentFile

from .models import Image
from .forms import UploadImageForm, SizeForm
from .utils import get_resized_image, get_image_by_url


def img_list_view(request):
    images = Image.objects.all()
    return render(request, 'img_resize/index.html', {'images': images})


def img_add_view(request):
    form = UploadImageForm(request.POST or None, request.FILES or None)
    if request.method == 'POST':
        if form.is_valid():
            img_file = form.cleaned_data.get('img')
            img_url = form.cleaned_data.get('url')

            if img_url:
                img_file = get_image_by_url(img_url)

            new_img = Image(img=img_file)
            new_img.save()
            return redirect(f"img/{new_img.id}")
    return render(request, 'img_resize/img_add.html', {'form': form})


def img_edit_view(request, img_id):
    img_obj = Image.objects.get(pk=img_id)
    filename = os.path.basename(img_obj.img.name)
    form = SizeForm(request.POST or None)

    if request.method == 'POST':
        if form.is_valid():
            height = int(request.POST.get('height') or 0)
            width = int(request.POST.get('width') or 0)

            image_io = get_resized_image(img_obj.img, width, height)
            img_obj.img_resized.save(
                name=filename,
                content=ContentFile(image_io.getvalue()),
                save=True
            )

    context = {'img_obj': img_obj,
               'img_filename': filename,
               'form': form,
               'img_id': img_id}
    return render(request, 'img_resize/img_edit.html', context)






