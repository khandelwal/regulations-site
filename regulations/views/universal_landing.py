from django.http import HttpResponse
from django.template import RequestContext
from django.template.loader import select_template

def universal(request):
   context = {'greeting':'hello'} 
   c = RequestContext(request, context)
   t = select_template(['regulations/universal.html'])
   return HttpResponse(t.render(c))
