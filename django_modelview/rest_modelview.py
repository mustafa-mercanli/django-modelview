from django.http import JsonResponse
from django.views.generic import View
import json

class DjangoModelView(View):
    qset = None
    fetch_limit = 1000000

    def fixer(self,val):
        mapping = {"true":True,"True":True,"false":False,"False":False,"null":None,"Null":None}
        return mapping.get(val,val)

    def get(self,request,*args,**kwargs):
        querystring = request.GET.dict()
        
        limit = int(querystring.pop('limit',self.fetch_limit))
        try:
            assert not limit > self.fetch_limit
        except:
            return JsonResponse({"err":"Limit cannot be greater than %s" % self.fetch_limit},status=400)
        
        offset = int(querystring.pop('offset',0))

        fields = querystring.pop('fields',None) 
        fields = fields.split(",") if fields else []
        
        order = querystring.pop('order',None)
        order = order.split(",") if order else []

        self.qset = self.qset.filter(**querystring).values(*fields)

        if kwargs.get("pk"):
            for row in self.qset.filter(pk=kwargs.get("pk")):
                resp = row
                break
            else:
                return JsonResponse({"err":"Record with %s not found: %s" % ("pk",kwargs.get("pk"))},status=404)
            
        else:
            total_records = self.qset.count()
            data = list(self.qset.order_by(*order)[offset:offset+limit])

            resp = {"total_records":total_records,"offset":offset,"limit":limit,"data":data}

        return JsonResponse(resp,safe=False)


    def post(self,request,*args,**kwargs):
        try:
            body = json.loads(request.body)
            assert not type(body) == list
        except:
            body = {}

        for key in body.keys():
            body[key] = self.fixer(body[key])

        record = self.qset.model(**body)
        record.save()
        
        for row in list(self.qset.filter(pk=record.pk).values()):
            data = row
            break
        else:
            row = {}
        
        return JsonResponse(data,safe=False)
    
    def put(self,request,*args,**kwargs):
        try:
            body = json.loads(request.body)
            assert not type(body) == list
        except:
            body = {}

        try:
            record = self.qset.get(pk=kwargs.get("pk"))
        except self.qset.model.DoesNotExist:
            return JsonResponse({"err":"Record with %s not found: %s" % ("pk",kwargs.get("pk"))},status=404)
        
        for key in body.keys():
            setattr(record,key,self.fixer(body[key]))
        
        record.save()
        
        for row in list(self.qset.filter(pk=record.pk).values()):
            data = row
            break
        else:
            return JsonResponse({"err":"Record with %s not found: %s" % ("pk",kwargs.get("pk"))},status=404)
        
        return JsonResponse(data,safe=False)
    
    def patch(self,request,*args,**kwargs):
        return self.put(request,*args,**kwargs)
    

    def delete(self,request,*args,**kwargs):
        for record in self.qset.filter(pk=kwargs.get("pk")).values():
            record = record
            break
        else:
            return JsonResponse({"err":"Record with %s not found: %s" % ("pk",kwargs.get("pk"))},status=404)

        self.qset.filter(pk=kwargs.get('pk')).delete()

        return JsonResponse(record,safe=False)

        