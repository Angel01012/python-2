from django.shortcuts import render,redirect,get_object_or_404,HttpResponse
from libro.models import Libro
from libro.forms import Libroform

#agregar
def NuevaPersona(request):
    if request.method=="POST":
        FormaPersona = Libroform(request.POST)
        if FormaPersona.is_valid():
            FormaPersona.save()
            return redirect("listadoPersonas")
    else:
        FormaPersona = Libroform()
    return render(request, "nuevo.html",{'formaPersona': FormaPersona})
#editar
def editarPersona(request,id):
    persona = get_object_or_404(Libro,pk=id)
    if request.method =='POST':
        formaPersona = Libroform(request.POST, instance=persona)
        if formaPersona.is_valid():
            formaPersona.save()
            return redirect("listadoPersonas")
    else:
        formaPersona = Libroform(instance=persona)
        return render(request,"editarPersona.html",{"formaPersona": formaPersona})

def eliminarPersona(request,id):
    persona = get_object_or_404(Libro,pk=id)
    if persona:
        persona.delete()
    return redirect("listadoPersonas")


def detallePersona(request, id):
    persona = get_object_or_404(Libro,pk=id)
    return render(request, "detallePersona.html", {"persona": persona})