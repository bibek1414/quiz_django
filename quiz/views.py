from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Quiz, Question, Choice, Result
from django.utils import timezone
from django.contrib.auth import login as auth_login
from django.urls import reverse


def quiz_list(request):
    quizzes = Quiz.objects.all()
    return render(request, "quiz/quiz_list.html", {"quizzes": quizzes})

@login_required
def take_quiz(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)
    questions = list(quiz.questions.all())  # Convert to list to ensure indexing works
    
    if not questions:
        messages.error(request, "This quiz has no questions.")
        return redirect('quiz_list')

    # Get the current question index from the URL, or default to 0
    current_question_index = int(request.GET.get('question', 0))
    
    # Validate the question index
    if current_question_index >= len(questions):
        return redirect('quiz_result', quiz_id=quiz_id)

    if request.method == "POST":
        current_question = questions[current_question_index]
        selected_choice_id = request.POST.get('selected_choice')  # Ensure this matches the hidden input name
        
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
                        'taken_at': timezone.now()
                    }
                )
            except Choice.DoesNotExist:
                messages.error(request, "Invalid choice selected.")
        
        # Move to next question
        next_question_index = current_question_index + 1
        if next_question_index < len(questions):
            return redirect(reverse('take_quiz', args=[quiz_id]) + f'?question={next_question_index}')
        else:
            return redirect('quiz_result', quiz_id=quiz_id)

    current_question = questions[current_question_index]
    time_limit = current_question.time_limit

    # Check if this question was already answered
    existing_result = Result.objects.filter(
        user=request.user,
        quiz=quiz,
        question=current_question
    ).first()

    context = {
        "quiz": quiz,
        "question": current_question,
        "current_question_index": current_question_index,
        "total_questions": len(questions),
        "time_limit": time_limit,
        "existing_answer": existing_result.choice if existing_result else None
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

    # Add correct answer to each result
    for result in results:
        # Fetch the correct answer for the question
        result.correct_answer = result.question.choices.filter(is_correct=True).first()

    context = {
        'quiz': quiz,
        'results': results,
        'result': total_correct,  # The score
        'total_questions': total_questions,
    }
    
    return render(request, 'quiz/quiz_result.html', context)

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.is_active = True
            user.save()
            auth_login(request, user)
            messages.success(request, "Your account has been created! You are now logged in.")
            return redirect("quiz_list")
    else:
        form = UserCreationForm()
    return render(request, "registration/register.html", {"form": form})