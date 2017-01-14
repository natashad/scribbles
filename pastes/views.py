import secrets

from django.shortcuts import render, get_object_or_404
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.utils import timezone

from .models import Paste

def index(request):
    context = {}
    return render(request, 'pastes/index.html', context)

def save(request):
    token = secrets.token_urlsafe(20)
    while Paste.objects.filter(token=token).exists():
        token = secrets.token_urlsafe(20)

    posted_content = request.POST['content']
    p = Paste(content=posted_content, pub_date=timezone.now(), is_private=True, token=token)
    p.save()

    return HttpResponseRedirect('show/' + token)

def show(request, token):     
    paste = get_object_or_404(Paste, pk=token)
    context = {'paste': paste}
    return render(request, 'pastes/show.html', context)        