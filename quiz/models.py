from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class DifficultyLevel(models.Model):
    level = models.CharField(max_length=50, unique=True)  

    def __str__(self):
        return self.level

class Quiz(models.Model):
    title = models.CharField(max_length=200)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name="quizzes")
    difficulty = models.ForeignKey(DifficultyLevel, on_delete=models.SET_NULL, null=True, related_name="quizzes")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Question(models.Model):
    QUESTION_TYPE_CHOICES = [
        ('multiple_choice', 'Multiple Choice'),
        ('true_false', 'True/False'),
        ('fill_blank', 'Fill in the Blank'),
        ('coding', 'Coding Question')
    ]
    
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name="questions")
    text = models.CharField(max_length=500)
    question_type = models.CharField(max_length=20, choices=QUESTION_TYPE_CHOICES, default='multiple_choice')
    time_limit = models.IntegerField(default=30)  # Time limit for each question in seconds
    hint = models.TextField(blank=True, null=True)  # Optional hint for the question
    explanation = models.TextField(blank=True, null=True)  # Explanation for the answer
    
    # For coding questions
    code_template = models.TextField(blank=True, null=True)  # Initial code template
    expected_output = models.TextField(blank=True, null=True)  # Expected output for code testing
    
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
    choice = models.ForeignKey(Choice, on_delete=models.CASCADE, null=True, blank=True)  
    user_answer_text = models.TextField(null=True, blank=True)  
    user_code_answer = models.TextField(null=True, blank=True)  
    is_correct = models.BooleanField(default=False)
    taken_at = models.DateTimeField(default=timezone.now)
    hint_used = models.BooleanField(default=False)  
    explanation = models.TextField(null=True, blank=True)
    score = models.IntegerField(default=0) 

    def save(self, *args, **kwargs):
        if self.choice:
            self.is_correct = self.choice.is_correct
        
        elif self.question.question_type == 'fill_blank' and self.user_answer_text:
            correct_answer = self.question.choices.filter(is_correct=True).first()
            if correct_answer and self.user_answer_text.strip().lower() == correct_answer.text.strip().lower():
                self.is_correct = True
        
        elif self.question.question_type == 'coding' and self.user_code_answer and self.question.expected_output:
            if self.user_code_answer.strip() == self.question.expected_output.strip():
                self.is_correct = True
        
        if not self.taken_at:
            self.taken_at = timezone.now()
        
        # Calculate score
        if self.is_correct:
            self.score = 10  # Assign 10 points for each correct answer
        else:
            self.score = 0  # Ensure score is 0 for incorrect answers
        
        super().save(*args, **kwargs)

    class Meta:
        unique_together = ['user', 'quiz', 'question']