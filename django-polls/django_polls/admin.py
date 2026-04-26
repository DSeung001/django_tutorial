from django.contrib import admin
from django_polls.models import Question, Choice

class ChoiceInline(admin.TabularInline):
    model = Choice
    # 추가 input 으로 표시 되는 Choice 개수
    extra = 3

class QuestionAdmin(admin.ModelAdmin):
    # fieldset 나 fields 값을 바꿔서 순서 지정 가능
    # fields = ["pub_date", "question_text"]
    fieldsets = [
        (None, {"fields": ["question_text"]}),
        ("Date information", {"fields": ["pub_date"]}),
    ]
    # inlines 로 `ForeignKey` 관계를 여러개 등록할 수 있습니다.
    inlines = [ChoiceInline]

    # Question 모델의 was_published_recently()도 포함 시킬 수 있음
    list_display = ["question_text", "pub_date", "was_published_recently"]

    list_filter = ["pub_date"]
    search_fields = ["question_text"]

# 모델과 admin_class 연결
admin.site.register(Question, QuestionAdmin)
