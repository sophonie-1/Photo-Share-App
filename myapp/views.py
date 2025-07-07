from typing import Any
from django.shortcuts import render,get_list_or_404,get_object_or_404,redirect
from .models import Photo, Category,CommentModel
from .forms import PhotoForm,CommentForm
from django.views import View
from django.views.generic import ListView,DetailView,UpdateView,DeleteView,CreateView
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login



class LoginCustomView(LoginView):
    template_name='registration/login.html'
    redirect_authenticated_user =True

class RegisterView(CreateView):
    form_class =UserCreationForm
    template_name='registration/register.html'
    # success_url=reverse_lazy('login')
    redirect_authenticated_user =True

    def form_valid(self, form):
        user =form.save()
        if user is not None:
            login(self.request,user)
            return redirect('gallery')

        return super().form_valid(form)
    

class GalleryView(LoginRequiredMixin,ListView):
    model=Photo
    template_name='myapp/gallery.html'
    context_object_name='photos'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["categories"] = get_list_or_404(Category)
        context["Allphotos"] = Photo.objects.filter(user=self.request.user).count()
        return context
    
    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            return Photo.objects.all().order_by('-date')
        else:
            # If the user is not authenticated, return an empty queryset or handle as needed
            return Photo.objects.none()
        
        return super().get_queryset()
    
    
    

class DetailImageView(LoginRequiredMixin,DeleteView):
    model=Photo
    context_object_name='photo'
    template_name='myapp/photoview.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comments'] = CommentModel.objects.filter(photo=self.object).order_by('-date')
        context['form'] = CommentForm()
        context['photo'] = self.object
        context['user'] = self.request.user
        context['is_owner'] = self.object.user == self.request.user
        context['can_comment'] = self.request.user.is_authenticated
        return context

class CreateFormView(LoginRequiredMixin,CreateView):
    form_class =PhotoForm
    
    success_url=reverse_lazy('gallery')
    template_name='myapp/form.html'

    def form_valid(self, form):
        photo= form.save(commit=False)
        photo.user = self.request.user
        
        photo.save()
        # form.save_m2m()
        
        return super().form_valid(form)
class PhotoUpdateView(LoginRequiredMixin,UpdateView):
    model=Photo
    template_name='myapp/form.html'
    context_object_name='photo'
    form_class=PhotoForm
    success_url=reverse_lazy('gallery')

class DeleteImageView(LoginRequiredMixin,DeleteView):
    template_name='myapp/delete.html'
    context_object_name='photo'
    model=Photo
    success_url=reverse_lazy('gallery')


class CommentView(LoginRequiredMixin,CreateView):
    model=CommentModel
    form_class=CommentForm
    context_object_name='comments'
    # template_name='myapp/comment.html'
    # def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
    #     context = super().get_context_data(**kwargs)
    #     context['photo'] = get_object_or_404(Photo, pk=self.kwargs['pk'])
    #     context['comments'] = CommentModel.objects.filter(photo=context['photo']).order_by('-date')
    #     return context
    
    def form_valid(self, form: Any) -> Any:
        comment = form.save(commit=False)
        comment.user = self.request.user
        comment.photo = get_object_or_404(Photo, pk=self.kwargs['pk'])
        comment.save()
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy('image', kwargs={'pk': self.kwargs['pk']})


class LikesView(LoginRequiredMixin, View):
    def post(self, request, pk):
        comment = get_object_or_404(CommentModel, pk=pk)
        if request.user == comment.user:
            return redirect('image', pk=comment.photo.pk)
        
        if 'like' in request.POST:
            comment.likes += 1
        elif 'dislike' in request.POST:
            comment.dislikes += 1
        
        comment.save()
        return redirect('image', pk=comment.photo.pk)
    
    