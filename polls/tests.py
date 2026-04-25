import datetime

from django.test import TestCase
from django.utils import timezone
from django.urls import reverse

from polls.models import Question

class QuestionModelTest(TestCase):
    def test_was_published_recently_with_future_questions(self):
        """
        python Docstring으로 Django 관례에서는 여기에 함수나 클래스 설명이 위치함
        was_published_recently()는 pub_date가 긴 미래일 경우 false를 반환
        """
        time = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(pub_date=time)
        self.assertIs(future_question.was_published_recently(), False)

    def test_was_published_recently_with_old_questions(self):
        """
            1일보다 오래된 질문에는 false를 반환
        """
        time = timezone.now() - datetime.timedelta(days=1)
        old_question = Question(pub_date=time)

        self.assertIs(old_question.was_published_recently(), False)

    def test_was_published_recently_with_recent_questions(self):
        """
            1일 이내인 질문은 True를 반환
        """
        time = timezone.now() - datetime.timedelta(hours=23, minutes=59, seconds=59)
        recent_question = Question(pub_date=time)

        self.assertIs(recent_question.was_published_recently(), True)

def create_question(question_text, days):
    """ 질문 생성 함수 """
    time = timezone.now() + datetime.timedelta(days=days)
    return Question.objects.create(question_text=question_text, pub_date=time)

class QuestionIndexViewTests(TestCase):
    def test_no_questions(self):
        """질문이 없는 경우"""
        response = self.client.get(reverse('polls:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No polls are available")
        self.assertQuerySetEqual(response.context['latest_question_list'], [])

    def test_past_questions(self):
        """pub_date가 지난 글은 보이는지"""
        question = create_question("Past question", days=-30)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerySetEqual(response.context['latest_question_list'], [question])

    def test_future_questions(self):
        """pub_date가 안지난 미래글은 안 보이는지"""
        create_question("Future question", days=30)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerySetEqual(response.context['latest_question_list'], [])

    def test_future_question_and_past_question(self):
        """pub_date가 지난거랑 안 지난거 있을 경우"""
        question = create_question("Past question", days=-30)
        create_question("Future question", days=30)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerySetEqual(response.context['latest_question_list'], [question])

    def test_two_past_questions(self):
        """표시해야할 question이 복수개 이상"""
        question1 = create_question("Past question 1", days=-30)
        question2 = create_question("Past question 2", days=-5)
        response = self.client.get(reverse('polls:index'))
        # 정렬 순서 맞춰서 question2가 . 최신글
        self.assertQuerySetEqual(response.context['latest_question_list'], [question2, question1])


class QuestionDetailViewTests(TestCase):
    def test_future_question(self):
        """pub_date가 지나지 않은 건 404로 표시되어야 합니다."""
        future_question = create_question("Future question", days=5)
        url = reverse('polls:detail', args=(future_question.pk,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_past_question(self):
        """pub_date가 지나면 표시"""
        past_question = create_question("Past question", days=-5)
        url = reverse('polls:detail', args=(past_question.pk,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, past_question.question_text)
