from django.contrib import admin

from .models import Form, Question, AnswerOption, FormResponse, QuestionResponse

admin.site.register(Form)
admin.site.register(Question)
admin.site.register(AnswerOption)
admin.site.register(FormResponse)
admin.site.register(QuestionResponse)
