from django.shortcuts import render, redirect
from django.views import View
from django.core.files.storage import FileSystemStorage

import cv2
from pysimilar import compare
import pytesseract

# from django.shortcuts import render

# Create your views here.

class OverwriteStorage(FileSystemStorage):
    def _save(self, name, content):
        available_name = name
        if self.exists(name):
            available_name = self.get_available_name(name)

        super(OverwriteStorage, self)._save(available_name, content)
        return available_name

def ocr_core(img):
  text = pytesseract.image_to_string(img)
  return text

def get_greyscale(image):
  return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

def remove_noise(image):
  return cv2.medianBlur(image, 5)

def thresholding(image):
  return cv2.threshold(image, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]

class IndexView(View):
  html_file = "home.html"

  def get(self, request, *args, **kwargs):
    return render(request, self.html_file)

class AboutView(View):
  html_file = "about.html"

  def get(self, request, *args, **kwargs):
    return render(request, self.html_file)
  

def remove_non_ascii(text):
    return unidecode(unicode(text, encoding = "utf-8"))

all = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', ' ']
all_caps = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', ' ']

def upload(request):
  
  context = {}

  if (request.method == 'POST'):
    file1 = request.FILES['fa']
    file2 = request.FILES['fb']

    fs = OverwriteStorage()

    file1.name = fs._save(file1.name, file1)
    file2.name = fs._save(file2.name, file2)

    file1_img = cv2.imread(f'./media/{file1.name}')
    file2_img = cv2.imread(f'./media/{file2.name}')

    # file1_img = get_greyscale(file1_img)
#    file1_img = thresholding(file1_img)
    # file1_img = remove_noise(file1_img)

    # file2_img = get_greyscale(file2_img)
#     file2_img = thresholding(file2_img)
    # file2_img = remove_noise(file2_img)

    text_file1 = ocr_core(file1_img)
    text_file2 = ocr_core(file2_img)

    t1 = ""
    t2 = ""

    for c in text_file1:
      if c in all or c in all_caps:
        t1 += c

    for c in text_file2:
      if c in all or c in all_caps:
        t2 += c

    res = compare(t1, t2)

    res *= 100.0
    if (res > 100.0):
      res = 100.0

    context['percent'] = str(round(res, 2))
    res2 = 100.0 - res
    context['percent2'] = str(round(res2, 2))
    context['file1'] = t1
    context['file2'] = t2

  return render(request, "result.html", context)

class ToolsView(View):
  html_file = "tools.html"

  def get(self, request, *args, **kwargs):
    return render(request, self.html_file)  

def tools_upload(request):
  
  context = {}

  if (request.method == 'POST'):
    file1 = request.FILES['fa']

    fs = OverwriteStorage()

    file1.name = fs._save(file1.name, file1)

    file1_img = cv2.imread(f'./media/{file1.name}')

    # file1_img = get_greyscale(file1_img)
#    file1_img = thresholding(file1_img)
    # file1_img = remove_noise(file1_img)

    # file2_img = get_greyscale(file2_img)
#     file2_img = thresholding(file2_img)
    # file2_img = remove_noise(file2_img)

    text_file1 = ocr_core(file1_img)

    t1 = ""

    for c in text_file1:
      if c in all or c in all_caps:
        t1 += c

    context['file1'] = t1

  return render(request, "tools_result.html", context)
