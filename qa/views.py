from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.core.exceptions import PermissionDenied
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy, reverse
from django.utils.http import urlencode
from django.views import generic

from .forms import QuestionSearchForm, QuestionCreateForm, AnswerCreateForm, ReplyCreateForm
from .mixins import AuthorRequiredMixin, PublicOrAuthorRequiredMixin
from .models import Question, Answer, Reply, Tag


class QuestionIndexView(generic.ListView):
    model = Question
    paginate_by = settings.PAGE_SIZE

    def get_queryset(self):
        question_list = Question.objects.public()

        if self.request.user.is_authenticated:
            question_list = question_list | Question.objects.private(self.request)

        self.form = QuestionSearchForm(self.request.GET or None)
        if self.form.is_valid():
            query =  self.form.cleaned_data.get('q')
            question_list = question_list.search(query)

        if self.request.GET.get('tag'):
            self.tag = Tag.objects.get(name=self.request.GET.get('tag'))
            question_list = question_list.filter(tag=self.tag)
        return question_list

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_form'] = self.form

        if self.request.GET.get('tag'):
            context['tag'] = self.tag
        return context


class QuestionDetailView(PublicOrAuthorRequiredMixin, generic.DetailView):
    model = Question

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        question = self.get_object()
        context['answer_list'] = question.answer_set.get_not_best()
        context['best_answer'] = question.best_answer
        return context


class QuestionCreateView(LoginRequiredMixin, generic.CreateView):
    model = Question
    form_class = QuestionCreateForm

    def form_valid(self, form):
        question = form.save(commit=False)
        question.author = self.request.user
        question.save()
        form.save_m2m()
        return redirect('qa:question_detail', pk=question.pk)	


class QuestionUpdateView(AuthorRequiredMixin, generic.UpdateView):
    form_class = QuestionCreateForm

    def get_success_url(self):
        return reverse('qa:question_detail', kwargs={'pk': self.kwargs['pk']})

    def get_object(self):
        return get_object_or_404(Question, pk=self.kwargs['pk'])


class QuestionDeleteView(AuthorRequiredMixin, generic.DeleteView):
    model = Question
    success_url = reverse_lazy('qa:question_list')


class TagIndexView(generic.ListView):
    model = Tag


class AnswerCreateView(LoginRequiredMixin, generic.CreateView):
    model = Answer
    form_class = AnswerCreateForm

    def form_valid(self, form):
        question = self.get_object()
        answer = form.save(commit=False)
        answer.question = question
        answer.author = self.request.user
        answer.save()

        question.update_status()
        return redirect('qa:question_detail', pk=question.pk)	

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['question'] = self.get_object()
        return context

    def get_object(self):
        return get_object_or_404(Question, pk=self.kwargs['pk'])


class AnswerDeleteView(AuthorRequiredMixin, generic.DeleteView):
    model = Answer

    def delete(self, *args, **kwargs):
        answer = self.get_object()
        answer.delete()
        answer.question.update_status()
        return redirect('qa:question_detail', pk=answer.question.pk)	

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['question'] = self.get_object().question
        return context


class ReplyCreateView(LoginRequiredMixin, generic.CreateView):
    model = Reply
    form_class = ReplyCreateForm

    def form_valid(self, form):
        answer = self.get_object()
        reply = form.save(commit=False)
        reply.answer = answer
        reply.author = self.request.user
        reply.save()
        return redirect('qa:question_detail', pk=answer.question.pk)	

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['answer'] = self.get_object()
        context['question'] = context['answer'].question
        return context

    # def get_object(self):
    #     return get_object_or_404(Answer, pk=self.kwargs['answer_pk'])


class ReplyDeleteView(AuthorRequiredMixin, generic.DeleteView):
    model = Reply

    def delete(self, *args, **kwargs):
        reply = self.get_object()
        reply.delete()
        return redirect('qa:question_detail', pk=reply.answer.question.pk)	

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['answer'] = self.get_object().answer
        context['question'] = context['answer'].question
        return context

    # def get_object(self):
    #     return get_object_or_404(Reply, pk=self.kwargs['pk'])



class BestAnswerUpdate(AuthorRequiredMixin, generic.View):

    def post(self, request, *args, **kwargs):
        question = self.get_object()
        answer = get_object_or_404(Answer, pk=self.kwargs['pk'])

        if question.best_answer:
            question.leave_best()
        if request.POST.get('is_best') == 'true':
            question.sellect_best(answer)

        question.update_status()
        return redirect('qa:question_detail', pk=question.pk)

    def get_object(self):
        answer = get_object_or_404(Answer, pk=self.kwargs['pk'])
        return answer.question
