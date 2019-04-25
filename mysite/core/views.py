from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse

from .models import Image

import cv2
import sys
import os

from clarifai.rest import ClarifaiApp


def home(request):
    count = User.objects.count()
    return render(request, 'home.html', {
        'count': count
    })


def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {
        'form': form
    })

@login_required
def profile(request):
    return render(request, 'profile.html')

@login_required
def dashboard(request):

    
    app = ClarifaiApp(api_key='18e645eb7c0f49d594ca9cc0a680a9c5')
    model = app.public_models.general_model
    response = model.predict_by_filename('C:/tensorflow1/ImageDescriptorModel-master/opencv_frame_0.png')
    concepts = response['outputs'][0]['data']['concepts']
    for concept in concepts:
        print(concept['name'], concept['value'])    

    return render(request, 'dashboard.html')

@login_required
def test(request):
    os.system('python C:/tensorflow1/ImageDescriptorModel-master/mysite/core/Object_detection_webcam.py')

    img = Image()
    img.image ="C:/tensorflow1/ImageDescriptorModel-master/opencv_frame_0.png"
    img.save()
    print(img)
    all = Image.objects.all().values()
    print(all)
    pic = Image.objects.all().order_by('-id')
    return render(request, 'test.html', {"img":pic})

def faq(request):

    return render(request, 'faq.html')



class analysis(LoginRequiredMixin, TemplateView):
    template_name = 'analysis.html'
"""
def show_webcam(mirror=False):
        cam = cv2.VideoCapture(0)
        while True:
            ret_val, img = cam.read()
            if mirror: 
                img = cv2.flip(img, 1)
            cv2.imshow('my webcam', img)
            if cv2.waitKey(1) == 27: 
                break  # esc to quit
        cv2.destroyAllWindows()

show_webcam(mirror=True)
"""