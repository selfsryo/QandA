from django.conf import settings
from django.contrib.auth import authenticate, get_user_model, login, views as auth_views
from django.shortcuts import render
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views import generic
from django.views.generic.list import MultipleObjectMixin
from django.shortcuts import get_object_or_404, redirect

from .forms import CustomUserCreationForm
from .mixins import OnlyYouMixin, LoginAndOtherRequiredMixin

UserModel = get_user_model()


class UserDetailView(generic.DetailView, MultipleObjectMixin):
    model = UserModel
    paginate_by = settings.PAGE_SIZE
    template_name = 'users/user_detail.html'

    def get_object(self):
        return get_object_or_404(UserModel, username=self.kwargs['username'])

    def get_context_data(self, **kwargs):
        obj_user = self.get_object()
        visitor = self.request.user
        question_list = obj_user.question_set.public()
        # 自分自身の質問も取得
        if visitor == obj_user:
            question_list = question_list | obj_user.question_set.private(self.request)

        context = super().get_context_data(object_list=question_list, **kwargs)
        context['question_list'] = context['page_obj']

        # フォローできるかどうか
        context['can_follow'] = visitor != obj_user
        return context


class UserSignUpView(generic.CreateView):
    form_class = CustomUserCreationForm
    template_name = 'users/user_signup.html'

    def form_valid(self, form):
        form.save()
        input_email = form.cleaned_data['email']
        input_password = form.cleaned_data['password1']
        new_user = authenticate(email=input_email, password=input_password)
        if new_user is not None:
            login(self.request, new_user)
            return redirect('users:user_detail', username=new_user.username)	


class UserUpdateView(OnlyYouMixin, generic.UpdateView):
    fields = ('username', 'email', 'thumbnail')
    template_name = 'users/user_update.html'

    def get_success_url(self):
        return reverse_lazy('users:user_detail', kwargs={'username': self.request.user.username})

    def get_object(self):
        return self.request.user


class UserFollow(LoginAndOtherRequiredMixin, generic.View):
    def get_object(self):
        return get_object_or_404(UserModel, username=self.kwargs['username'])

    def post(self, request, **kwargs):
        followee = self.get_object()
        visitor = self.request.user
        if followee in visitor.followees.all():
            visitor.unfollow(followee)
        else:
            visitor.follow(followee)
        visitor.save()
        return redirect('users:user_detail', username=followee.username)


class UserPasswordChangeView(auth_views.PasswordChangeView):
    template_name='users/password_change.html'
    success_url=reverse_lazy('users:password_change_done')


class UserPasswordResetView(auth_views.PasswordResetView):
    template_name='users/password_reset.html'
    email_template_name='users/password_reset_email.html'
    subject_template_name='users/password_reset_subject.txt'
    success_url=reverse_lazy('users:password_reset_done')


class UserPasswordResetConfirmView(auth_views.PasswordResetConfirmView):
    template_name='users/password_reset_confirm.html'
    post_reset_login = True
    post_reset_login_backend = 'django.contrib.auth.backends.ModelBackend'
    success_url=reverse_lazy('users:password_reset_complete')

