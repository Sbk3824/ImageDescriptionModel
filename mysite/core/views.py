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
import operator

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
    users = User.objects.all()
    return render(request, 'profile.html', {'users': users})

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

    """
    img = Image()
    img.image ="C:/tensorflow1/ImageDescriptorModel-master/opencv_frame_0.png"
    img.save()
    print(img)
    all = Image.objects.all().values()
    #print(all)
    pic = Image.objects.all().order_by('-id')
    """
    
    #Clarifai API Call
    app = ClarifaiApp(api_key='18e645eb7c0f49d594ca9cc0a680a9c5')
    
    dict_main = {}
    
    #General Model
    model = app.public_models.general_model
    response = model.predict_by_filename('C:/tensorflow1/ImageDescriptorModel-master/media/opencv_frame_0.png')
    concepts = response['outputs'][0]['data']['concepts']
    dict_main = {'c1' : concepts[0]['name'], 'c2': concepts[1]['name'], 'c3' : concepts[2]['name']}
    
    for concept in concepts:
        print(concept['name'], concept['value'])    
    json_string = {'test':  json.dumps(concepts)}
    print()
    print()



    #Faces Model
    model1 = app.models.get('face-v1.3')
    response1 = model1.predict_by_filename('C:/tensorflow1/ImageDescriptorModel-master/media/opencv_frame_0.png')
    #response1 = model1.predict_by_url(url='https://premierleague-static-files.s3.amazonaws.com/premierleague/photo/2018/09/25/a87449ac-ca40-4875-a67c-4d2986ba5017/Man-City-fans-celebrate-v-Arsenal-lead.png')
    print('THIS IS THE FACE MODEL\n\n! {}'.format(response1))
    #item_dict = json.loads(response1)          
    print()
    print()
    if 'regions' in response1['outputs'][0]['data']:
        numface = len(response1['outputs'][0]['data']['regions']) 
    else:
        numface = 'None'
    print(numface)
    
    face_dict = {'numface' : numface}
    print(face_dict)
    json_facestring = json.dumps(face_dict)
    print()
    print()

    dict_main['numface'] = numface
    print('\n Dictioanry\n')
    print(dict_main)

    #Color Model
    model2 = app.models.get('color')
    response2 = model2.predict_by_filename('C:/tensorflow1/ImageDescriptorModel-master/media/opencv_frame_0.png')
    #image = ClImage('C:/tensorflow1/ImageDescriptorModel-master/media/opencv_frame_0.png')
    #print(model2.predict([image]))
    print('this is color model print !!!!!!!!   !!!!     @@@@@@ @  @ @   @@@   !!!!!')
    #print(response2)
    color_dict = response2['outputs'][0]['data']
    print('\n\n\n\n\n this is the colour dictionary')
    #print(color_dict)
    colorname = []
    colorvalue = []
    x = len(color_dict['colors'])
    print(x)
    i = 0
    while(i<x):
        name = color_dict['colors'][i]['w3c']['name']
        value = color_dict['colors'][i]['value']
        
        colorname.append(name)
        colorvalue.append(value)
        i += 1
    
    colordata_dict = dict(zip(colorname,colorvalue))    
    print(colordata_dict)
    print()
    print()
    sorted_color_dict = sorted(colordata_dict.items(), key = operator.itemgetter(1))
    sorted_color_dict.reverse()
    print(sorted_color_dict[0][0])
    #print(sorted_color_dict.keys())
  
    dict_main['color1'] = sorted_color_dict[0][0]
    dict_main['color2'] = sorted_color_dict[1][0]
    dict_main['color3'] = sorted_color_dict[2][0]



    #Demographics API
    
    model3 = app.models.get('demographics')
    response3 = model3.predict_by_filename('C:/tensorflow1/ImageDescriptorModel-master/media/opencv_frame_0.png')
    
    if 'regions' in response1['outputs'][0]['data']:

        age = response3['outputs'][0]['data']['regions'][0]['data']['face']['age_appearance']['concepts'][0]['name']
        print('The Age is ,,,,,......')
        print(age)

        gender = response3['outputs'][0]['data']['regions'][0]['data']['face']['gender_appearance']['concepts'][0]['name']
        print(gender)

        ethnicity = response3['outputs'][0]['data']['regions'][0]['data']['face']['multicultural_appearance']['concepts'][0]['name']
        print(ethnicity)
        print("This is demographics response")
    
        dict_main['age'] = age
        dict_main['ethnicity'] = ethnicity
        if(gender == 'masculine'):
            dict_main['gender'] = 'Male'
        else:
            dict_main['gender'] = 'Female'
    else:
        dict_main['age'] = 'undetectable'
        dict_main['ethnicity'] = 'of multiple ethnic backgrounds'
        dict_main['gender'] = 'unresolvable'
            
    print()
    print()
    print(dict_main)
    return render(request, 'analysis.html', {'dict_main': dict_main})

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