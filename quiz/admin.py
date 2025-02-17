from django.contrib import admin
from .models import Quiz, Question, Choice, Result, Category, DifficultyLevel

class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 1
    min_num = 2  # Minimum required choices
    max_num = 5  # Maximum allowed choices
    fields = ['text', 'is_correct']
    ordering = ['id']

class QuestionInline(admin.TabularInline):
    model = Question
    extra = 1
    fields = ['text', 'question_type', 'time_limit']
    show_change_link = True

@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'difficulty', 'created_at', 'question_count')
    list_filter = ('category', 'difficulty', 'created_at')
    search_fields = ('title', 'category__name', 'difficulty__level')
    date_hierarchy = 'created_at'
    inlines = [QuestionInline]
    
    def question_count(self, obj):
        return obj.questions.count()
    question_count.short_description = 'Questions'

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('text', 'quiz', 'question_type', 'time_limit', 'has_hint')
    list_filter = ('quiz', 'question_type', 'time_limit')
    search_fields = ('text', 'quiz__title')
    autocomplete_fields = ['quiz']
    inlines = [ChoiceInline]
    fieldsets = (
        (None, {
            'fields': ('quiz', 'text', 'question_type', 'time_limit')
        }),
        ('Additional Help', {
            'classes': ('collapse',),
            'fields': ('hint', 'explanation'),
        }),
        ('Coding Question Settings', {
            'classes': ('collapse',),
            'fields': ('code_template', 'expected_output'),
        }),
    )
    
    def has_hint(self, obj):
        return bool(obj.hint)
    has_hint.boolean = True

@admin.register(Choice)
class ChoiceAdmin(admin.ModelAdmin):
    list_display = ('text', 'question', 'is_correct')
    list_filter = ('is_correct', 'question__quiz')
    search_fields = ('text', 'question__text')
    autocomplete_fields = ['question']

@admin.register(Result)
class ResultAdmin(admin.ModelAdmin):
    list_display = ('user', 'quiz', 'question', 'score', 'is_correct', 'taken_at')
    list_filter = ('quiz', 'user', 'is_correct')
    search_fields = ('user__username', 'quiz__title', 'question__text')
    readonly_fields = ('taken_at',)
    date_hierarchy = 'taken_at'
    fields = ('user', 'quiz', 'question', 'choice', 'user_answer_text', 
             'user_code_answer', 'is_correct', 'score', 'hint_used', 
             'explanation', 'taken_at')

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'quiz_count')
    search_fields = ('name',)
    
    def quiz_count(self, obj):
        return obj.quizzes.count()
    quiz_count.short_description = 'Quizzes'

@admin.register(DifficultyLevel)
class DifficultyLevelAdmin(admin.ModelAdmin):
    list_display = ('level', 'quiz_count')
    search_fields = ('level',)
    
    def quiz_count(self, obj):
        return obj.quizzes.count()
    quiz_count.short_description = 'Quizzes'

    actions = ['delete_selected']
    
    def delete_selected(self, request, queryset):
        # Prevent deletion if difficulty levels are in use
        for obj in queryset:
            if obj.quizzes.exists():
                self.message_user(request, f"Cannot delete {obj.level} - it's being used by quizzes", level='ERROR')
                return
        super().delete_selected(request, queryset)
    delete_selected.short_description = "Delete selected Difficulty Levels" 