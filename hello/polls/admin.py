from django.contrib import admin
from polls.models import Poll, Choice

class ChoiceInline(admin.TabularInline):
# class ChoiceInline(admin.StackedInline):
    model = Choice
    extra = 3

class PollAdmin(admin.ModelAdmin):
    list_display = ('question', 'pub_date', 'was_published_recently')
    list_filter = ['pub_date']
    search_fileds = ['question']
    date_hierarchy = 'pub_date'
    # fields = ['pub_date', 'question']
    fieldsets = [
        (None, {'fields': ['question']}),
        ('Date information', {'fields':['pub_date'], 'classes': ['collapse']}),
    ]
    inlines = [ChoiceInline]

admin.site.register(Poll, PollAdmin)
# admin.site.register(Choice, ChoiceInline)

