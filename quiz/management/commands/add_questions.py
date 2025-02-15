import random
from django.core.management.base import BaseCommand
from quiz.models import Quiz, Question, Choice

class Command(BaseCommand):
    help = 'Automatically add questions and choices to the database'

    def handle(self, *args, **kwargs):
        quizzes_data = {}
        for quiz_title, questions_data in quizzes_data.items():
            quiz, created = Quiz.objects.get_or_create(title=quiz_title)

            # Add questions and choices for each quiz
            for question_data in questions_data:
                question = Question.objects.create(
                    quiz=quiz,
                    text=question_data["text"],
                    time_limit=question_data["time_limit"],
                )

                # Shuffle choices before saving
                choices = question_data["choices"]
                random.shuffle(choices)

                # Add choices to each question
                for choice_data in choices:
                    Choice.objects.create(
                        question=question,
                        text=choice_data["text"],
                        is_correct=choice_data["is_correct"],
                    )

        self.stdout.write(self.style.SUCCESS('Successfully added quizzes, questions, and choices!'))