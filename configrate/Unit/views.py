from django.shortcuts import render

from django_datatables_view.base_datatable_view import BaseDatatableView
from django.utils.html import escape
from django.views.generic.edit import CreateView
from django.http import  JsonResponse, HttpResponse
from django.contrib.auth import authenticate
from django.contrib.auth import views as auth_views #new
from django.views import View

from configrate.models import Unit
from .forms import UnitForm
from django.urls import reverse
from django.core import serializers
from django.shortcuts import get_object_or_404
from django.http import QueryDict


class unit_item(CreateView):

    def get(self, request, *args, **kwargs):
        if 'id' in request.GET.keys():
            if request.GET.get('id'):
                data=Unit.objects.filter(pk=request.GET.get('id'))
                
                

                result={'status':1,'data':serializers.serialize('json',data)}
            else:
                result={'status':0,'data':''}
            return JsonResponse(result)
        else:
        
            Uni=Unit.objects.all()
            fileduse=UnitForm()
            context={
                "Unit":Uni,
                "filed":fileduse
            }
    
        return render(request, 'configrate/unit/unit_item.html',context)


    def post(self, request, *args, **kwargs):
        form = UnitForm(request.POST) 
        if request.POST.get('id'):
            data=get_object_or_404(Unit,pk=int(request.POST.get('id')))
            form=UnitForm(request.POST,instance=data)
        
        unit=''
        if form.is_valid():
            unit=form.save()


       

        if unit.id:
            context={
                    "status":1,
                    "message":"تم الحفظ"
                }
        else:
            context={
                    "status":0,
                    "message":"خطاء في الحفظ"
                }
        return JsonResponse(context)
        if form.is_valid():
            book = form.save()
            book.save()
            return HttpResponseRedirect(reverse_lazy('books:detail', args=[book.id]))
        return render(request, 'books/book-create.html', {'form': form})

    def delete(self, request,*args, **kwargs):
        pk=int(QueryDict(request.body).get('id'))
        if pk:
            try:
                data=get_object_or_404(Unit,pk=pk)
                data.delete()
                msg="تم الحذف"
                result={'status':1,'message':msg}
            except:
                msg="خطاء بالحذف"
                result={'status':0,'message':msg}
        else:
            msg="لا يوجد الصنف"
            result={'status':0,'message':msg}
        return JsonResponse(result)




class UnitJson(BaseDatatableView):
    # The model we're going to show
    model = Unit

    # define the columns that will be returned
    columns = [
    'id',
    "name_lo",
    "name_fk",
    "codeUnit",
    "action",

    ]

    # define column names that will be used in sorting
    # order is important and should be same as order of columns
    # displayed by datatables. For non-sortable columns use empty
    # value like ''
    order_columns = [
    'id',
    "name_lo",
    "name_fk",
    "codeUnit",
        "action",

    ]

    # set max limit of records returned, this is used to protect our site if someone tries to attack our site
    # and make it return huge amount of data
    max_display_length = 500
    count = 0
    def render_column(self, row, column):
        if column == "id":
            self.count += 1
            return self.count
        if column == "action":
            return '<a class="edit_row" data-url="{3}" data-id="{0}" style="DISPLAY: -webkit-inline-box;"  data-toggle="tooltip" title="{1}"><i class="fa fa-edit"></i></a><a class="delete_row" data-url="{3}" data-id="{0}"  style="    DISPLAY: -webkit-inline-box;"     data-toggle="tooltip" title="{2}"><i class="fa fa-trash"></i></a>'.format(row.pk,"Edit","Delete",reverse("unit"))
       
        else:
            # We want to render Unit as a custom column
            return super(UnitJson, self).render_column(row, column)

    def filter_queryset(self, qs):
        # use parameters passed in GET request to filter queryset

        # simple example:
        search = self.request.GET.get('search[value]', None)
        if search:
            qs = qs.filter(name__istartswith=search)

        # more advanced example using extra parameters
        filter_customer = self.request.GET.get('customer', None)

        if filter_customer:
            customer_parts = filter_customer.split(' ')
            qs_params = None
            for part in customer_parts:
                q = Q(customer_firstname__istartswith=part) | Q(customer_lastname__istartswith=part)
                qs_params = qs_params | q if qs_params else q
            qs = qs.filter(qs_params)
        return qs

