from django import forms
from .models import Image


class UploadImageForm(forms.Form):
    url = forms.CharField(label='Ссылка', required=False)
    img = forms.ImageField(label='Файл', required=False)

    def clean(self):
        cleaned_data = super().clean()
        cleaned_img = cleaned_data.get('img')
        cleaned_url = cleaned_data.get('url')

        if cleaned_img and cleaned_url:
            raise forms.ValidationError("Вы задали и локальный файл и внешнюю ссылку. Выберите что-то одно")

        if not cleaned_img and not cleaned_url:
            raise forms.ValidationError("Ни одно из полей не заполнено")

        return cleaned_data


class SizeForm(forms.Form):
    width = forms.IntegerField(label='Ширина', required=False)
    height = forms.IntegerField(label='Высота', required=False)

    def clean_width(self):
        width = self.cleaned_data.get('width')
        if width is not None and width < 1:
            raise forms.ValidationError("Укажите ширину больше 0")
        return width

    def clean_height(self):
        height = self.cleaned_data.get('height')
        if height is not None and height < 1:
            raise forms.ValidationError("Укажите высоту больше 0")
        return height

    def clean(self):
        cleaned_data = super().clean()
        width_ = cleaned_data.get('width')
        height_ = cleaned_data.get('height')
        if width_ is None and height_ is None:
            raise forms.ValidationError("Заполните хотя бы одно поле")
        return cleaned_data
