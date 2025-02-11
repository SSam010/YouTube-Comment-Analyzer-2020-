from captcha.fields import CaptchaField
from django.forms import ModelForm, TextInput, Textarea, HiddenInput

from .models import ChannelAdd


class ChannelAddForm(ModelForm):

    class Meta:
        model = ChannelAdd
        fields = ['channel_url', 'slug', 'channel_name', 'channel_desc', 'photo', 'user']

        widgets = {
            'channel_url': TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Channel link'
            }),
            'slug': HiddenInput(),
            'channel_name': TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Channel name'
            }),
            'channel_desc': Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Channel description'
            }),
            'user': HiddenInput()
        }
