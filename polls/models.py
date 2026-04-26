
import datetime
from django.db import models
from django.utils import timezone
from django.contrib import admin

class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')

    def __str__(self):
        return self.question_text

    # boolean=True이면 Django admin에서 아이콘(체크/엑스)으로 표시됨
    # ordering은 정렬 기준 필드, description은 목록 컬럼 헤더 텍스트
    @admin.display(boolean=True, ordering="pub_date", description="Published recently")
    def was_published_recently(self):
        """
            최근 글은 오늘 기준으로 하루 간격
        """
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now

class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.choice_text