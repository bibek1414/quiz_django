from django.core.management.base import BaseCommand
from quiz.models import Category, DifficultyLevel, Quiz, Question, Choice

class Command(BaseCommand):
    help = 'Adds a puzzle quiz with 10 challenging questions, each with four choices, hints, and explanations.'

    def handle(self, *args, **kwargs):
        # Create categories
        puzzles, created = Category.objects.get_or_create(name="Math Puzzles")
        
        # Create difficulty levels
        hard, created = DifficultyLevel.objects.get_or_create(level="Hard")
        very_hard, created = DifficultyLevel.objects.get_or_create(level="Very Hard")
        
        # Create a quiz
        quiz = Quiz.objects.create(
            title="Brain Teaser Puzzle Challenge",
            category=puzzles,
            difficulty=very_hard  # Set the difficulty level to "Very Hard"
        )
        
        # Add 10 challenging brain teaser questions with hints and explanations
        questions_data = [
            {
                "text": "If a plane crashes on the border between the US and Canada, where do they bury the survivors?",
                "question_type": "multiple_choice",
                "hint": "Think about who survives a plane crash.",
                "explanation": "Survivors are not buried, so the answer is none of the above.",
                "choices": [
                    {"text": "In the US", "is_correct": False},
                    {"text": "In Canada", "is_correct": False},
                    {"text": "In the Ocean", "is_correct": False},
                    {"text": "Nowhere", "is_correct": True},
                ]
            },
            {
                "text": "What is always in front of you but can’t be seen?",
                "question_type": "multiple_choice",
                "hint": "It’s a concept, not a physical object.",
                "explanation": "The answer is 'The future.'",
                "choices": [
                    {"text": "The past", "is_correct": False},
                    {"text": "Your nose", "is_correct": False},
                    {"text": "Your reflection", "is_correct": False},
                    {"text": "The future", "is_correct": True},
                ]
            },
            {
                "text": "What can travel around the world while staying in the corner?",
                "question_type": "multiple_choice",
                "hint": "Think about stamps on a letter.",
                "explanation": "A stamp stays in the corner of an envelope while the letter travels around the world.",
                "choices": [
                    {"text": "A coin", "is_correct": False},
                    {"text": "A clock", "is_correct": False},
                    {"text": "A stamp", "is_correct": True},
                    {"text": "A bird", "is_correct": False},
                ]
            },
            {
                "text": "If two’s company and three’s a crowd, what is four and five?",
                "question_type": "multiple_choice",
                "hint": "Do the math.",
                "explanation": "The answer is 'Nine' because 4 + 5 = 9.",
                "choices": [
                    {"text": "Eleven", "is_correct": False},
                    {"text": "Nine", "is_correct": True},
                    {"text": "Seven", "is_correct": False},
                    {"text": "Eight", "is_correct": False},
                ]
            },
            {
                "text": "What comes once in a minute, twice in a moment, but never in a thousand years?",
                "question_type": "multiple_choice",
                "hint": "Think about letters.",
                "explanation": "The answer is 'The letter M.'",
                "choices": [
                    {"text": "The letter M", "is_correct": True},
                    {"text": "Time", "is_correct": False},
                    {"text": "The sun", "is_correct": False},
                    {"text": "A star", "is_correct": False},
                ]
            },
            {
                "text": "A man gave one son 10 cents and another son was given 15 cents. What time is it?",
                "question_type": "multiple_choice",
                "hint": "It’s not about the money.",
                "explanation": "The answer is 'A quarter to two.' (The two sons were given 10 cents and 15 cents, which are a quarter and a dime).",
                "choices": [
                    {"text": "A quarter past one", "is_correct": False},
                    {"text": "A quarter to two", "is_correct": True},
                    {"text": "One o’clock", "is_correct": False},
                    {"text": "Two o’clock", "is_correct": False},
                ]
            },
            {
                "text": "You see a house with two doors. One door leads to certain death and the other leads to freedom. There are two guards, one who always tells the truth and one who always lies. You can ask only one question. What do you ask?",
                "question_type": "multiple_choice",
                "hint": "Ask a question that will give you the right door no matter which guard answers.",
                "explanation": "Ask either guard, 'If I were to ask the other guard which door leads to freedom, which would they point to?' Then go through the opposite door.",
                "choices": [
                    {"text": "Which door leads to freedom?", "is_correct": False},
                    {"text": "What is the truth?", "is_correct": False},
                    {"text": "Which door leads to certain death?", "is_correct": False},
                    {"text": "If I were to ask the other guard which door leads to freedom, which would they point to?", "is_correct": True},
                ]
            },
            {
                "text": "The more you take, the more you leave behind. What am I?",
                "question_type": "multiple_choice",
                "hint": "Think about the path you walk.",
                "explanation": "The answer is 'Footsteps.'",
                "choices": [
                    {"text": "Memories", "is_correct": False},
                    {"text": "Footsteps", "is_correct": True},
                    {"text": "Time", "is_correct": False},
                    {"text": "Air", "is_correct": False},
                ]
            },
            {
                "text": "What has keys but can't open locks?",
                "question_type": "multiple_choice",
                "hint": "It's a musical instrument.",
                "explanation": "The answer is 'A piano.'",
                "choices": [
                    {"text": "A lockbox", "is_correct": False},
                    {"text": "A piano", "is_correct": True},
                    {"text": "A map", "is_correct": False},
                    {"text": "A book", "is_correct": False},
                ]
            },
            {
                "text": "If a tree falls in a forest and no one is around to hear it, does it make a sound?",
                "question_type": "true_false",
                "hint": "It’s a philosophical question.",
                "explanation": "The answer is 'False'. The concept of sound requires a listener to perceive it.",
                "choices": [
                    {"text": "True", "is_correct": False},
                    {"text": "False", "is_correct": True},
                ]
            },
        ]
        
        # Add questions and choices to the quiz
        for question_data in questions_data:
            question = Question.objects.create(
                quiz=quiz,
                text=question_data["text"],
                question_type=question_data["question_type"],
                time_limit=55,  # Set time limit to 55 seconds for hard/very hard questions
                hint=question_data["hint"],
                explanation=question_data["explanation"]
            )
            for choice_data in question_data["choices"]:
                Choice.objects.create(
                    question=question,
                    text=choice_data["text"],
                    is_correct=choice_data["is_correct"]
                )
        
        self.stdout.write(self.style.SUCCESS('Successfully added a brain teaser puzzle quiz with 10 challenging questions, hints, and explanations.'))
