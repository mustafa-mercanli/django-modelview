from json import JSONDecoder
from .rest_modelview import DjangoModelView
from django.http import HttpResponse,JsonResponse
from .models import Users
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator


def ping(request):

    return HttpResponse("ACK/Pong")

@method_decorator(csrf_exempt, name='dispatch')
class UsersView(DjangoModelView):
    qset = Users.objects.all() #required, it is the datasource
    fetch_limit = 100 # optional, default 1000000

    def get(self,request,*args,**kwargs):
        #self.qset = self.qset.filter(owner_name="John Doe")
        print("Some operations before request")
        return super(UsersView,self).get(request,*args,**kwargs)
    
    def post(self,request,*args,**kwargs):
        #if requset.user_not_authenticated_to_post: return JsonResponse({"err":"Not authenticated",status=403})
        print("Some operations before request")
        return super(UsersView,self).post(request,*args,**kwargs)

    def delete(self,request,*args,**kwargs):
        #I have to prevent client getting classic internal server error
        try:
            print("Some operations before request")
            return super(UsersView,self).delete(request,*args,**kwargs)
        except:
            return JsonResponse({"err":"Something went wrong"},status=500)
