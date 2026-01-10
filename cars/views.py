from django.shortcuts import render
from cars.models import Car, DealRequest
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from cars.forms import CarForm, DealRequestForm
from django.views.decorators.http import require_POST
from django.db import transaction

# Create your views here.

def cars_list(request):
    all_cars = Car.objects.filter(available=True)
    return render(request, 'cars_list.html', context={'all_cars': all_cars})

def car_detail(request, car_id):
    car_from_db = get_object_or_404(Car, pk=car_id)
    return render(request, 'car_detail.html', context={'car': car_from_db})

@login_required
def car_create(request):
    if not request.user.is_owner():
        return redirect('cars:cars_list')

    if request.method == 'POST':
        form = CarForm(request.POST, request.FILES)
        if form.is_valid():
            car = form.save(commit=False)
            car.owner = request.user
            car.save()
            return redirect('cars:car_detail', car_id=car.id)
    else:
        form = CarForm()
    return render(request, 'car_create.html', context={'form': form})

@login_required
def car_edit(request, car_id):
    car = get_object_or_404(Car, id=car_id, owner=request.user)

    if request.method == 'POST':
        form = CarForm(request.POST, request.FILES, instance=car)
        if form.is_valid():
            form.save()
            return redirect('cars:car_detail', car_id=car.id)
    else:
        form = CarForm(instance=car)
    return render(request, 'car_create.html', context={'form': form})

@login_required
def car_delete(request, car_id):
    car = get_object_or_404(Car, id=car_id, owner=request.user)

    if request.method == 'POST':
        car.delete()
        return redirect('cars:cars_list')

    return render(request, 'car_confirm_delete.html', context={'car': car})


@login_required
def send_deal_request(request, car_id):
    car = get_object_or_404(Car, id=car_id)

    if not request.user.is_seeker():
        return redirect('cars:car_detail', car_id=car_id)

    if request.method == 'POST':
        form = DealRequestForm(request.POST)
        if form.is_valid():
            deal_request = form.save(commit=False)
            deal_request.seeker = request.user
            deal_request.car = car
            deal_request.save()
            return redirect('cars:cars_list')
    else:
        form = DealRequestForm()

    return render(request,
                    'deal_request.html',
                      context={
                          'form': form,
                          'car': car
                      })

@login_required
def owner_deal_requests_list(request):
    if not request.user.is_owner():
        return redirect('cars:car_detail')

    all_requests = (DealRequest.objects
                    .select_related("car", "seeker")
                    .filter(car__owner=request.user))

    return render(request, 'owner_deal_requests.html',
                  context={'all_requests': all_requests})

@login_required
@require_POST
@transaction.atomic
def approve_deal_request(request, deal_request_id):
    deal_request = get_object_or_404(DealRequest,
                                     id=deal_request_id,
                                     car__owner=request.user,
                                     status=DealRequest.WAITING)

    deal_request.status = DealRequest.APPROVED
    deal_request.save()

    deal_request.car.available = False
    deal_request.car.save()

    return redirect('cars:owner_deal_requests_list')


@login_required
@require_POST
@transaction.atomic
def reject_deal_request(request, deal_request_id):
    deal_request = get_object_or_404(DealRequest,
                                     id=deal_request_id,
                                     car__owner=request.user,
                                     status=DealRequest.WAITING)

    deal_request.status = DealRequest.REJECTED
    deal_request.save()


    return redirect('cars:owner_deal_requests_list')

def statistics(request):
    total_cars = Car.cars_count()
    available_cars = Car.available_cars_count()
    sold_cars = Car.sold_cars_count()

    total_requests = DealRequest.requests_count()
    approved_requests = DealRequest.approved_requests_count()
    waiting_requests = DealRequest.waiting_requests_count()
    rejected_requests = DealRequest.rejected_requests_count()

    context = {
        'total_cars': total_cars,
        'available_cars': available_cars,
        'sold_cars': sold_cars,
        'total_requests': total_requests,
        'approved_requests': approved_requests,
        'waiting_requests': waiting_requests,
        'rejected_requests': rejected_requests,
    }

    return render(request, 'statistics.html', context)