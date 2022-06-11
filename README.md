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
Let's look at the query keywords above. 
* **fields** keyword is for specifying which model fields you deserved to fetch. If not set, it means all fields.
* **order** keyword is how do you want to order the queryset. Ex; -name,surname means name descending and surname ascending together.
* **offset and limit** keyword is used to slice data into the pieces. It means paginating.
* Except the keywords above, whole statement in url query used to queryset filter. You can use all django queryset filtering keywords in this part.

Note: You can use | operator in querystring. Ex: name=John & surname__icontains=smi | car_id=1

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

The source codes has also includes a simple db handler middleware. If you use multiple db in you environment, you can set a **_db="sample_db"** property your model. It means when you query on this model, sample_db connection will be used.


```python
#Your multidb_middleware.py file
class DBRouter:
    def db_for_read(self,model,**hints):
        return getattr(model,"_db","default")
    
    def db_for_write(Self,model,**hints):
        return getattr(model,"_db","default")

    def allow_relation(self,a,b,**hints):
        return True
    
    def allow_migrate(self,a,b,**hints):
        return True
```

```
#Your settings.py file
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    },
    'pgsql' : {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'postgres',
        'HOST': '127.0.0.1',
        'PORT': '5432',
        'USER': 'postgres',
        'PASSWORD': '*****'
    }
}

DATABASE_ROUTERS=["django_modelview.multidb_middleware.DBRouter"]
```

```
#Your models.py file
DATABASE_ROUTERS=["django_modelview.multidb_middleware.DBRouter"]

class Users(models.Model):
    name = models.CharField(max_length=128, blank=True, null=True)
    surname = models.CharField(max_length=128, blank=True, null=True)
    car = models.ForeignKey("Cars",on_delete=models.CASCADE,null=True)

    _db = "pgsql"

    class Meta:
        db_table = 'users'
```