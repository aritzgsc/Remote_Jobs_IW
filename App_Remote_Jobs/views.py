from django.shortcuts import render

def inicio(request):
    return render(request, "App_Remote_Jobs/inicio.html")
