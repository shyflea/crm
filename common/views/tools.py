from django.http import HttpResponse
from django.utils.decorators import classonlymethod

from common.utils import trans_to_pingyin


# 汉字转拼英
def pingyin(request):
    content = trans_to_pingyin(request.GET['chinese'])
    return HttpResponse(content)


