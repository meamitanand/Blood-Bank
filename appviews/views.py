#Imports
from appdata.models import BloodGroupType
from appdata.models import City
from appdata.models import Details
from appdata.models import Facts
from appdata.models import FamousQuotes
from appdata.models import Medication
from appdata.models import NotDonate
from appdata.models import State
from appdata.models import Availability
from django.contrib import auth
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.context_processors import csrf
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from forms import DetailsForm
from forms import UrgentForm
from helper import HelperFunctions
from googlemaps import Client as GoogleMaps
from operator import itemgetter
from collections import OrderedDict
#Captcha API objects
import CaptchasDotNet
import urlparse
import urllib
captchas = CaptchasDotNet.CaptchasDotNet (
                                client   = 'devanshug', 
                                secret   = '6HdMmG1EgKnJEOqHfQ5r9ywhkUbcM42UaeA0ffK1',
                                alphabet = 'abcdefghkmnopqrstuvwxyz0123456789',
                                letters  = 6,
                                width    = 240,
                                height   = 80
                                )
helperfunction = HelperFunctions()

#Data Updates
def dataUpdates(data):
    data['bloodgroupsCount'] = helperfunction.getCount()

#Views
def bloodgroupsystem(request):
    template = 'bloodgroupsystem.html'
    data = {}
    if request.user.is_authenticated():
        data['authenticated'] = request.user.is_authenticated()
        data['username'] = request.user.get_username()
    dataUpdates(data)
    return render_to_response(template, data)

def calculate(request):
    template = 'calculate.html'
    data = {}
    if request.user.is_authenticated():
        data['authenticated'] = request.user.is_authenticated()
        data['username'] = request.user.get_username()
    dataUpdates(data)
    return render_to_response(template, data)

def details(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/')
    template = 'details.html'
    data = {'bloodgroups':BloodGroupType.objects.all(),
            'states':State.objects.all(),
	    'cap_val':captchas.random(),
	    'cap_img':captchas.image(),
	    'cap_id':captchas.get_id(),
            }
    data['authenticated'] = request.user.is_authenticated()
    data['username'] = request.user.get_username()
    data.update(csrf(request))
    dataUpdates(data)
    return render_to_response(template, data)

def exists(request, username):
    if User.objects.filter(username=username).count():
        return HttpResponse('Username Exists')
    return HttpResponse('')

def facts(request):
    template = 'facts.html'
    data = {'facts':Facts.objects.all()}
    if request.user.is_authenticated():
        data['authenticated'] = request.user.is_authenticated()
        data['username'] = request.user.get_username()
    dataUpdates(data)
    return render_to_response(template, data)

def famousquotes(request):
    template = 'famousquotes.html'
    data = {'quotes':FamousQuotes.objects.all()}
    if request.user.is_authenticated():
        data['authenticated'] = request.user.is_authenticated()
        data['username'] = request.user.get_username()
    dataUpdates(data)
    return render_to_response(template, data)

def getData(request, state="Assam"):
    return render_to_response('data.html', {'cities':City.objects.filter(state_name=state)})

def index(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect('/wall')
    template = 'index.html'
    data = {}
    dataUpdates(data)
    data.update(helperfunction.getBloodRequirements(username=None))
    return render_to_response(template, data)

def login(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect('/')
    data = {}
    if request.method=='POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return HttpResponseRedirect('/wall')
        else:
            data['invalid'] = True
    template = 'login.html'
    data.update(csrf(request))
    dataUpdates(data)
    return render_to_response(template, data)

def logout(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/')
    auth.logout(request)
    return HttpResponseRedirect('/')

def qualified(request):
    template = 'qualification.html'
    data = {'no_donation':NotDonate.objects.all(),
            'medications':Medication.objects.all()}
    if request.user.is_authenticated():
        data['authenticated'] = request.user.is_authenticated()
        data['username'] = request.user.get_username()
    dataUpdates(data)
    return render_to_response(template, data)

def register(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect('/')
    if request.method=='POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            form = DetailsForm(request.POST,request.FILES)
            form.save()
            username = request.POST.get('username', '')
            password = request.POST.get('password1', '')
            user = auth.authenticate(username=username, password=password)
            if user is not None:
                auth.login(request, user)
                return HttpResponseRedirect('/wall')
    args = {'bloodgroups':BloodGroupType.objects.all(),
            'states':State.objects.all(),
	    'cap_val':captchas.random(),
	    'cap_img':captchas.image(),
	    'cap_id':captchas.get_id()}
    args.update(csrf(request))
    dataUpdates(args)
    return render_to_response('register.html', args)

def urgent_blood(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/')
    template = 'urgent_blood.html'
    data = {'bloodgroups':BloodGroupType.objects.all(),
            'states':State.objects.all(),
	    'cap_val':captchas.random(),
	    'cap_img':captchas.image(),
	    'cap_id':captchas.get_id()}
    data['authenticated'] = request.user.is_authenticated()
    data['username'] = request.user.get_username()
    data.update(csrf(request))
    dataUpdates(data)
    return render_to_response(template, data)

def verify(request, code="123456"):
	print(code,request)
	#print(captchas.password_length)
	#if not captchas.verify(code): return HttpResponse('Incorrect Captcha!!!')
	return HttpResponse('Verified Human!!!')

def wall(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/')
    data = {}
    if request.method=='POST':
        form = UrgentForm(request.POST)
        #print(form.is_valid())
        if form.is_valid():
            form.save()
            data['saved'] = True
            #p=UrgentBlood.objects.all()
            #print(p)
    template = 'wall.html'
    data['authenticated'] = request.user.is_authenticated()
    data['username'] = request.user.get_username()
    dataUpdates(data)
    data.update(helperfunction.getBloodRequirements(username=data['username']))
    return render_to_response(template, data)

def nearestbloodbank(request):
	template = 'nbb.html'
	data={}	
	s=request.GET.urlencode()
	if(s!=""):

		bloodtype=s[10:s.find('amount')-1]
		amount=s[s.find('amount')+7:s.find('location')-1]
		location=s[s.find('location')+9:s.find('submit')-1]
		if(bloodtype[len(bloodtype)-3:]=="%2B"):
			bloodtype=bloodtype[:len(bloodtype)-3]+"+"
		#print(bloodtype,amount,location)
		endloc,avail=main(location,amount,bloodtype)
		tab=Availability.objects.all()
		location=urllib.unquote(location).decode('utf8')
		print()
		location=location.replace("+","")	
		data={"tab":tab,"loc":location,"bg":bloodtype,"v":endloc,"at":amount,"qt":avail}
		return render_to_response("result.html",data)
	return render_to_response(template,data)




def converttomin(t):
	#print (t)
	t=t.split()
	if t[1]=="mins" or t[1]=="min":
		return int(t[0])
	return int(t[0])*60+int(t[2])
def main(end,qtyy,blood):  
	gmaps = GoogleMaps('AIzaSyBFcX4qpaWNXjHm7FoUm7OUMV11K8-QKdY')
	d=[]
	t=[]
	time=[]
	bldgrp=[]
	bbname=[]
	index=[]
	i=0
	cursor=Availability.objects.all()
	for row in cursor:
   	
		#print ("NAME = ", row[0])
		start=row.location
		dirs=gmaps.directions(start,end) 

		#print(dirs)
		dirs1=dirs[0]
		#d.append(dirs1['legs'][0]['distance']['text'])
		t=dirs1['legs'][0]['duration']['text']
		#t1=t[0]
		#print(t)
		tmin=converttomin(t)
		if blood=="A+":
			qty=row.Apos
		if blood=="A-":
			qty=row.Aneg
		
		if blood=="B+":
			qty=row.Bpos
		if blood=="B-":
			qty=row.Bneg
		
		if blood=="AB+":
			qty=row.ABpos
		if blood=="AB-":
			qty=row.ABneg
		
		if blood=="O+":
			qty=row.Opos
		if blood=="O-":
			qty=row.Oneg
		name=row.location
		time.append(tmin)
		bldgrp.append(qty)
		bbname.append(name)
		index.append(i)
		i+=1
	result=dict(zip(time,bldgrp))
	result1=dict(zip(time,index))
	result3=dict(zip(index,bbname))
	ans=OrderedDict(sorted(result.items(),key=itemgetter(0)))
	ans1=OrderedDict(sorted(result1.items(),key=itemgetter(0)))
	#print (result)
	#print (result1)
	j=0
	qt=0
	for i,v in ans.items():
		if v>=int(qtyy):
			qt=v
			#print (v)
			break
		j+=1
	k=0
	id=-1
	for i,v in ans1.items():
		if k==j:
			#print("Nearest Blood Bank is ","\n",i)
			id=v
			break
		k+=1
	for i,v in result3.items():
		if id==i:
			#print("Nearest Blood Bank is ",v)
			#print("Amount Available : ",qt)
			break
	if id==-1:
		return("",0)
	return (v,qt)
	
	
	
