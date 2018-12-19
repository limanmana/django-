from django.shortcuts import render,get_object_or_404
from django.http import HttpResponse,Http404,HttpResponseRedirect
from .models import Question,Choice
from django.template import loader
from django.shortcuts import render
from django.urls import reverse  # 类似前端模板语言 url 函数
from django.views import generic  # 从数据库取数据前台渲染列表
# Create your views here.
# def index(request):
#     return HttpResponse("""
#         <html>
#             <head>
#             </head>
#             <body>
#                 <h1>hello world</h1>
#             </body>
#         </html>
#     """)
# def index(request):
#     """
#     展示问题列表
#
#     :return:
#     """
#     question_list = Question.objects.all().order_by('-pub_date')[0:5]
#
#     # print(question_list)
#     # output = ''
#     # for q in question_list:
#     #     print(q.id, q.question_text,q.pub_date)
#     #     output = output + q.question_text + ','
#     #     print(output)
#     # output = ','.join([q.question_text for q in question_list])
#     template = loader.get_template('polls/index.html')
#
#     context = {
#         'question_list':question_list
#     }
#
#
#     return HttpResponse(template.render(context,request))




def index(request):
    question_list = Question.objects.order_by('-pub_date')[0:5]
    context = {
        'question_list':question_list
    }
    return render(request,'polls/index.html',context)
def detail(request,question_id):
    """
    显示一个问题的详细信息，问题内容、问题发布时间、选项内容、每个选项投票数。

    """
    try:
        question = Question.objects.get(id=question_id)
        # (基本思想)choices = Choice.objects.filter(question_id=question.id)
        # choices = question.choice_set.all()
        # 由于前端模板语言本质是后端代码，可以把上句话放到html页面中写
    except Question.DoesNotExist:
        raise Http404("出错了，次id不存在 404")
    context = {
        'question':question,

    }
    return render(request, 'polls/detail.html', context)
    # 写法2
    # question - Question.objects.filter(id=question_id)
    # if not question:
    #     raise Http404()

    # 写法3
    # question = get_object_or_404(Question,id=question_id)
    # return render(request,'polls/detail.html',{'question':question})

def results(request,question_id):
    """
    投票结果

    """
    question = Question.objects.get(id=question_id)
    return render(request,'polls/results.html',{'question':question})

def vote(request,question_id):
    """
    投票
    """
    try:
        question = Question.objects.get(id=question_id)
        choices = question.choice_set.all()
        choice_id = request.POST['choice']
        selected_choice = question.choice_set.get(id=choice_id)
    except Question.DoesNotExist as e:
        error_message = '问题不存在'
    except Choice.DoesNotExist as e:
        error_message = '问题对应选项不存在'
        return render(request,'polls/detail.html',context={'question':question,'error_message':error_message})
    else:
        selected_choice.votes += 1
        selected_choice.save()
        return HttpResponseRedirect(reverse('polls:results',args=(question_id,)))


# 通用模板示例，跟 def index 类比着看。 比较适合单调的增删改查。
class SimpleView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'question_list'

    def get_queryset(self):
        return Question.objects.all()














