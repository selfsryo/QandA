from django.db import models
from django.db.models import Q
from django.core.paginator import Paginator

from markdownx.models import MarkdownxField


class Tag(models.Model):
    name = models.CharField("タグ", max_length=255)

    def __str__(self):
        return self.name


class QuestionQuerySet(models.QuerySet):

    def public(self):
        return self.filter(is_public=True)

    def private(self, request):
        return self.filter(author=request.user)

    def search(self, query):
        if query:
            for q in query.split():
                self = self.filter(Q(title__icontains=q) | Q(text__icontains=q))	
        return self


class QuestionManager(models.Manager):

    def get_queryset(self):
        return QuestionQuerySet(self.model, using=self._db).select_related('author').prefetch_related('tag')

    def public(self):
        return self.get_queryset().public()

    def private(self, request):
        return self.get_queryset().private(request)

    def search(self, query):
        return self.get_queryset().search(query)


class Question(models.Model):
    title = models.CharField("タイトル", max_length=255)
    tag = models.ManyToManyField(
        Tag,
        verbose_name="タグ",
        blank=True
    )
    text = MarkdownxField("質問の本文")
    author = models.ForeignKey(
        "users.User", 
        on_delete=models.CASCADE, 
        verbose_name="質問者"
    )
    created_at = models.DateTimeField("質問した日時", auto_now_add=True)
    is_public = models.BooleanField("公開する", default=True)
    best_answer = models.OneToOneField("Answer", 
        on_delete=models.SET_NULL, 
        null= True, 
        blank=True,
        verbose_name="ベストアンサー",
        related_name="question_best_answer")

    class Status(models.TextChoices):
        ACTIVE = "active", "アクティブ"
        NOT_ANSWERED = "not_answered", "未回答"
        ACCEPTED = "accepted", "解決済み"
        
    status = models.CharField("ステータス", 
        max_length=12, 
        choices=Status.choices, 
        default=Status.NOT_ANSWERED)

    objects = QuestionManager()

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    def leave_best(self):
        if self.best_answer:
            self.best_answer.is_best = False
            self.best_answer.save()
            self.best_answer = None

    def sellect_best(self, answer):
        answer.is_best = True
        answer.save()
        self.best_answer = answer

    def update_status(self):
        if self.best_answer:
            self.status = self.Status.ACCEPTED
        else:
            self.status = self.Status.ACTIVE if self.answer_set.all() else self.Status.NOT_ANSWERED
        self.save()


class AnswerManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().select_related('author', 'question')
    
    def get_not_best(self):
        return self.get_queryset().exclude(is_best=True)


class Answer(models.Model):
    text = MarkdownxField("回答の本文")
    question = models.ForeignKey(
        Question, 
        on_delete=models.CASCADE, 
        verbose_name="対象の質問"
    )
    author = models.ForeignKey(
        "users.User", 
        on_delete=models.CASCADE, 
        verbose_name="回答者"
    )
    is_best = models.BooleanField("ベストアンサー", default=False)
    created_at = models.DateTimeField("回答した日時", auto_now=True)

    objects = AnswerManager()

    class Meta:
        ordering = ['-created_at']


class ReplyManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().select_related('author', 'answer')


class Reply(models.Model):
    text = MarkdownxField("回答への返答")
    answer = models.ForeignKey(
        Answer, 
        on_delete=models.CASCADE, 
        verbose_name="対象の回答"
    )
    author = models.ForeignKey(
        "users.User", 
        on_delete=models.CASCADE, 
        verbose_name="返答者"
    )
    created_at = models.DateTimeField("返答した日時", auto_now=True)

    class Meta:
        ordering = ['-created_at']
