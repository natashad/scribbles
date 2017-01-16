import bcrypt
import uuid

from django.shortcuts import render, get_object_or_404
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.utils import timezone

from .models import Paste

def index(request):
    context = {}
    return render(request, 'pastes/index.html', context)

def save(request):
    uid = uuid.uuid4()
    token = uid.hex
    while Paste.objects.filter(token=token).exists():
        uid = uuid.uuid4()
        token = uid.hex

    posted_content = request.POST['content']

    is_private = False
    if 'isPrivate' in request.POST:
        is_private = True

    password = request.POST['pwd']
    hashed = ""
    if len(password) > 0:
        hashed = bcrypt.hashpw(password, bcrypt.gensalt())

    p = Paste(content=posted_content, pub_date=timezone.now(), 
        is_private=is_private, token=token, password=hashed)
    p.save()

    return HttpResponseRedirect('show/' + token)

def show(request, token, authFailure=False):     
    paste = get_object_or_404(Paste, pk=token)

    if len(paste.password) > 0:
        context = {'token': token, 'authFailure': authFailure}
        return render(request, 'pastes/password_protected.html', context)
    
    return show_without_password_check(request, paste)

def show_without_password_check(request, paste):
    context = {'paste': paste}    
    return render(request, 'pastes/show.html', context)

def authenticate(request):
    password = request.POST['pwd']
    token = request.POST['token']

    paste = Paste.objects.get(pk=token)

    if bcrypt.hashpw(password, paste.password) == paste.password:
        return show_without_password_check(request, paste)

    return show(request, token, authFailure=True)



