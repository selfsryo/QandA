from django.urls import path, include

from . import views


app_name = 'qa'

urlpatterns = [
    path('', views.QuestionIndexView.as_view(), name='question_list'),
	path('question/create/', views.QuestionCreateView.as_view(), name='question_create'),
	path('question/detail/<int:pk>/', views.QuestionDetailView.as_view(), name='question_detail'),
	path('question/update/<int:pk>/', views.QuestionUpdateView.as_view(), name='question_update'),
	path('question/delete/<int:pk>/', views.QuestionDeleteView.as_view(), name='question_delete'),
    path('question/select_best/<int:pk>/', views.BestAnswerUpdate.as_view(), name='best_answer'),
    path('tag/', views.TagIndexView.as_view(), name='tag_list'),
	path('answer/create/<int:pk>/', views.AnswerCreateView.as_view(), name='answer_create'),
	path('answer/delete/<int:pk>/', views.AnswerDeleteView.as_view(), name='answer_delete'),
	path('reply/create/<int:pk>/', views.ReplyCreateView.as_view(), name='reply_create'),
	path('reply/delete/<int:pk>/', views.ReplyDeleteView.as_view(), name='reply_delete'),
]
