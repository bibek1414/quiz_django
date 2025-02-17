from django.contrib.auth.forms import UserCreationForm
from .forms import CustomUserCreationForm, QuizForm 
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Quiz, Choice, Result, User
from django.utils import timezone
from django.contrib.auth import login as auth_login
from django.urls import reverse
from django.core.paginator import Paginator
from django.db.models import Q
from datetime import datetime
from django.core.serializers.json import DjangoJSONEncoder
import json
from .models import Quiz, Category, DifficultyLevel
from django.db.models import Sum

def quiz_list(request):
    # Get the category from URL parameter, if provided
    category_filter = request.GET.get('category')
    
    # Get all categories for the navigation
    categories = Category.objects.all()
    
    if category_filter:
        # If category is selected, get quizzes for that category only
        category = get_object_or_404(Category, name=category_filter)
        quizzes = Quiz.objects.filter(category=category)
        difficulty_levels = DifficultyLevel.objects.filter(quizzes__category=category).distinct()
        
        # If difficulty is also specified, filter further
        difficulty_filter = request.GET.get('difficulty')
        if difficulty_filter:
            quizzes = quizzes.filter(difficulty__level=difficulty_filter)
    else:
        # If no category selected, group quizzes by category
        quizzes = None
        difficulty_levels = None
    
    context = {
        "categories": categories,
        "selected_category": category_filter,
        "quizzes": quizzes,
        "difficulty_levels": difficulty_levels,
        "selected_difficulty": request.GET.get('difficulty'),
    }
    return render(request, "quiz/quiz_list.html", context)

@login_required
def take_quiz(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)
    questions = list(quiz.questions.all())

    if not questions:
        messages.error(request, "This quiz has no questions.")
        return redirect('quiz_list')

    # Get the current question index from the URL, or default to 0
    current_question_index = int(request.GET.get('question', 0))

    # Validate the question index
    if current_question_index >= len(questions):
        return redirect('quiz_result', quiz_id=quiz_id)

    current_question = questions[current_question_index]

    # Check if this question was already answered
    existing_result = Result.objects.filter(
        user=request.user,
        quiz=quiz,
        question=current_question
    ).first()

    if request.method == "POST":
        is_hint_request = 'get_hint' in request.POST

        # Handle hint request
        if is_hint_request:
            # Generate hint if not already in database
            if not current_question.hint:
                choices = current_question.choices.all()
                current_question.hint = (current_question.text, choices)
                current_question.save()

            # Mark that the hint was used
            if existing_result:
                existing_result.hint_used = True
                existing_result.save()
            else:
                Result.objects.create(
                    user=request.user,
                    quiz=quiz,
                    question=current_question,
                    hint_used=True
                )

            # Redirect back to the same question with hint displayed
            return redirect(reverse('take_quiz', args=[quiz_id]) + f'?question={current_question_index}')

        # Handle answer submission
        if current_question.question_type in ['multiple_choice', 'true_false']:
            selected_choice_id = request.POST.get('selected_choice')
            if selected_choice_id:
                try:
                    selected_choice = Choice.objects.get(id=selected_choice_id)

                    # Create or update the result
                    Result.objects.update_or_create(
                        user=request.user,
                        quiz=quiz,
                        question=current_question,
                        defaults={
                            'choice': selected_choice,
                            'is_correct': selected_choice.is_correct,
                            'taken_at': timezone.now(),
                            'hint_used': existing_result.hint_used if existing_result else False
                        }
                    )
                except Choice.DoesNotExist:
                    messages.error(request, "Invalid choice selected.")

        elif current_question.question_type == 'fill_blank':
            user_answer = request.POST.get('fill_blank_answer', '').strip()
            if user_answer:
                # Create or update the result
                Result.objects.update_or_create(
                    user=request.user,
                    quiz=quiz,
                    question=current_question,
                    defaults={
                        'user_answer_text': user_answer,
                        'taken_at': timezone.now(),
                        'hint_used': existing_result.hint_used if existing_result else False
                    }
                )

        elif current_question.question_type == 'coding':
            user_code = request.POST.get('code_answer', '').strip()
            if user_code:
                # Create or update the result
                Result.objects.update_or_create(
                    user=request.user,
                    quiz=quiz,
                    question=current_question,
                    defaults={
                        'user_code_answer': user_code,
                        'taken_at': timezone.now(),
                        'hint_used': existing_result.hint_used if existing_result else False
                    }
                )

        # Move to next question
        next_question_index = current_question_index + 1
        if next_question_index < len(questions):
            return redirect(reverse('take_quiz', args=[quiz_id]) + f'?question={next_question_index}')
        else:
            return redirect('quiz_result', quiz_id=quiz_id)

    time_limit = current_question.time_limit

    # Generate explanation if not already in database
    if current_question.question_type in ['multiple_choice', 'true_false'] and not current_question.explanation:
        correct_choice = current_question.choices.filter(is_correct=True).first()
        if correct_choice:
            current_question.explanation = (current_question.text, correct_choice.text)
            current_question.save()

    context = {
        "quiz": quiz,
        "question": current_question,
        "current_question_index": current_question_index,
        "total_questions": len(questions),
        "time_limit": time_limit,
        "existing_answer": existing_result.choice if existing_result and existing_result.choice else None,
        "existing_text_answer": existing_result.user_answer_text if existing_result else None,
        "existing_code_answer": existing_result.user_code_answer if existing_result else None,
        "hint_used": existing_result.hint_used if existing_result else False
    }

    return render(request, "quiz/take_quiz.html", context)

@login_required
def quiz_result(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)

    # Get all results for this user and quiz
    results = Result.objects.filter(
        user=request.user,
        quiz=quiz
    ).select_related('question', 'choice')

    # Calculate total score
    total_correct = results.filter(is_correct=True).count()
    total_questions = quiz.questions.count()

    # Ensure the user has actually taken the quiz
    if not results:
        messages.warning(request, "You haven't completed this quiz yet.")
        return redirect('take_quiz', quiz_id=quiz_id)

    # Prepare data for each question type
    for result in results:
        # For multiple choice and true/false
        if result.question.question_type in ['multiple_choice', 'true_false']:
            result.correct_answer = result.question.choices.filter(is_correct=True).first()

        # For fill-in-the-blank
        elif result.question.question_type == 'fill_blank':
            result.correct_answer = result.question.choices.filter(is_correct=True).first()

        # For coding questions
        elif result.question.question_type == 'coding':
            result.expected_output = result.question.expected_output

    context = {
        'quiz': quiz,
        'results': results,
        'result': total_correct,  # The score
        'total_questions': total_questions,
    }

    return render(request, 'quiz/quiz_result.html', context)


def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.is_active = True
            user.save()
            auth_login(request, user)
            messages.success(request, "Your account has been created! You are now logged in.")
            return redirect("quiz_list")
    else:
        form = CustomUserCreationForm()
    return render(request, "registration/register.html", {"form": form})
@login_required
def quiz_history(request):
    # Fetch all results for the logged-in user, ordered by taken_at in descending order
    results = Result.objects.filter(user=request.user).select_related('quiz', 'question', 'choice').order_by('-taken_at')

    # Filter by quiz title
    quiz_filter = request.GET.get('quiz')
    if quiz_filter:
        results = results.filter(quiz__title__icontains=quiz_filter)

    # Filter by date
    date_filter = request.GET.get('date')
    if date_filter:
        try:
            filter_date = datetime.strptime(date_filter, '%Y-%m-%d').date()
            results = results.filter(taken_at__date=filter_date)
        except ValueError:
            pass

    # Organize results by quiz and then by attempt
    quizzes = {}
    for result in results:
        quiz_key = result.quiz.id  # Group by quiz
        if quiz_key not in quizzes:
            quizzes[quiz_key] = {
                'quiz': result.quiz,
                'attempts': [],
            }

        # Find or create the attempt for this quiz and taken_at timestamp
        attempt_key = result.taken_at
        attempt = next((a for a in quizzes[quiz_key]['attempts'] if a['taken_at'] == attempt_key), None)
        if not attempt:
            attempt = {
                'taken_at': result.taken_at,
                'results': [],
                'correct_count': 0,
                'incorrect_count': 0,
            }
            quizzes[quiz_key]['attempts'].append(attempt)

        # Add the result to the attempt
        attempt['results'].append(result)
        if result.is_correct:
            attempt['correct_count'] += 1
        else:
            attempt['incorrect_count'] += 1

    # Sort attempts within each quiz by taken_at in descending order
    for quiz_data in quizzes.values():
        quiz_data['attempts'].sort(key=lambda x: x['taken_at'], reverse=True)

    # Convert quizzes dictionary to a list for pagination
    quiz_list = list(quizzes.values())

    # Paginate quizzes (10 per page)
    paginator = Paginator(quiz_list, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Prepare data for the chart (all results)
    all_quiz_titles = [quiz['quiz'].title for quiz in quiz_list]  # Extract quiz titles
    all_correct_counts = [sum(a['correct_count'] for a in quiz['attempts']) for quiz in quiz_list]
    all_incorrect_counts = [sum(a['incorrect_count'] for a in quiz['attempts']) for quiz in quiz_list]

    # Serialize data for JavaScript
    quiz_titles_json = json.dumps(all_quiz_titles, cls=DjangoJSONEncoder)
    correct_counts_json = json.dumps(all_correct_counts, cls=DjangoJSONEncoder)
    incorrect_counts_json = json.dumps(all_incorrect_counts, cls=DjangoJSONEncoder)

    context = {
        'quizzes': page_obj,  # Pass the paginated quizzes to the template
        'page_obj': page_obj,
        'quiz_titles': quiz_titles_json,
        'correct_counts': correct_counts_json,
        'incorrect_counts': incorrect_counts_json,
    }
    return render(request, 'quiz/quiz_history.html', context)


def leaderboard(request):
    
    leaderboard_data = User.objects.annotate(
        total_score=Sum('result__score')
    ).order_by('-total_score')[:10]  

    context = {
        'leaderboard': leaderboard_data
    }
    return render(request, 'quiz/leaderboard.html', context)

