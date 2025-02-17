from django.core.management.base import BaseCommand
from quiz.models import Category, DifficultyLevel, Quiz, Question, Choice
import random

class Command(BaseCommand):
    help = 'Adds mind-challenging quizzes with 10 questions for each difficulty level'

    def handle(self, *args, **kwargs):
        # Create categories
        mind_challenges, created = Category.objects.get_or_create(name="Mind Challenges")
        
        # Create difficulty levels
        easy, created = DifficultyLevel.objects.get_or_create(level="Easy")
        medium, created = DifficultyLevel.objects.get_or_create(level="Medium")
        hard, created = DifficultyLevel.objects.get_or_create(level="Hard")
        extreme, created = DifficultyLevel.objects.get_or_create(level="Extreme")
        
        # Mind-challenging questions for each difficulty level
        questions_data = {
            easy: [
                {
                    "text": "Question 1: A farmer has 17 sheep. All but 9 die. How many sheep are left?",
                    "choices": [
                        {"text": "9", "is_correct": True},
                        {"text": "8", "is_correct": False},
                        {"text": "0", "is_correct": False},
                        {"text": "17", "is_correct": False},
                    ]
                },
                {
                    "text": "Question 2: If you multiply this number by any other number, the answer will always be the same. What number is it?",
                    "choices": [
                        {"text": "Zero", "is_correct": True},
                        {"text": "One", "is_correct": False},
                        {"text": "Ten", "is_correct": False},
                        {"text": "Hundred", "is_correct": False},
                    ]
                },
                {
                    "text": "Question 3: What is at the end of a rainbow?",
                    "choices": [
                        {"text": "The letter W", "is_correct": True},
                        {"text": "Gold", "is_correct": False},
                        {"text": "Colors", "is_correct": False},
                        {"text": "Nothing", "is_correct": False},
                    ]
                },
                {
                    "text": "Question 4: What room can no one enter?",
                    "choices": [
                        {"text": "A mushroom", "is_correct": True},
                        {"text": "A bedroom", "is_correct": False},
                        {"text": "A bathroom", "is_correct": False},
                        {"text": "A living room", "is_correct": False},
                    ]
                },
                {
                    "text": "Question 5: What word is always spelled wrong in the dictionary?",
                    "choices": [
                        {"text": "Wrong", "is_correct": True},
                        {"text": "Incorrect", "is_correct": False},
                        {"text": "Misspelled", "is_correct": False},
                        {"text": "Error", "is_correct": False},
                    ]
                },
                {
                    "text": "Question 6: What occurs once in every minute, twice in every moment, but never in a thousand years?",
                    "choices": [
                        {"text": "The letter M", "is_correct": True},
                        {"text": "Time", "is_correct": False},
                        {"text": "Space", "is_correct": False},
                        {"text": "Numbers", "is_correct": False},
                    ]
                },
                {
                    "text": "Question 7: What has 13 hearts but no organs?",
                    "choices": [
                        {"text": "A deck of cards", "is_correct": True},
                        {"text": "A valentine's box", "is_correct": False},
                        {"text": "A hospital", "is_correct": False},
                        {"text": "A love story", "is_correct": False},
                    ]
                },
                {
                    "text": "Question 8: What has a thumb and four fingers but is not alive?",
                    "choices": [
                        {"text": "A glove", "is_correct": True},
                        {"text": "A hand drawing", "is_correct": False},
                        {"text": "A robot hand", "is_correct": False},
                        {"text": "A statue", "is_correct": False},
                    ]
                },
                {
                    "text": "Question 9: What has keys but no locks, space but no room?",
                    "choices": [
                        {"text": "A keyboard", "is_correct": True},
                        {"text": "A house", "is_correct": False},
                        {"text": "A car", "is_correct": False},
                        {"text": "A phone", "is_correct": False},
                    ]
                },
                {
                    "text": "Question 10: The more of them you take, the more you leave behind. What are they?",
                    "choices": [
                        {"text": "Footsteps", "is_correct": True},
                        {"text": "Memories", "is_correct": False},
                        {"text": "Time", "is_correct": False},
                        {"text": "Thoughts", "is_correct": False},
                    ]
                },
            ],
            medium: [
                {
                    "text": "Question 1: If it takes 5 machines 5 minutes to make 5 widgets, how long would it take 100 machines to make 100 widgets?",
                    "choices": [
                        {"text": "5 minutes", "is_correct": True},
                        {"text": "100 minutes", "is_correct": False},
                        {"text": "20 minutes", "is_correct": False},
                        {"text": "500 minutes", "is_correct": False},
                    ]
                },
                {
                    "text": "Question 2: A doctor gives you three pills and tells you to take one every half hour. How long would the pills last?",
                    "choices": [
                        {"text": "1 hour", "is_correct": True},
                        {"text": "1.5 hours", "is_correct": False},
                        {"text": "2 hours", "is_correct": False},
                        {"text": "30 minutes", "is_correct": False},
                    ]
                },
                {
                    "text": "Question 3: In a year, there are 12 months. Seven months have 31 days. How many months have 28 days?",
                    "choices": [
                        {"text": "All of them", "is_correct": True},
                        {"text": "One", "is_correct": False},
                        {"text": "Five", "is_correct": False},
                        {"text": "Four", "is_correct": False},
                    ]
                },
                {
                    "text": "Question 4: What is always coming but never arrives?",
                    "choices": [
                        {"text": "Tomorrow", "is_correct": True},
                        {"text": "Today", "is_correct": False},
                        {"text": "Time", "is_correct": False},
                        {"text": "Future", "is_correct": False},
                    ]
                },
                {
                    "text": "Question 5: What gets wetter and wetter the more it dries?",
                    "choices": [
                        {"text": "A towel", "is_correct": True},
                        {"text": "A sponge", "is_correct": False},
                        {"text": "Clothes", "is_correct": False},
                        {"text": "Hair", "is_correct": False},
                    ]
                },
                {
                    "text": "Question 6: What building has the most stories?",
                    "choices": [
                        {"text": "A library", "is_correct": True},
                        {"text": "A skyscraper", "is_correct": False},
                        {"text": "Empire State", "is_correct": False},
                        {"text": "Burj Khalifa", "is_correct": False},
                    ]
                },
                {
                    "text": "Question 7: What has branches and leaves but no bark?",
                    "choices": [
                        {"text": "A library book", "is_correct": True},
                        {"text": "A bush", "is_correct": False},
                        {"text": "A plant", "is_correct": False},
                        {"text": "A vine", "is_correct": False},
                    ]
                },
                {
                    "text": "Question 8: What invention lets you look right through a wall?",
                    "choices": [
                        {"text": "A window", "is_correct": True},
                        {"text": "X-ray", "is_correct": False},
                        {"text": "Camera", "is_correct": False},
                        {"text": "Telescope", "is_correct": False},
                    ]
                },
                {
                    "text": "Question 9: What kind of coat is always wet when you put it on?",
                    "choices": [
                        {"text": "A coat of paint", "is_correct": True},
                        {"text": "A raincoat", "is_correct": False},
                        {"text": "A winter coat", "is_correct": False},
                        {"text": "A fur coat", "is_correct": False},
                    ]
                },
                {
                    "text": "Question 10: What has keys that open no doors, space but no room, and you can enter but not go in?",
                    "choices": [
                        {"text": "A keyboard", "is_correct": True},
                        {"text": "A phone", "is_correct": False},
                        {"text": "A computer", "is_correct": False},
                        {"text": "A calculator", "is_correct": False},
                    ]
                },
            ],
            hard: [
                {
                    "text": "Question 1: I am an odd number. Take away a letter and I become even. What number am I?",
                    "choices": [
                        {"text": "Seven", "is_correct": True},
                        {"text": "Three", "is_correct": False},
                        {"text": "Five", "is_correct": False},
                        {"text": "Nine", "is_correct": False},
                    ]
                },
                {
                    "text": "Question 2: What starts with 'e', ends with 'e', but only contains one letter?",
                    "choices": [
                        {"text": "Envelope", "is_correct": True},
                        {"text": "Eye", "is_correct": False},
                        {"text": "Everyone", "is_correct": False},
                        {"text": "Exercise", "is_correct": False},
                    ]
                },
                {
                    "text": "Question 3: A girl has as many brothers as sisters, but each brother has only half as many brothers as sisters. How many brothers and sisters are there?",
                    "choices": [
                        {"text": "4 sisters, 3 brothers", "is_correct": True},
                        {"text": "3 sisters, 3 brothers", "is_correct": False},
                        {"text": "4 sisters, 4 brothers", "is_correct": False},
                        {"text": "3 sisters, 4 brothers", "is_correct": False},
                    ]
                },
                {
                    "text": "Question 4: Which word in the dictionary is spelled incorrectly?",
                    "choices": [
                        {"text": "Incorrectly", "is_correct": True},
                        {"text": "Misspelled", "is_correct": False},
                        {"text": "Wrong", "is_correct": False},
                        {"text": "Error", "is_correct": False},
                    ]
                },
                {
                    "text": "Question 5: What can you catch but not throw?",
                    "choices": [
                        {"text": "Your breath", "is_correct": True},
                        {"text": "A cold", "is_correct": False},
                        {"text": "Time", "is_correct": False},
                        {"text": "Light", "is_correct": False},
                    ]
                },
                {
                    "text": "Question 6: If you drop a yellow hat in the Red Sea, what does it become?",
                    "choices": [
                        {"text": "Wet", "is_correct": True},
                        {"text": "Red", "is_correct": False},
                        {"text": "Orange", "is_correct": False},
                        {"text": "Lost", "is_correct": False},
                    ]
                },
                {
                    "text": "Question 7: What has one head, one foot, and four legs?",
                    "choices": [
                        {"text": "A bed", "is_correct": True},
                        {"text": "A chair", "is_correct": False},
                        {"text": "A table", "is_correct": False},
                        {"text": "A desk", "is_correct": False},
                    ]
                },
                {
                    "text": "Question 8: What belongs to you but others use it more than you do?",
                    "choices": [
                        {"text": "Your name", "is_correct": True},
                        {"text": "Your phone", "is_correct": False},
                        {"text": "Your car", "is_correct": False},
                        {"text": "Your time", "is_correct": False},
                    ]
                },
                {
                    "text": "Question 9: What is black when clean and white when dirty?",
                    "choices": [
                        {"text": "A chalkboard", "is_correct": True},
                        {"text": "A tire", "is_correct": False},
                        {"text": "A shoe", "is_correct": False},
                        {"text": "A road", "is_correct": False},
                    ]
                },
                {
                    "text": "Question 10: What goes up white and comes down yellow and white?",
                    "choices": [
                        {"text": "An egg", "is_correct": True},
                        {"text": "A flower", "is_correct": False},
                        {"text": "A bird", "is_correct": False},
                        {"text": "A cloud", "is_correct": False},
                    ]
                },
            ],
            extreme: [
                {
                "text": "Question 1: Two fathers and two sons go fishing together. They each catch a fish and bring home one each. Yet there are only three fish. How is this possible?",
                "choices": [
                    {"text": "They are grandfather, father, and son", "is_correct": True},
                    {"text": "One fish escaped", "is_correct": False},
                    {"text": "They shared one fish", "is_correct": False},
                    {"text": "They lost one fish", "is_correct": False}
                ]
                },
                {
                "text": "Question 2: What can fill a room but takes up no space?",
                "choices": [
                    {"text": "Light", "is_correct": True},
                    {"text": "Air", "is_correct": False},
                    {"text": "Sound", "is_correct": False},
                    {"text": "Dark", "is_correct": False}
                ]
                },
                {
                "text": "Question 3: If you have me, you want to share me. If you share me, you haven't got me. What am I?",
                "choices": [
                    {"text": "A secret", "is_correct": True},
                    {"text": "Love", "is_correct": False},
                    {"text": "Money", "is_correct": False},
                    {"text": "Time", "is_correct": False}
                ]
                },
                {
                "text": "Question 4: A man is looking at a photograph of someone. His friend asks who it is. The man replies, 'Brothers and sisters, I have none. But that man's father is my father's son.' Who was in the photograph?",
                "choices": [
                    {"text": "His son", "is_correct": True},
                    {"text": "His brother", "is_correct": False},
                    {"text": "His father", "is_correct": False},
                    {"text": "His friend", "is_correct": False}
                ]
                },
                {
                "text": "Question 5: What has a heart that doesn’t beat?",
                "choices": [
                    {"text": "An artichoke", "is_correct": True},
                    {"text": "A clock", "is_correct": False},
                    {"text": "A tree", "is_correct": False},
                    {"text": "A stone", "is_correct": False}
                ]
                },
                {
                "text": "Question 6: You see a house with two doors. One door leads to certain death, and the other leads to freedom. There are two guards. One always tells the truth, and one always lies. You can ask one question to one guard to find the correct door. What question do you ask?",
                "choices": [
                    {"text": "If I asked the other guard which door leads to freedom, which one would they say?", "is_correct": True},
                    {"text": "Which door leads to freedom?", "is_correct": False},
                    {"text": "Which guard is telling the truth?", "is_correct": False},
                    {"text": "Can you point to the death door?", "is_correct": False}
                ]
                },
                {
                "text": "Question 7: You have a bucket that holds exactly 3 gallons of water and another bucket that holds exactly 5 gallons of water. How can you measure exactly 4 gallons of water?",
                "choices": [
                    {"text": "Fill the 5-gallon bucket, pour it into the 3-gallon bucket until full, and you'll be left with 4 gallons in the 5-gallon bucket.", "is_correct": True},
                    {"text": "Fill the 3-gallon bucket, then fill the 5-gallon bucket", "is_correct": False},
                    {"text": "Fill the 5-gallon bucket twice", "is_correct": False},
                    {"text": "Use a measuring cup", "is_correct": False}
                ]
                },
                {
                "text": "Question 8: A man is pushing his car along a road when he comes to a hotel. He shouts, 'I’m bankrupt!' Why?",
                "choices": [
                    {"text": "He is playing Monopoly", "is_correct": True},
                    {"text": "He is broke and lost all his money", "is_correct": False},
                    {"text": "He owes the hotel money", "is_correct": False},
                    {"text": "He lost his job", "is_correct": False}
                ]
                },
                {
                "text": "Question 9: You’re in a room with two doors. One leads to freedom and the other leads to certain death. You don’t know which is which. The guards at each door will either always tell the truth or always lie. What question can you ask to find the door to freedom?",
                "choices": [
                    {"text": "Ask one guard, 'What would the other guard say if I asked which door leads to freedom?'", "is_correct": True},
                    {"text": "Ask both guards to point to the correct door", "is_correct": False},
                    {"text": "Ask both guards which door they would choose", "is_correct": False},
                    {"text": "Ask one guard if the door to the left leads to freedom", "is_correct": False}
                ]
                },
                {
                "text": "Question 10: A father and son are in a car accident. The father dies, and the son is taken to the hospital. The surgeon looks at him and says, 'I can't operate on him; he's my son.' How is this possible?",
                "choices": [
                    {"text": "The surgeon is his mother", "is_correct": True},
                    {"text": "The surgeon is his uncle", "is_correct": False},
                    {"text": "The surgeon is his brother", "is_correct": False},
                    {"text": "The surgeon is a family friend", "is_correct": False}
                ]
                }
            ]
                    }

        # Add questions and choices to the quiz for each difficulty level
        for difficulty, questions in questions_data.items():
            quiz = Quiz.objects.create(
                title=f"Mind Challenging - {difficulty.level}",
                category=mind_challenges,
                difficulty=difficulty
            )
            for question_data in questions:
                question = Question.objects.create(
                    quiz=quiz,
                    text=question_data["text"],
                    question_type="multiple_choice",
                    time_limit=50,  # Set time limit to 50 seconds for riddles
                    hint="Think carefully about the riddle.",
                    explanation="The answer is based on the riddle's logic."
                )
                
                # Get the choices and ensure the correct answer is not at position A
                choices = question_data["choices"].copy()
                
                # Find the correct answer
                correct_choice = next(choice for choice in choices if choice["is_correct"])
                incorrect_choices = [choice for choice in choices if not choice["is_correct"]]
                
                # Shuffle incorrect choices
                random.shuffle(incorrect_choices)
                
                # Create the final choice list making sure correct answer is not in first position
                final_choices = [incorrect_choices[0]]  # First position is always incorrect
                
                # Insert correct choice at a random position after the first
                correct_position = random.randint(1, 3)
                final_choices.insert(correct_position, correct_choice)
                
                # Fill the remaining positions with incorrect choices
                remaining_incorrect = incorrect_choices[1:]
                for i in range(1, 4):
                    if i != correct_position:
                        if remaining_incorrect:
                            final_choices.insert(i, remaining_incorrect.pop(0))
                
                # Create the choices in database
                for choice_data in final_choices:
                    Choice.objects.create(
                        question=question,
                        text=choice_data["text"],
                        is_correct=choice_data["is_correct"]
                    )
        
        self.stdout.write(self.style.SUCCESS('Successfully added riddle quizzes with 10 questions for each difficulty level.'))