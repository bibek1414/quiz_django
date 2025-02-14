from django.contrib import admin
from .models import Quiz, Question, Choice, Result

# Inline model to add choices directly from the Question admin page
class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 3  # How many empty choices to show by default

# Customizing the Question admin panel to display the new time_limit field
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('text', 'quiz', 'time_limit')  # Show the time_limit on the question list page
    search_fields = ('text',)  # Search by question text
    list_filter = ('quiz',)  # Filter by quiz
    inlines = [ChoiceInline]  # Add choices inline with questions


# Register models with the admin site
admin.site.register(Quiz)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Choice)
admin.site.register(Result)
