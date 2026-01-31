from django.db import models
from django.contrib.auth import get_user_model
from apps.main.models import TimeStampedModel

User = get_user_model()


class DailyTask(TimeStampedModel):
    class TaskType(models.TextChoices):
        HOMEWORK = 'homework', 'Homework'
        LESSON = 'lesson', 'Lesson'

    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    task_type = models.CharField(max_length=20,choices=TaskType.choices)
    assigned_to = models.ForeignKey(User,on_delete=models.CASCADE,related_name='tasks')
    assigned_by = models.ForeignKey(User,on_delete=models.SET_NULL,null=True,related_name='created_tasks')
    due_date = models.DateField()
    is_completed = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.title} ({self.task_type})"

class HomeworkSubmission(TimeStampedModel):
    task = models.ForeignKey(DailyTask,on_delete=models.CASCADE,related_name='submissions')
    student = models.ForeignKey(User,on_delete=models.CASCADE,related_name='homework_submissions')
    text_answer = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.student} → {self.task.title}"
    
class HomeworkImage(models.Model):
    submission = models.ForeignKey(HomeworkSubmission,on_delete=models.CASCADE,related_name='images')
    image = models.ImageField()

    def __str__(self):
        return self.submission

class HomeworkReview(TimeStampedModel):
    submission = models.OneToOneField(HomeworkSubmission,on_delete=models.CASCADE,related_name='review')
    mentor = models.ForeignKey(User,on_delete=models.CASCADE,related_name='homework_reviews')
    is_approved = models.BooleanField(default=False)
    comment = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Review by {self.mentor}"
