from django.shortcuts import render, redirect
from django.views import View
from django.core.files.storage import FileSystemStorage

# from django.shortcuts import render

# Create your views here.

class OverwriteStorage(FileSystemStorage):
    def _save(self, name, content):
        available_name = name
        if self.exists(name):
            available_name = self.get_available_name(name)

        super(OverwriteStorage, self)._save(available_name, content)
        return available_name

class IndexView(View):
  html_file = "home.html"

  def get(self, request, *args, **kwargs):
    return render(request, self.html_file)

def upload(request):
  if (request.method == 'POST'):
    file1 = request.FILES['fa']
    file2 = request.FILES['fb']

    fs = OverwriteStorage()

    file1.name = fs._save(file1.name, file1)
    file2.name = fs._save(file2.name, file1)

  return render(request, "home.html")
