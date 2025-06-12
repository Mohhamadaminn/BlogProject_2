from .models import CustomUser
from django import forms
from django.contrib.auth.forms import UserCreationForm


class CustomUserCreationForm(UserCreationForm):
  
  email = forms.EmailField()  # email required.

  class Meta:
      model = CustomUser
      fields = ['username', ]

  def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({
                'class': 'w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-gray-700'
            })
  


