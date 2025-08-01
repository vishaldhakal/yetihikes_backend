from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Post, Tag, Category
from .serializers import PostSerializer, PostSmallSerializer, TagSerializer, CategorySerializer, TagSmallSerializer, CategorySmallSerializer, PostSlugSerializer, LandingPagePostSerializer
from bs4 import BeautifulSoup


@api_view(['GET'])
def post_list(request):
    if request.method == 'GET':
        posts = Post.objects.all()
        serializer = LandingPagePostSerializer(posts, many=True)
        return Response({
            "posts": serializer.data,

        })


@api_view(['GET'])
def post_list_slug(request):
    if request.method == 'GET':
        posts = Post.objects.only('slug')
        serializer = PostSlugSerializer(posts, many=True)
        return Response(serializer.data)


@api_view(['GET'])
def post_single(request, slug):
    if request.method == 'GET':
        posts = Post.objects.get(slug=slug)
        html_string = posts.blog_content
        soup = BeautifulSoup(html_string, 'html.parser')
        toc_div = soup.find('div', class_='mce-toc')
        if toc_div is not None:
            toc_div.extract()
        updated_html_string = str(toc_div)
        serializer = PostSerializer(posts)
        return Response({
            "data": serializer.data,
            "toc": updated_html_string,
        })


@api_view(['GET'])
def recent_posts(request):
    if request.method == 'GET':
        posts = Post.objects.all()[:5]
        posts_serializer = LandingPagePostSerializer(posts, many=True)
        return Response({
            "recent_posts": posts_serializer.data,
        })
