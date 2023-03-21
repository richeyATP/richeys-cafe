from django.shortcuts import render
from django.views import View
from .models import MenuItem, OrderModel


class Index(View):
    def get(self, request, *arg, **kwargs):
        return render(request, 'customer/index.html')
    
class About(View):
    def get(self, request, *arg, **kwargs):
        return render(request, 'customer/about.html')
    
class Order(View):
    def get(self, request, *arg, **kwargs):
        # get all items from each category
        coffees = MenuItem.objects.filter(category__name__contains='Coffee')
        teas = MenuItem.objects.filter(category__name__contains='Tea')
        snacks = MenuItem.objects.filter(category__name__contains='Snack')
        
        # pass into context
        context = {
            'coffees': coffees,
            'teas': teas,
            'snacks': snacks, 
        }
    
        # render the template
        return render(request, 'customer/order.html', context)
    
    def post(self, request, *args, **kwargs):
        order_items = {
            'items': []
        }
        
        items = request.POST.getlist('items[]')

        for item in items:
            menu_item = MenuItem.objects.get(pk__contains=int(item))
            item_data = {
                'id': menu_item.pk,
                'name': menu_item.name,
                'price': menu_item.price
            }
        
            order_items['items'].append(item_data)
        
        price = 0
        item_ids = []
        
        for item in order_items['items']:
            price += item['price']
            item_ids.append(item['id'])
            
        order = OrderModel.objects.create(price=price)
        order.items.add(*item_ids)

        context = {
            'items': order_items['items'],
            'price': price
        }        
        
        return render(request, 'customer/order_confirmation.html', context)
        