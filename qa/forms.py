from django import forms
from django.db.models import Q
from django.shortcuts import get_object_or_404
from markdownx.widgets import MarkdownxWidget
from markdownx.models import MarkdownxField

from .models import Question, Answer, Reply, Tag


class QuestionSearchForm(forms.Form):
	q = forms.CharField(required=False)


class QuestionCreateForm(forms.ModelForm):
	class Meta:
		model = Question
		fields = ('title', 'tag', 'text', 'is_public')
		widgets = {
			'tag': forms.CheckboxSelectMultiple(
				attrs={'class': 'list-unstyled',}
			),
			'question_text': MarkdownxWidget(
				attrs={'placeholder': 'マークダウンに対応しています。'}
			),
		}


class AnswerCreateForm(forms.ModelForm):
	class Meta:
		model = Answer
		fields = ('text',)
		widgets = {
			'text': forms.Textarea(
				attrs={'placeholder': 'マークダウンに対応しています。'}
			)
		}


class ReplyCreateForm(forms.ModelForm):
	class Meta:
		model = Reply
		fields = ('text',)
		widgets = {
			'text': forms.Textarea(
				attrs={'placeholder': 'マークダウンに対応しています。'}
			)
		}
