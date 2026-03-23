from django.contrib import admin
from .models import Priority, Category, Task, Note, SubTask

@admin.register(Priority)
class PriorityAdmin(admin.ModelAdmin):
    list_display = ("status",)
    search_fields = ("status",)

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ("title", "status", "deadline", "priority", "category")
    list_filter = ("status", "priority", "category")
    search_fields = ("title", "description")

@admin.register(SubTask)
class SubTaskAdmin(admin.ModelAdmin):
    list_display = ("title", "status", "get_parent_task_name")
    list_filter = ("status",)
    search_fields = ("title",)

    @admin.display(description="Parent Task")
    def get_parent_task_name(self, obj):
        return obj.parent_task.title

@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    list_display = ("task", "content_snippet", "created_at")
    list_filter = ("created_at",)
    search_fields = ("content",)

    @admin.display(description="Content")
    def content_snippet(self, obj):
        return obj.content[:50]
