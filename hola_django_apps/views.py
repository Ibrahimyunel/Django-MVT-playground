from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.urls import reverse
import plotly.express as px

from .models import Film

def home(request):
    return render(request, 'home.html')

def main(request):
    film_list = Film.objects.all()
    context = {
        'title': 'Main Page',
        'film_list': film_list,
    }
    return render(request, 'hola/main.html', context)

def user_info(request):
    if request.method == 'GET':
        if request.session.get('username', False):
            userinfo = {
                'username': request.session['username'],
                'country': request.session['country'],
            }
        else:
            userinfo = False
        
        context = {
            'title': 'User Info Page',
            'userinfo': userinfo,
        }
        template = 'hola/user_info.html'
        return render(request, template, context)

def user_form(request):
    if request.method == 'GET':
        context = {'title': 'User Form Page'}
        template = 'hola/user_form.html'

        return render(request, template, context)
    
    elif request.method =='POST':
        username = request.POST.get('username')
        country = request.POST.get('country')
        request.session['username'] = username
        request.session['country'] = country

        return redirect(reverse('hola:user_info'))

def details(request, id, title):
    film = Film.objects.get(id=id)
    context = {
        'film': film,
    }
    return render(request, 'hola/details.html', context)


def get_data():
    df = px.data.gapminder()
    print(df)
    return df

def create_plot(df, year):
    fig = px.scatter(
        data_frame= df.query(f'year=={year}'),
        x= 'gdpPercap',
        y= 'lifeExp',
        color= 'continent',
        size= 'pop',
        height= 500,
        log_x= True,
        size_max= 60,
        hover_name="country"
    )
    fig = fig.to_html()
    return fig

def gapminder(request, year):
    df = get_data()
    fig = create_plot(df, year)
    context = {
        'plot': fig,
        'year': year,
    }
    template = 'gapminder.html'
    return render(request, template, context)