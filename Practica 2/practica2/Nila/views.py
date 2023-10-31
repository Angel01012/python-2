from django.shortcuts import render
from libro.models import Libro,Cliente,Autor

# Create your views here.
def index(request):
    return render(request, 'bienvenido.html')


def indexLibro(request):
    libros = Libro.objects.order_by('id')
    autores  = Autor.objects.order_by('id')
    clientes = Cliente.objects.order_by('id')
    return render(request,'indexLibro.html', {"libros": libros,"autores":autores,"clientes":clientes})
