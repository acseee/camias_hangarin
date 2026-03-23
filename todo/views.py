from django.shortcuts import render, redirect
from django.views.generic import ListView, TemplateView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.db.models import Q
from django.utils import timezone
from .models import Task, Category, Priority
from django.contrib.auth.mixins import LoginRequiredMixin

class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'todo/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        now = timezone.now()
        tasks = Task.objects.all()
        
        context['total_tasks'] = tasks.count()
        context['completed_tasks'] = tasks.filter(status='Completed').count()
        context['pending_tasks'] = tasks.filter(status='Pending').count()
        context['tasks_this_year'] = tasks.filter(created_at__year=now.year).count()
        
        # Add some data for charts/visuals
        context['recent_tasks'] = tasks.order_by('-created_at')[:5]
        return context

class TaskListView(LoginRequiredMixin, ListView):
    model = Task
    template_name = 'todo/task_list.html'
    context_object_name = 'tasks'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        search_query = self.request.GET.get('q')
        sort_by = self.request.GET.get('sort', '-created_at')
        
        if search_query:
            queryset = queryset.filter(
                Q(title__icontains=search_query) |
                Q(category__name__icontains=search_query) |
                Q(description__icontains=search_query)
            )
        
        # Valid sort fields
        valid_sorts = ['title', 'created_at', 'deadline', 'status', '-title', '-created_at', '-deadline', '-status']
        if sort_by in valid_sorts:
            queryset = queryset.order_by(sort_by)
            
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_query'] = self.request.GET.get('q', '')
        context['current_sort'] = self.request.GET.get('sort', '-created_at')
        return context

class TaskCreateView(LoginRequiredMixin, CreateView):
    model = Task
    template_name = 'todo/task_form.html'
    fields = ['title', 'description', 'deadline', 'status', 'category', 'priority']
    success_url = reverse_lazy('task_list')

class TaskUpdateView(LoginRequiredMixin, UpdateView):
    model = Task
    template_name = 'todo/task_form.html'
    fields = ['title', 'description', 'deadline', 'status', 'category', 'priority']
    success_url = reverse_lazy('task_list')

class TaskDeleteView(LoginRequiredMixin, DeleteView):
    model = Task
    template_name = 'todo/task_confirm_delete.html'
    success_url = reverse_lazy('task_list')
