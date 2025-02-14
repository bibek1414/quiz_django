
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Quiz(models.Model):
    title = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Question(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name="questions")
    text = models.CharField(max_length=500)
    time_limit = models.IntegerField(default=30)  # Time limit for each question in seconds

    def __str__(self):
        return self.text

class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="choices")
    text = models.CharField(max_length=200)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return self.text

class Result(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice = models.ForeignKey(Choice, on_delete=models.CASCADE)
    is_correct = models.BooleanField(default=False)
    taken_at = models.DateTimeField(default=timezone.now)

    def save(self, *args, **kwargs):
        # Ensure the correct answer is marked as True for the Result
        if self.choice.is_correct:  # Check if the choice is correct
            self.is_correct = True
        else:
            self.is_correct = False
        
        # Set the taken_at timestamp to now if not already set
        if not self.taken_at:
            self.taken_at = timezone.now()
        
        super().save(*args, **kwargs)

    class Meta:
        unique_together = ['user', 'quiz', 'question']