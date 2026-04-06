from django.shortcuts import render, redirect
from django.views.generic import ListView, TemplateView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.db.models import Q
from django.utils import timezone
from .models import Task, Category, Priority, SubTask, Note
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

class CategoryListView(LoginRequiredMixin, ListView):
    model = Category
    template_name = 'todo/category_list.html'
    context_object_name = 'categories'

class CategoryCreateView(LoginRequiredMixin, CreateView):
    model = Category
    template_name = 'todo/category_form.html'
    fields = ['name']
    success_url = reverse_lazy('category_list')

class CategoryUpdateView(LoginRequiredMixin, UpdateView):
    model = Category
    template_name = 'todo/category_form.html'
    fields = ['name']
    success_url = reverse_lazy('category_list')

class CategoryDeleteView(LoginRequiredMixin, DeleteView):
    model = Category
    template_name = 'todo/category_confirm_delete.html'
    success_url = reverse_lazy('category_list')

class PriorityListView(LoginRequiredMixin, ListView):
    model = Priority
    template_name = 'todo/priority_list.html'
    context_object_name = 'priorities'

class PriorityCreateView(LoginRequiredMixin, CreateView):
    model = Priority
    template_name = 'todo/priority_form.html'
    fields = ['status']
    success_url = reverse_lazy('priority_list')

class PriorityUpdateView(LoginRequiredMixin, UpdateView):
    model = Priority
    template_name = 'todo/priority_form.html'
    fields = ['status']
    success_url = reverse_lazy('priority_list')

class PriorityDeleteView(LoginRequiredMixin, DeleteView):
    model = Priority
    template_name = 'todo/priority_confirm_delete.html'
    success_url = reverse_lazy('priority_list')

class SubTaskListView(LoginRequiredMixin, ListView):
    model = SubTask
    template_name = 'todo/subtask_list.html'
    context_object_name = 'subtasks'

class SubTaskCreateView(LoginRequiredMixin, CreateView):
    model = SubTask
    template_name = 'todo/subtask_form.html'
    fields = ['title', 'status', 'parent_task']
    success_url = reverse_lazy('subtask_list')

class SubTaskUpdateView(LoginRequiredMixin, UpdateView):
    model = SubTask
    template_name = 'todo/subtask_form.html'
    fields = ['title', 'status', 'parent_task']
    success_url = reverse_lazy('subtask_list')

class SubTaskDeleteView(LoginRequiredMixin, DeleteView):
    model = SubTask
    template_name = 'todo/subtask_confirm_delete.html'
    success_url = reverse_lazy('subtask_list')

class NoteListView(LoginRequiredMixin, ListView):
    model = Note
    template_name = 'todo/note_list.html'
    context_object_name = 'notes'

class NoteCreateView(LoginRequiredMixin, CreateView):
    model = Note
    template_name = 'todo/note_form.html'
    fields = ['content', 'task']
    success_url = reverse_lazy('note_list')

class NoteUpdateView(LoginRequiredMixin, UpdateView):
    model = Note
    template_name = 'todo/note_form.html'
    fields = ['content', 'task']
    success_url = reverse_lazy('note_list')

class NoteDeleteView(LoginRequiredMixin, DeleteView):
    model = Note
    template_name = 'todo/note_confirm_delete.html'
    success_url = reverse_lazy('note_list')

class OfflineView(TemplateView):
    template_name = 'todo/offline.html'
