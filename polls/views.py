from django.db.models import F
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils import timezone
from django.views import generic

from polls.models import Question, Choice

# Generic View를 상속
class IndexView(generic.ListView):
    # 각 Generic View 는 사용할 Template와 Model 명을 알아야합니다.
    # default로 template_name 은 <app name>/<model name>_detail.html를 표시
    # 내부적으로도 template_name을 사용해서 매핑해줌
    template_name = "polls/index.html"
    # context 변수의 이름을 변경
    context_object_name = "latest_question_list"

    # 목록으로 가져올 데이터 쿼리 오버라이딩
    def get_queryset(self):
        """
            발행일이 지난 글에서 최신 글을 가져옵니다.
        """
        return Question.objects.filter(pub_date__lte=timezone.now()).order_by("-pub_date")[:5]

class DetailView(generic.DetailView):
    model = Question
    template_name = "polls/detail.html"

    def get_queryset(self):
        """ 아직 발행이 지나지 않은 경우 제외"""
        return Question.objects.filter(pub_date__lte=timezone.now())

class ResultsView(generic.DetailView):
    model = Question
    template_name = "polls/results.html"

def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        # request로 요청 데이터 접근, reqeust.GET도 존재
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    # except로 2가지 예외 핸들링
    # - KeyError: 존재 하지 않는 키 접근
    # - Choice.DoesNotExist: Choice 데이터가 존재 하지 않는 경우
    except (KeyError, Choice.DoesNotExist):
        # 다시 detail로
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        # F로 DB에 저장된 모델 필드 값을 메모리 가져 오지 않고 직접 참조할 수 있게 해줌
        selected_choice.votes = F('votes') + 1
        selected_choice.save()
        #  POST 요청이 성공시, HttpResponseRedirect를 반환 해야 함
        #  reverse로 `URLconf`기반 url 생성 ex: "/polls/3/results/"
        return HttpResponseRedirect(reverse("polls:results", args=(question.id,)))