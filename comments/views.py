import imp
from multiprocessing import context
from django.shortcuts import render, get_object_or_404, redirect
from note.models import Post
from django.views.decorators.http import require_POST
from .forms import CommentForm
from django.contrib import messages

# Create your views here.

@require_POST
def comment(request, post_pk):
    # 要将评论和被评论的文章关联，先获取被评论的文章
    # 获取文章Post存在时，则获取，否则返回404
    post = get_object_or_404(Post, pk=post_pk)

    # 将用户提交数据封装在request.POST中，这是一个类字典对象
    # 利用这些数据构造CommentForm实例，生成了一个绑定用户提交数据的表单
    form = CommentForm(request.POST)

    # django自动检查表单数据是否符合格式要求
    if form.is_valid():
        # 若数据合法，调用表单save方法保存到数据库
        
        # 利用表单的数据生成Comment模型类的实例
        comment = form.save(commit=False)

        # 评论和被评论的文章关联起来
        comment.post = post

        # 将评论数据保存金数据库
        comment.save()

        messages.add_message(request, messages.SUCCESS, '评论发表成功！', extra_tags='success')

        # 重定向到post详情页
        return redirect(post)


    context = {
        'post': post,
        'form': form,
    }
    messages.add_message(request, messages.ERROR, '评论发表失败！请修改表单中的错误后重新提交。', extra_tags='danger')
    return render(request, 'comments/preview.html', context=context)
