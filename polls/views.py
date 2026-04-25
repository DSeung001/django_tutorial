from django.db.models import F
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.template import loader
from django.urls import reverse

from polls.models import Question, Choice


def index(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:5]

    # 튜플화
    context = {"latest_question_list": latest_question_list}

    # template + return을 render로 간략화 가능
    # template = loader.get_template('polls/index.html')
    # return HttpResponse(template.render(context, request))
    return render(request, 'polls/index.html', context)

def detail(request, question_id):
    # 아래 예외 처리를 다음 코드로 간략화 가능
    # try:
    #    question = Question.objects.get(pk=question_id)
    # except Question.DoesNotExist:
    #    raise Http404("Question does not exist")
    question = get_object_or_404(Question, pk=question_id)

    return render(request, 'polls/detail.html', {'question': question})

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

def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, "polls/results.html", {"question":question})