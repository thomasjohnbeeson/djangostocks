from django.shortcuts import render, redirect
from .models import Stock
from django.contrib import messages
from .forms import StockForm
from django import forms

def home(request):
    if request.method == "POST":
        ticker = request.POST["ticker"] #will get the symbol from the form

        import requests, json
        url = "https://cloud.iexapis.com/stable/stock/" + ticker + "/quote?token=pk_45817a824f534dc1856c3be2a7319283"
        api_req = requests.get(url)
        try:
            api_content = json.loads(api_req.content)
        except Exception as e:
            api_content = "Error..."

        return render(request, "home.html", {"api_content": api_content})

    else:
        return render(request, "home.html", {"ticker": "enter a ticker symbol above..."})




    # API key for iexcloud.io (financial information api): pk_45817a824f534dc1856c3be2a7319283
    import requests, json
    url = "https://cloud.iexapis.com/stable/stock/aapl/quote?token=pk_45817a824f534dc1856c3be2a7319283"
    api_req = requests.get(url)
    try:
        api_content = json.loads(api_req.content)
    except Exception as e:
        api_content = "Error..."

    return render(request, "home.html", {"api_content": api_content})


def about(request):
    return render(request, "about.html", {})

def add_stock(request):

    if request.method == "POST":
        form = StockForm(request.POST or None)

        if form.is_valid():
            form.save()
            messages.success(request, ("Stock has been added successfully!"))
            return redirect('add_stock')

        else:
            messages.success(request, ("There was an error..."))
            return redirect("home")
    else:
        ticker = Stock.objects.all()
        import requests, json

        output = []
        for ticker_item in ticker:
            url = "https://cloud.iexapis.com/stable/stock/" + str(ticker_item).lower() + "/quote?token=pk_45817a824f534dc1856c3be2a7319283"
            api_req = requests.get(url)
            try:
                api_content = json.loads(api_req.content)
                api_content.update({"ticker": ticker_item})
                output.append(api_content)
            except Exception as e:
                api_content = "Error..." 

        
        return render(request, "add_stock.html", {"ticker": ticker, "output":output})


def delete(request,stock_id):
    item = Stock.objects.get(pk=stock_id)
    item.delete()
    messages.success(request, ("Stock has been deleted successfully!"))
    return redirect("add_stock")





