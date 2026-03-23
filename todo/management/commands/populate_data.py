from django.core.management.base import BaseCommand
from django.utils import timezone
from faker import Faker
import random
from todo.models import Priority, Category, Task, Note, SubTask

class Command(BaseCommand):
    help = 'Populate the database with initial and fake data'

    def handle(self, *args, **kwargs):
        fake = Faker()
        
        # 1. Populate Priorities
        priority_names = ["High", "Medium", "Low", "Critical", "Optional"]
        priorities = []
        for name in priority_names:
            p, created = Priority.objects.get_or_create(status=name)
            priorities.append(p)
            if created:
                self.stdout.write(self.style.SUCCESS(f'Created priority: {name}'))

        # 2. Populate Categories
        category_names = ["Work", "School", "Personal", "Finance", "Projects"]
        categories = []
        for name in category_names:
            c, created = Category.objects.get_or_create(name=name)
            categories.append(c)
            if created:
                self.stdout.write(self.style.SUCCESS(f'Created category: {name}'))

        # 3. Create Tasks
        statuses = ["Pending", "In Progress", "Completed"]
        for _ in range(20):
            title = fake.sentence(nb_words=5).rstrip('.')
            description = fake.paragraph(nb_sentences=3)
            deadline = timezone.make_aware(fake.date_time_this_month())
            status = fake.random_element(elements=statuses)
            category = random.choice(categories)
            priority = random.choice(priorities)
            
            task = Task.objects.create(
                title=title,
                description=description,
                deadline=deadline,
                status=status,
                category=category,
                priority=priority
            )
            
            # create some notes for each task
            for _ in range(random.randint(1, 4)):
                Note.objects.create(
                    content=fake.paragraph(nb_sentences=2),
                    task=task
                )
                
            # create some subtasks for each task
            for _ in range(random.randint(2, 5)):
                SubTask.objects.create(
                    title=fake.sentence(nb_words=3).rstrip('.'),
                    status=fake.random_element(elements=statuses),
                    parent_task=task
                )
                
        self.stdout.write(self.style.SUCCESS('Successfully populated fake data!'))
