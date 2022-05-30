from django.shortcuts import render, redirect
from api import get_data, Busshift
import datetime


# principal view, with the busshifts
def index(request):
    return render(request, 'bs_planner/index.html', {'busshifts': get_data('busshift'), 'buses': get_data('fleet_bus'), 'drivers': get_data('fleet_driver'), 'busstops': get_data('geography_place')})


# function that deletes the busshift (in the db and on the view), when the button is clicked
def delete_bs(request):
    name = request.POST.get("name")
    busshift = Busshift(name, '', 0, [], datetime.time(0, 0, 0), datetime.time(0, 0, 0))
    busshift.delete()
    return redirect(index)

# function that adds the busshift to the db, when the form is filled
def add_bs(request):
    name = request.POST.get("name")
    bus = request.POST.get("bus")
    driver = request.POST.get("driver")
    busstops = request.POST.getlist("place")

    start_init = request.POST.get("start")
    h_start, m_start = start_init.split(":")
    start = datetime.time(int(h_start), int(m_start), 0)

    stop_init = request.POST.get("stop")
    h_stop, m_stop = stop_init.split(":")
    stop = datetime.time(int(h_stop), int(m_stop), 0)

    busshift = Busshift(name, bus, driver, busstops, start, stop)
    busshift.save()
    return redirect(index)
