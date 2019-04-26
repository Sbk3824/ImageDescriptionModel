from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
import json
from .models import Image

import cv2
import sys
import os

from clarifai.rest import ClarifaiApp
from clarifai.rest import Image as ClImage

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

    #Clarifai API Call
    app = ClarifaiApp(api_key='18e645eb7c0f49d594ca9cc0a680a9c5')
    model = app.public_models.general_model
    response = model.predict_by_filename('C:/tensorflow1/ImageDescriptorModel-master/media/opencv_frame_0.png')
    concepts = response['outputs'][0]['data']['concepts']
    print('I am inside Views.py')
    for concept in concepts:
        print(concept['name'], concept['value'])    
    json_string = json.dumps(concepts)
    return render(request, 'dashboard.html', {'concepts_json': json_string})

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

    
    #Clarifai API Call
    app = ClarifaiApp(api_key='18e645eb7c0f49d594ca9cc0a680a9c5')
    
    
    #General Model
    model = app.public_models.general_model
    response = model.predict_by_filename('C:/tensorflow1/ImageDescriptorModel-master/media/opencv_frame_0.png')
    concepts = response['outputs'][0]['data']['concepts']
    for concept in concepts:
        print(concept['name'], concept['value'])    
    json_string = json.dumps(concepts)
    
    #Faces Model
    model1 = app.models.get('face-v1.3')
    #response1 = model1.predict_by_filename('C:/tensorflow1/ImageDescriptorModel-master/media/opencv_frame_0.png')
    response1 = model1.predict_by_url(url='https://premierleague-static-files.s3.amazonaws.com/premierleague/photo/2018/09/25/a87449ac-ca40-4875-a67c-4d2986ba5017/Man-City-fans-celebrate-v-Arsenal-lead.png')
       
    print(response1)
    #item_dict = json.loads(response1)
    numface = len(response1['outputs'][0]['data']['regions'])


    #Color Model
    model2 = app.models.get('color')
    response2 = model2.predict_by_filename('C:/tensorflow1/ImageDescriptorModel-master/media/opencv_frame_0.png')
    #image = ClImage('C:/tensorflow1/ImageDescriptorModel-master/media/opencv_frame_0.png')
    #print(model2.predict([image]))
    print('this is color model perint !!!!!!!!!!!!@@@@@@@@@@@@!!!!!')
    print(response2)

    colorname = response2['outputs'][0]['data']['colors'][0]['w3c']['name']
    print(colorname)


    
    return render(request, 'analysis.html', {'concepts_json': json_string})

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