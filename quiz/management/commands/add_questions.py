
from django.core.management.base import BaseCommand
from quiz.models import Category, DifficultyLevel, Quiz, Question, Choice
import random

class Command(BaseCommand):
    help = 'Adds MLBB quizzes with 10 questions for each difficulty level'

    def handle(self, *args, **kwargs):
        # Create MLBB category
        mlbb_category, created = Category.objects.get_or_create(name="Mobile Legends: Bang Bang")
        
        # Create difficulty levels
        easy, created = DifficultyLevel.objects.get_or_create(level="Easy")
        medium, created = DifficultyLevel.objects.get_or_create(level="Medium")
        hard, created = DifficultyLevel.objects.get_or_create(level="Hard")
        extreme, created = DifficultyLevel.objects.get_or_create(level="Extreme")
        
        # MLBB questions for each difficulty level
        questions_data = {
            easy: [
                {
                    "text": "Question 1: Which hero is known as the 'Fighter of the Dawn'?",
                    "choices": [
                        {"text": "Alucard", "is_correct": True},
                        {"text": "Fanny", "is_correct": False},
                        {"text": "Layla", "is_correct": False},
                        {"text": "Gusion", "is_correct": False},
                    ],
                    "hint": "This hero is a melee fighter with lifesteal abilities.",
                    "explanation": "Alucard is known as the 'Fighter of the Dawn' due to his lifesteal and melee combat skills."
                },
                {
                    "text": "Question 2: What is the name of the dragon that spawns in the river?",
                    "choices": [
                        {"text": "Lord", "is_correct": False},
                        {"text": "Turtle", "is_correct": False},
                        {"text": "Crab", "is_correct": False},
                        {"text": "None of the above", "is_correct": True},
                    ],
                    "hint": "The dragon is a powerful neutral monster that provides buffs.",
                    "explanation": "There is no dragon in the river; the Turtle and Lord are the main neutral monsters."
                },
                {
                    "text": "Question 3: Which hero is known for her ultimate ability 'Demon Slayer'?",
                    "choices": [
                        {"text": "Aldous", "is_correct": True},
                        {"text": "Lancelot", "is_correct": False},
                        {"text": "Gusion", "is_correct": False},
                        {"text": "Kagura", "is_correct": False},
                    ],
                    "hint": "This hero can deal massive damage to a single target.",
                    "explanation": "Aldous's ultimate ability 'Demon Slayer' allows him to deal massive damage to a single enemy hero."
                },
                {
                    "text": "Question 4: What is the primary role of a tank hero?",
                    "choices": [
                        {"text": "Damage dealer", "is_correct": False},
                        {"text": "Support", "is_correct": False},
                        {"text": "Crowd control", "is_correct": False},
                        {"text": "Absorb damage", "is_correct": True},
                    ],
                    "hint": "These heroes are often at the front lines.",
                    "explanation": "Tank heroes are designed to absorb damage and protect their teammates."
                },
                {
                    "text": "Question 5: Which item grants additional health and mana regeneration?",
                    "choices": [
                        {"text": "Blade of Despair", "is_correct": False},
                        {"text": "Oracle", "is_correct": True},
                        {"text": "Endless Battle", "is_correct": False},
                        {"text": "Bloodlust Axe", "is_correct": False},
                    ],
                    "hint": "This item is often used by support heroes.",
                    "explanation": "Oracle grants additional health and mana regeneration to the user and nearby allies."
                },
                {
                    "text": "Question 6: What is the maximum number of players in a standard MLBB match?",
                    "choices": [
                        {"text": "5", "is_correct": True},
                        {"text": "10", "is_correct": False},
                        {"text": "7", "is_correct": False},
                        {"text": "3", "is_correct": False},
                    ],
                    "hint": "Each team consists of the same number of players.",
                    "explanation": "A standard MLBB match consists of 5 players on each team."
                },
                {
                    "text": "Question 7: Which hero is known for her ability to heal allies?",
                    "choices": [
                        {"text": "Angela", "is_correct": True},
                        {"text": "Lylia", "is_correct": False},
                        {"text": "Kaja", "is_correct": False},
                        {"text": "Gord", "is_correct": False},
                    ],
                    "hint": "This hero can also attach to allies.",
                    "explanation": "Angela can heal allies and attach to them, providing additional support."
                },
                {
                    "text": "Question 8: What is the primary objective in MLBB?",
                    "choices": [
                        {"text": "Destroy the enemy base", "is_correct": True},
                        {"text": "Kill the most heroes", "is_correct": False},
                        {"text": "Collect the most gold", "is_correct": False},
                        {"text": "Capture the most turrets", "is_correct": False},
                    ],
                    "hint": "The game ends when one team's base is destroyed.",
                    "explanation": "The primary objective in MLBB is to destroy the enemy's base."
                },
                {
                    "text": "Question 9: Which hero is known for her crowd control abilities?",
                    "choices": [
                        {"text": "Layla", "is_correct": False},
                        {"text": "Kagura", "is_correct": True},
                        {"text": "Miya", "is_correct": False},
                        {"text": "Fanny", "is_correct": False},
                    ],
                    "hint": "This hero can control the battlefield with her skills.",
                    "explanation": "Kagura has crowd control abilities that can disrupt enemy movements."
                },
                {
                    "text": "Question 10: What is the role of a marksman in MLBB?",
                    "choices": [
                        {"text": "Tank", "is_correct": False},
                        {"text": "Damage dealer", "is_correct": True},
                        {"text": "Support", "is_correct": False},
                        {"text": "Crowd control", "is_correct": False},
                    ],
                    "hint": "These heroes deal damage from a distance.",
                    "explanation": "Marksmen are ranged heroes that deal damage from a distance."
                },
            ],
            medium: [
                {
                    "text": "Question 1: Which hero can teleport to their sword?",
                    "choices": [
                        {"text": "Chou", "is_correct": False},
                        {"text": "Lancelot", "is_correct": False},
                        {"text": "Hayabusa", "is_correct": False},
                        {"text": "Fanny", "is_correct": True},
                    ],
                    "hint": "This hero uses energy cables to move around the map.",
                    "explanation": "Fanny can teleport to her sword using her energy cables."
                },
                {
                    "text": "Question 2: What is the maximum level a hero can reach in a match?",
                    "choices": [
                        {"text": "15", "is_correct": True},
                        {"text": "20", "is_correct": False},
                        {"text": "10", "is_correct": False},
                        {"text": "25", "is_correct": False},
                    ],
                    "hint": "The level cap is the same for all heroes.",
                    "explanation": "The maximum level a hero can reach in a match is 15."
                },
                {
                    "text": "Question 3: Which hero has the ability 'Blazing Duet'?",
                    "choices": [
                        {"text": "Layla", "is_correct": False},
                        {"text": "Lancelot", "is_correct": False},
                        {"text": "Miya", "is_correct": False},
                        {"text": "Masha", "is_correct": True},
                    ],
                    "hint": "This hero is a marksman with a powerful ultimate.",
                    "explanation": "Masha's ultimate ability 'Blazing Duet' allows her to deal damage in a wide area."
                },
                {
                    "text": "Question 4: What is the cooldown of the Retribution spell at max level?",
                    "choices": [
                        {"text": "30 seconds", "is_correct": False},
                        {"text": "45 seconds", "is_correct": False},
                        {"text": "20 seconds", "is_correct": True},
                        {"text": "60 seconds", "is_correct": False},
                    ],
                    "hint": "Retribution is used primarily by junglers.",
                    "explanation": "The cooldown of Retribution at max level is 20 seconds."
                },
                {
                    "text": "Question 5: Which item grants additional attack speed?",
                    "choices": [
                        {"text": "Berserker's Fury", "is_correct": False},
                        {"text": "Windtalker", "is_correct": True},
                        {"text": "Blade of Despair", "is_correct": False},
                        {"text": "Endless Battle", "is_correct": False},
                    ],
                    "hint": "This item is commonly used by marksmen.",
                    "explanation": "Windtalker grants additional attack speed and critical chance."
                },
                {
                    "text": "Question 6: Which hero can create a clone of themselves?",
                    "choices": [
                        {"text": "Aldous", "is_correct": False},
                        {"text": "Lancelot", "is_correct": False},
                        {"text": "Miya", "is_correct": False},
                        {"text": "Minsitthar", "is_correct": True},
                    ],
                    "hint": "This hero can confuse enemies with their clone.",
                    "explanation": "Minsitthar can create a clone of themselves to confuse enemies."
                },
                {
                    "text": "Question 7: What is the primary role of a support hero?",
                    "choices": [
                        {"text": "Tank", "is_correct": False},
                        {"text": "Damage dealer", "is_correct": False},
                        {"text": "Heal and assist allies", "is_correct": True},
                        {"text": "Crowd control", "is_correct": False},
                    ],
                    "hint": "These heroes help their teammates in various ways.",
                    "explanation": "Support heroes are designed to heal and assist their allies."
                },
                {
                    "text": "Question 8: Which hero is known for their ultimate ability 'Demon Hunter'?",
                    "choices": [
                        {"text": "Aldous", "is_correct": False},
                        {"text": "Kagura", "is_correct": False},
                        {"text": "Granger", "is_correct": True},
                        {"text": "Chou", "is_correct": False},
                    ],
                    "hint": "This hero is a marksman with high burst damage.",
                    "explanation": "Granger's ultimate ability 'Demon Hunter' allows him to deal massive damage to enemies."
                },
                {
                    "text": "Question 9: What is the role of a jungler in MLBB?",
                    "choices": [
                        {"text": "Farm jungle monsters and gank lanes", "is_correct": True},
                        {"text": "Stay in lane and farm minions", "is_correct": False},
                        {"text": "Support allies", "is_correct": False},
                        {"text": "Tank damage", "is_correct": False},
                    ],
                    "hint": "This role is crucial for gaining gold and experience.",
                    "explanation": "Junglers farm jungle monsters and gank lanes to help their teammates secure kills and objectives."
                },
                {
                    "text": "Question 10: Which item is essential for mages to increase their spell power?",
                    "choices": [
                        {"text": "Bloodlust Axe", "is_correct": False},
                        {"text": "Clock of Destiny", "is_correct": True},
                        {"text": "Blade of Despair", "is_correct": False},
                        {"text": "Holy Crystal", "is_correct": False},
                    ],
                    "hint": "This item provides both mana and spell power.",
                    "explanation": "Clock of Destiny is essential for mages as it increases their spell power and provides mana."
                },
            ],
            hard: [
                {
                    "text": "Question 1: Which hero has the ability 'Soul Resonance'?",
                    "choices": [
                        {"text": "Lunox", "is_correct": True},
                        {"text": "Kagura", "is_correct": False},
                        {"text": "Harith", "is_correct": False},
                        {"text": "Esmeralda", "is_correct": False},
                    ],
                    "hint": "This hero can switch between light and dark forms.",
                    "explanation": "Lunox has the ability 'Soul Resonance' in her dark form."
                },
                {
                    "text": "Question 2: What is the cooldown of the Retribution spell at max level?",
                    "choices": [
                        {"text": "30 seconds", "is_correct": False},
                        {"text": "45 seconds", "is_correct": False},
                        {"text": "20 seconds", "is_correct": True},
                        {"text": "60 seconds", "is_correct": False},
                    ],
                    "hint": "Retribution is used primarily by junglers.",
                    "explanation": "The cooldown of Retribution at max level is 20 seconds."
                },
                {
                    "text": "Question 3: Which hero can absorb damage with their ultimate ability?",
                    "choices": [
                        {"text": "Aldous", "is_correct": False},
                        {"text": "Gord", "is_correct": False},
                        {"text": "Leomord", "is_correct": True},
                        {"text": "Chou", "is_correct": False},
                    ],
                    "hint": "This hero can transform into a powerful mount.",
                    "explanation": "Leomord can absorb damage while mounted and deal significant damage."
                },
                {
                    "text": "Question 4: What is the primary role of a mage in MLBB?",
                    "choices": [
                        {"text": "Tank", "is_correct": False},
                        {"text": "Damage dealer with spells", "is_correct": True},
                        {"text": "Support", "is_correct": False},
                        {"text": "Crowd control", "is_correct": False},
                    ],
                    "hint": "These heroes deal damage using their abilities.",
                    "explanation": "Mages are primarily damage dealers who use spells to inflict damage."
                },
                {
                    "text": "Question 5: Which item is essential for tanks to increase their durability?",
                    "choices": [
                        {"text": "Oracle", "is_correct": True},
                        {"text": "Blade of Despair", "is_correct": False},
                        {"text": "Holy Crystal", "is_correct": False},
                        {"text": "Endless Battle", "is_correct": False},
                    ],
                    "hint": "This item provides health and magic resistance.",
                    "explanation": "Oracle is essential for tanks as it increases their durability and provides magic resistance."
                },
                {
                    "text": "Question 6: Which hero is known for their crowd control abilities?",
                    "choices": [
                        {"text": "Layla", "is_correct": False},
                        {"text": "Kagura", "is_correct": True},
                        {"text": "Miya", "is_correct": False},
                        {"text": "Fanny", "is_correct": False},
                    ],
                    "hint": "This hero can control the battlefield with her skills.",
                    "explanation": "Kagura has crowd control abilities that can disrupt enemy movements."
                },
                {
                    "text": "Question 7: What is the role of a marksman in MLBB?",
                    "choices": [
                        {"text": "Tank", "is_correct": False},
                        {"text": "Damage dealer", "is_correct": True},
                        {"text": "Support", "is_correct": False},
                        {"text": "Crowd control", "is_correct": False},
                    ],
                    "hint": "These heroes deal damage from a distance.",
                    "explanation": "Marksmen are ranged heroes that deal damage from a distance."
                },
                {
                    "text": "Question 8: Which hero can create a clone of themselves?",
                    "choices": [
                        {"text": "Aldous", "is_correct": False},
                        {"text": "Lancelot", "is_correct": False},
                        {"text": "Miya", "is_correct": False},
                        {"text": "Minsitthar", "is_correct": True},
                    ],
                    "hint": "This hero can confuse enemies with their clone.",
                    "explanation": "Minsitthar can create a clone of themselves to confuse enemies."
                },
                {
                    "text": "Question 9: What is the cooldown of the ultimate ability 'Flicker'?",
                    "choices": [
                        {"text": "120 seconds", "is_correct": True},
                        {"text": "90 seconds", "is_correct": False},
                        {"text": "60 seconds", "is_correct": False},
                        {"text": "150 seconds", "is_correct": False},
                    ],
                    "hint": "This ability allows heroes to reposition quickly.",
                    "explanation": "'Flicker' has a cooldown of 120 seconds, allowing heroes to escape or engage quickly."
                },
                {
                    "text": "Question 10: Which item is essential for assassins to increase their burst damage?",
                    "choices": [
                        {"text": "Bloodlust Axe", "is_correct": False},
                        {"text": "Blade of Despair", "is_correct": True},
                        {"text": "Clock of Destiny", "is_correct": False},
                        {"text": "Holy Crystal", "is_correct": False},
                    ],
                    "hint": "This item provides a significant boost to physical attack.",
                    "explanation": "Blade of Despair is essential for assassins as it increases their burst damage significantly."
                },
            ],
            extreme: [
                {
                    "text": "Question 1: Which hero can summon a giant mecha?",
                    "choices": [
                        {"text": "Johnson", "is_correct": False},
                        {"text": "X.Borg", "is_correct": True},
                        {"text": "Alpha", "is_correct": False},
                        {"text": "Granger", "is_correct": False},
                    ],
                    "hint": "This hero is a fighter with fire-based abilities.",
                    "explanation": "X.Borg can summon a giant mecha as part of his ultimate ability."
                },
                {
                    "text": "Question 2: What is the name of the item that reduces cooldowns?",
                    "choices": [
                        {"text": "Blade of Despair", "is_correct": False},
                        {"text": "Enchanted Talisman", "is_correct": True},
                        {"text": "Endless Battle", "is_correct": False},
                        {"text": "Thunder Belt", "is_correct": False},
                    ],
                    "hint": "This item is commonly used by mages and supports.",
                    "explanation": "Enchanted Talisman reduces cooldowns and provides mana regeneration."
                },
                {
                    "text": "Question 3: Which hero has the ability 'Tempest of Blades'?",
                    "choices": [
                        {"text": "Hayabusa", "is_correct": True},
                        {"text": "Lancelot", "is_correct": False},
                        {"text": "Gusion", "is_correct": False},
                        {"text": "Aldous", "is_correct": False},
                    ],
                    "hint": "This hero is an assassin known for high mobility.",
                    "explanation": "Hayabusa's ultimate ability 'Tempest of Blades' allows him to deal damage to multiple enemies."
                },
                {
                    "text": "Question 4: What is the primary role of a fighter in MLBB?",
                    "choices": [
                        {"text": "Tank", "is_correct": False},
                        {"text": "Damage dealer with durability", "is_correct": True},
                        {"text": "Support", "is_correct": False},
                        {"text": "Crowd control", "is_correct": False},
                    ],
                    "hint": "These heroes can deal damage while also taking hits.",
                    "explanation": "Fighters are versatile heroes that can deal damage while being durable."
                },
                {
                    "text": "Question 5: Which item grants lifesteal?",
                    "choices": [
                        {"text": "Bloodlust Axe", "is_correct": True},
                        {"text": "Blade of Despair", "is_correct": False},
                        {"text": "Holy Crystal", "is_correct": False},
                        {"text": "Oracle", "is_correct": False},
                    ],
                    "hint": "This item is essential for sustaining in fights.",
                    "explanation": "Bloodlust Axe grants lifesteal, allowing heroes to recover health from damage dealt."
                },
                {
                    "text": "Question 6: Which hero can manipulate time?",
                    "choices": [
                        {"text": "Harith", "is_correct": True},
                        {"text": "Lunox", "is_correct": False},
                        {"text": "Kagura", "is_correct": False},
                        {"text": "Gusion", "is_correct": False},
                    ],
                    "hint": "This hero can speed up or slow down time.",
                    "explanation": "Harith has the ability to manipulate time, allowing him to dodge attacks and reposition."
                },
                {
                    "text": "Question 7: What is the cooldown of the ultimate ability 'Demon Slayer'?",
                    "choices": [
                        {"text": "60 seconds", "is_correct": False},
                        {"text": "90 seconds", "is_correct": True},
                        {"text": "120 seconds", "is_correct": False},
                        {"text": "150 seconds", "is_correct": False},
                    ],
                    "hint": "This ability deals massive damage to a single target.",
                    "explanation": "'Demon Slayer' has a cooldown of 90 seconds, allowing Aldous to deal significant damage."
                },
                {
                    "text": "Question 8: Which item is essential for increasing magic power?",
                    "choices": [
                        {"text": "Clock of Destiny", "is_correct": True},
                        {"text": "Blade of Despair", "is_correct": False},
                        {"text": "Endless Battle", "is_correct": False},
                        {"text": "Oracle", "is_correct": False},
                    ],
                    "hint": "This item provides both mana and spell power.",
                    "explanation": "Clock of Destiny is essential for mages as it increases their spell power and provides mana."
                },
                {
                    "text": "Question 9: Which hero is known for their ability to heal themselves?",
                    "choices": [
                        {"text": "Aldous", "is_correct": False},
                        {"text": "Lunox", "is_correct": True},
                        {"text": "Kagura", "is_correct": False},
                        {"text": "Gord", "is_correct": False},
                    ],
                    "hint": "This hero can switch between light and dark forms.",
                    "explanation": "Lunox can heal herself using her abilities while switching forms."
                },
                {
                    "text": "Question 10: What is the primary objective of the Lord in MLBB?",
                    "choices": [
                        {"text": "Destroy turrets", "is_correct": False},
                        {"text": "Assist in pushing lanes", "is_correct": True},
                        {"text": "Kill enemy heroes", "is_correct": False},
                        {"text": "Collect gold", "is_correct": False},
                    ],
                    "hint": "This powerful monster can help turn the tide of battle.",
                    "explanation": "The Lord assists in pushing lanes and can help secure objectives for the team."
                },
            ]
        }

        # Add questions and choices to the quiz for each difficulty level
        for difficulty, questions in questions_data.items():
            quiz = Quiz.objects.create(
                title=f"MLBB Quiz - {difficulty.level}",
                category=mlbb_category,
                difficulty=difficulty
            )
            for question_data in questions:
                question = Question.objects.create(
                    quiz=quiz,
                    text=question_data["text"],
                    question_type="multiple_choice",
                    time_limit=30,  # Set time limit to 30 seconds for MLBB questions
                    hint=question_data.get("hint", "No hint available."),
                    explanation=question_data.get("explanation", "No explanation available.")
                )
                
                # Shuffle choices to randomize their order
                choices = question_data["choices"].copy()
                random.shuffle(choices)
                
                # Create the choices in the database
                for choice_data in choices:
                    Choice.objects.create(
                        question=question,
                        text=choice_data["text"],
                        is_correct=choice_data["is_correct"]
                    )
        
        self.stdout.write(self.style.SUCCESS('Successfully added MLBB quizzes with 10 questions for each difficulty level.'))