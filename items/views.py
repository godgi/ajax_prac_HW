from django.shortcuts import render,redirect,get_object_or_404
from .models import *
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST # POST 형식의 Http 통신만 받기 위해 사용
from django.http import HttpResponse #response를 반환하는 가장 기본 함수, html 파일, 이미지 등 다양한 응답을 함
import json #딕셔너리를 json 형식으로 바꾸기 위해 사용


def main(request):
    items = Post.objects.all()
    return render(request, 'items/home.html', {'items':items})

def new(request):
    return render(request, 'items/new.html')

def create(request):
    if request.method=="POST":
        title = request.POST.get('title')
        content = request.POST.get('content')
        image = request.FILES.get('image')
        user = request.user
        Post.objects.create(title=title, content=content, image=image,user=user)
    return redirect('main')

def show(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    post.view_count = post.view_count+1
    post.save()
    return render(request, 'items/show.html', {'post':post})


#삭제하기
def delete(request,post_id):
    post = get_object_or_404(Post, pk=post_id)
    post.delete()
    return redirect('main')


@require_POST
@login_required
def like_toggle(request, post_id):

    post=get_object_or_404(Post, pk=post_id)
    post_like, post_like_created = Like.objects.get_or_create(user=request.user, post=post)

    if not post_like_created:
        post_like.delete()
        result = "like_cancel"
    else:
        result = "like"

    context = {
        "like_count" : post.like_count,
        "result": result
    }

    return HttpResponse(json.dumps(context),content_type="application/json") #json.dumps = json 형식으로 바꾸겠다.
    
@login_required
@require_POST
def dislike_toggle(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    post_dislike, post_dislike_created = Dislike.objects.get_or_create(user=request.user, post=post)

    if not post_dislike_created:
        post_dislike.delete()
        result = "dislike_cancel"
    else:
        result = "dislike"
    
    context = {
        "dislike_count":post.dislike_count,
        "result":result
    }

    return HttpResponse(json.dumps(context), content_type="application/json")
