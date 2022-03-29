from distutils import extension
from unicodedata import name
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse
from markdown import markdown
import markdown
import re
from django.utils.html import strip_tags
from markdown.extensions.toc import TocExtension
from django.utils.text import slugify
from django.utils.functional import cached_property

def generate_rich_content(value):
		md = markdown.Markdown(
			extensions=[
				"markdown.extensions.extra",
				"markdown.extensions.codehilite",
				TocExtension(slugify=slugify),
			]
		)
		content = md.convert(value)
		m = re.search(r'<div class="toc">\s*<ul>(.*)</ul>\s*</div>', md.toc, re.S)
		toc = m.group(1) if m is not None else ''
		return {"content": content, "toc": toc}

class Category(models.Model):
	'''
	django模型必须继承models.Model类
	分类的表由类Category代表，有一个属性分类名name
	分类名name的数据类型是字符型，用CharField指定，最大长度100
	'''
	name = models.CharField(max_length=100)

	# 定义model的特性，admin后台显示中文
	class Meta:
		verbose_name = '分类'
		verbose_name_plural = verbose_name

	def __str__(self):
		return self.name

class Tag(models.Model):
	'''
	标签的表由类Tag表示，同样要继承models.Model类
	'''
	name = models.CharField(max_length=100)

	# 定义model的特性，admin后台显示中文
	class Meta:
		verbose_name = '标签'
		verbose_name_plural = verbose_name

	def __str__(self):
		return self.name

class Post(models.Model):
	'''
	文章的数据库表由类Post代表
	'''

	# 文章标题
	title = models.CharField('标题', max_length=70)

	# 文章正文使用TextField，存储大段字符串
	body = models.TextField('正文')

	# 文章的创建时间和最后一次修改时间用DateField类型
	created_time = models.DateTimeField('创建时间')
	modified_time = models.DateTimeField('修改时间')

	# 文章摘要用CharField类型，默认不能为空，所以设置blank参数值允许空值
	excerpt = models.CharField('摘要', max_length=200,blank=True)

	# 分类与文章是一对多关系用ForeignKey关联，级联删除
	category = models.ForeignKey(Category,verbose_name='分类',on_delete=models.CASCADE)
	# 标签和文章是多对多关系用ManyToMany代表，允许为空
	tags = models.ManyToManyField(Tag,verbose_name='标签',blank=True)

	# 作者和文章也是一对多关系，和category类似
	# User是django的内置应用django.contrib.auth.models
	author = models.ForeignKey(User,verbose_name='作者',on_delete=models.CASCADE)

	# 创建时间默认为当前时间
	created_time = models.DateTimeField('创建时间', default=timezone.now)

	# 记录阅读量
	views = models.PositiveIntegerField(default=0, editable=False)

	# 统计阅读量模型方法
	def increase_views(self):
		self.views += 1
		self.save(update_fields=['views'])

	# 定义model的特性，admin后台显示中文
	class Meta:
		verbose_name = '文章'
		verbose_name_plural = verbose_name
		ordering = ['-created_time', 'title']

	# model被save到数据库前指定modified_time的值
	def save(self, *args, **kwargs):
		self.modified_time = timezone.now()
		# 实例化一个Markdown类渲染body文本，去掉目录生成摘要
		md = markdown.Markdown(extensions=[
			'markdown.extensions.extra',
			'markdown.extensions.codehilite',
		])
		# Markdown转HTML，去掉文本中的HTML标签
		self.excerpt = strip_tags(md.convert(self.body))[:54]
		super().save(*args, **kwargs)

	def __str__(self):
		return self.title

	# 自定义获取绝对url方法，从django.urls中导入reverse函数
	def get_absolute_url(self):
		return reverse('note:detail',kwargs={'pk': self.pk})

	@property
	def toc(self):
		return self.rich_content.get("toc", "")

	@property
	def body_html(self):
		return self.rich_content.get("content","")

	@cached_property
	def rich_content(self):
		return generate_rich_content(self.body)


