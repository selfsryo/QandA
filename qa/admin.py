from django.contrib import admin
from markdownx.admin import MarkdownxModelAdmin

from .models import Question, Answer, Tag, Reply


class QuestionAdmin(MarkdownxModelAdmin):
	list_display = ('title', 'get_tag', 'author', 'created_at', 'is_public')
	list_display_links = list_display
	ordering = ('-created_at',)
	
	def get_tag(self, row):
		return ','.join([x.name for x in row.tag.all()])


class AnswerAdmin(MarkdownxModelAdmin):
	list_display = ('question', 'author', 'is_best', 'created_at')
	list_display_links = list_display


class ReplyAdmin(admin.ModelAdmin):
	list_display = ('id', 'answer', 'author')


class TagAdmin(admin.ModelAdmin):
	list_display = ('id', 'name')


admin.site.register(Question, QuestionAdmin)
admin.site.register(Answer, AnswerAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Reply, ReplyAdmin)
