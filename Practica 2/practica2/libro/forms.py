from  django.forms import ModelForm,EmailInput
from libro.models import Libro

class Libroform(ModelForm):
    class Meta:
        model = Libro
        fields = "_all_"
        widgets={
            'email':EmailInput(
                attrs ={
                    'type': 'email',
                    'class': 'form-control',
                    'style': 'max-width:100px',
                    'placeholder':'Correo'
                }
            )
        }