from django.shortcuts import render
from django.views import View
from django.http import Http404, HttpResponseNotFound, HttpResponseServerError
from tours.data import title, subtitle, departures, description, tours
from  random import sample


# Create your views here.
def custom_handler404(request, exception):
    return HttpResponseNotFound('<h1>Ой, что то сломалось... Простите извините! Ошибка: 404</h1>')


def custom_handler500(request):
    return HttpResponseServerError('<h1>Ой, что то сломалось... Простите извините! Ошибка: 500</h1>')


class MainView(View):
    def get(self, request, *args, **kwargs):
        context = {
            'tours': sample(tours.items(), 6),
            'departures': departures.items(),
            'title': title,
            'subtitle': subtitle,
            'description': description,
        }

        return render(request, 'index.html', context=context)


class DepartureView(View):
    def get(self, request, departure, *args, **kwargs):
        if departure not in departures.keys():
            raise Http404
        context = {
            'tours': [tour for tour in tours.items() if tour[1]["departure"] == departure],
            'departureChosed': departures[departure],
            'departures': departures.items(),
            'title': title
        }

        context['tourslen'] = len(context['tours'])
        priceAndNights = [tour[1]['price'] for tour in context['tours']]
        context['maxprice'] = max(priceAndNights)
        context['minprice'] = min(priceAndNights)
        priceAndNights = [tour[1]['nights'] for tour in context['tours']]
        context['maxnights'] = max(priceAndNights)
        context['minnights'] = min(priceAndNights)

        return render(request, 'departure.html', context=context)


class TourView(View):
    def get(self, request, id, *args, **kwargs):
        if id not in tours:
            raise Http404
        context = {
            'title': title,
            'tour': tours[id],
            'departureChosed': departures[tours[id]['departure']],
            'departures': departures.items()
        }
        return render(request, 'tour.html', context=context)
