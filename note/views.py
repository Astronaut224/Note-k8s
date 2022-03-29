from calendar import month
from multiprocessing import context
from pyexpat import model
import re
from unicodedata import category
from urllib import response
import markdown
from markdown.extensions.toc import TocExtension
from django.utils.text import slugify
from django.shortcuts import render, get_object_or_404, redirect
from .models import Post, Category, Tag
from django.views.generic import ListView, DetailView
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from pure_pagination.mixins import PaginationMixin
from django.contrib import messages
from django.db.models import Q


# Create your views here.

def search(request):
    q = request.GET.get('q')

    if not q:
        error_msg = "请输入搜索关键词"
        messages.add_message(request, messages.ERROR, error_msg, extra_tags='danger')
        return redirect('note:index')

    post_list = Post.objects.filter(Q(title__icontains=q) | Q(body__icontains=q))
    return render(request, 'note/index.html', {'post_list': post_list})

class IndexView(PaginationMixin, ListView):
	model = Post
	template_name = 'note/index.html'
	context_object_name = 'post_list'
	# 指定paginate_by 属性后开启分页功能，参数值代表每页多少篇文章
	paginate_by = 10

# def index(request):
# 	post_list = Post.objects.all().order_by('-created_time')
# 	return render(request,'note/index.html',context={
# 		'post_list': post_list
# 		})

class PostDetailView(DetailView):
	model = Post
	template_name = 'note/detail.html'
	context_object_name = 'post'
	def get(self, request, *args, **kwargs):
		# 父类的get方法被调用后才有self.object属性，其值是Post模型实例（文章post）
		# 覆写get方法是因为文章阅读量增加需要self.object属性
		response = super(PostDetailView, self).get(request, *args, **kwargs)
		# 文章阅读量+1
		self.object.increase_views()
		return response
	
	# def get_object(self, queryset=None):
	# 	post = super().get_object(queryset=None)
	# 	md = markdown.Markdown(extensions=[
	# 	'markdown.extensions.extra',
	# 	'markdown.extensions.codehilite',
	# 	TocExtension(slugify=slugify),
	# ])
	# 	post.body = md.convert(post.body)
	# 	m = re.search(r'<div class="toc">\s*<ul>(.*)</ul>\s*</div>', md.toc, re.S)
	# 	post.toc = m.group(1) if m is not None else ''
	# 	return post

# def detail(request,pk):
# 	post = get_object_or_404(Post, pk=pk)

# 	# 阅读量+1
# 	post.increase_views()

# 	md = markdown.Markdown(extensions=[
# 		'markdown.extensions.extra',
# 		'markdown.extensions.codehilite',
# 		TocExtension(slugify=slugify),
# 	])
# 	post.body = md.convert(post.body)
# 	m = re.search(r'<div class="toc">\s*<ul>(.*)</ul>\s*</div>', md.toc, re.S)
# 	post.toc = m.group(1) if m is not None else ''
# 	return render(request, 'note/detail.html', context={'post':post})

class ArchiveView(IndexView):
	def get_queryset(self):
		return super(ArchiveView, self).get_queryset().filter(
			created_time__year=self.kwargs.get('year'),
 			created_time__month=self.kwargs.get('month')
		)

# def archive(request, year, month):
# 	post_list = Post.objects.filter(
# 		created_time__year=year,
# 		created_time__month=month
# 	).order_by('-created_time')
# 	return render(request, 'note/index.html',context={'post_list': post_list})

class CategoryView(IndexView):
	def get_queryset(self):
		cate = get_object_or_404(Category, pk=self.kwargs.get('pk'))
		return super(CategoryView, self).get_queryset().filter(category=cate)

# def category(request, pk):
# 	cate = get_object_or_404(Category, pk=pk)
# 	post_list = Post.objects.filter(category=cate).order_by('-created_time')
# 	return render(request, 'note/index.html', context={'post_list': post_list})

class TagView(IndexView):
	def get_queryset(self):
		t = get_object_or_404(Tag, pk=self.kwargs.get('pk'))
		return super(TagView, self).get_queryset().filter(tags=t)

# def tag(request, pk):
#     t = get_object_or_404(Tag, pk=pk)
#     post_list = Post.objects.filter(tags=t).order_by('-created_time')
#     return render(request, 'note/index.html', context={'post_list': post_list})