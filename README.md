# django-modelview

## Goal
It is a parent view class that manages django models. With GET,POST,PUT and DELETE methods on it, you can query your tables or insert,update,delete data to table.

## Usage

Usage of this parent view is so easy.

```python
#Your views.py file

from .rest_modelview import DjangoModelView
from .models import Users

class UsersView(DjangoModelView):
    qset = Users.objects.all() #required, it is the datasource
    fetch_limit = 100 # optional, default 1000000
    
    #optional, maybe you want to override your methods or pass through a middleware
    def get(self,request,*args,**kwargs):
        #self.qset = self.qset.filter(owner_name="John Doe")
        print("Some operations before request")
        return super(UsersView,self).get(request,*args,**kwargs)
    
    #optional
    def post(self,request,*args,**kwargs):
        #if requset.user_not_authenticated_to_post: return JsonResponse({"err":"Not authenticated",status=403})
        print("Some operations before request")
        return super(UsersView,self).post(request,*args,**kwargs)
    
    #optional
    def delete(self,request,*args,**kwargs):
        #I have to prevent client getting classic internal server error
        try:
            print("Some operations before request")
            return super(UsersView,self).delete(request,*args,**kwargs)
        except:
            return JsonResponse({"err":"Something went wrong"},status=500)
```

```python
# Your urls.py file

from django.urls import path
from .views import UsersView

urlpatterns = [
    path('users', UsersView.as_view()),
    path('users/<int:pk>', UsersView.as_view()),
]
```

Thats all. Now you can call you endpoint.

```curl
Method:GET

URL:http://localhost:8000/users?fields=id,name,surname,car__brand&order=surname,-name&offset=0&limit=3&name__icontains=mu&id__gte=5&car__brand=BMW

Response:
{
    "total_records": 1,
    "offset": 0,
    "limit": 3,
    "data": [
        {
            "id": 9,
            "name": "Mustafa",
            "surname": "Mercanlı",
            "car__brand": "BMW"
        }
    ]
}
```
```curl
Method:GET (Only one record. Ex; its pkey is 9)

URL:http://localhost:8000/users/9

Response:
{
    "id": 9,
    "name": "Mustafa",
    "surname": "Mercanlı",
    "car_id": 1
}
```

```curl
Method:POST

URL:http://localhost:8000/users

Request body:
{
    "name":"John",
    "surname":"Doe"
}

Response:
{
    "id": 21,
    "name": "John",
    "surname": "Doe",
    "car_id": null
}

```

```curl
Method:PUT

URL:http://localhost:8000/users/21

Request body:
{
    "name":"John",
    "surname":"Smith"
}

Response:
{
    "id": 21,
    "name": "John",
    "surname": "Smith",
    "car_id": null
}

```

```curl
Method:DELETE

URL:http://localhost:8000/users/21

Response:
{
    "id": 21,
    "name": "John",
    "surname": "Smith",
    "car_id": null
}

```

## Additional
You have to set only a property named **qset**. This property bind your view and model. If you want you can override class methods (GET,POST..) so that you can do some logics before run the method or you can manipulate your output response.