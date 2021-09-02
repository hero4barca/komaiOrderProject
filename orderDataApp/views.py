import copy
from django.shortcuts import render


from django.http import HttpResponse, HttpResponseRedirect
from .forms import CsvUploadForm

def home(request):
    return render (request, 'home.html')



def upload_csv_file(request):
    if request.method == 'POST':
        form =  CsvUploadForm(request.POST, request.FILES)
        if form.is_valid():
            

            form_data = form.cleaned_data
            request.session['order_data'] = form_data.get("order_data")
            request.session['summary'] = form_data.get("summary")
            
            # @TODO: save copy of uploaded file 
            # process the csv file into database here

            # return HttpResponse(request.FILES['csv_file'])
            #handle_uploaded_file(request.FILES['file'])
            return HttpResponseRedirect('/update_data/')
    else:
        form = CsvUploadForm()
    return render(request, 'loadcsv.html', {'form': form})



def update_data(request):
    
    
    try:
        order_data = request.session.get('order_data')
        summary = request.session.get('summary')
        err_msg = False
        seller_data_list =  make_seller_list(order_data)
    except Exception as err:
        err_msg = "Can't access data from sessions."
        order_data, summary, seller_data_list = None



    return render (request, 'process_csv.html', {'err_msg':err_msg,
                                                  "summary": summary,
                                                  'seller_data_list': seller_data_list,
                                                  'order_data': order_data  
                                                  })

def show_data (request):
    return HttpResponse(request.session['order_data'])


# ************** ordinary method calls **************

def make_seller_list(order_data):
    
    seller_data_list = []
    
    
    for row in order_data: # looping through orders
        
        new_order_items_list = row["order_items"] # list of order items

        for item in new_order_items_list:  # looping through single items
            new_seller_data = item["seller"] # retrieve seller data for each item -> current seller data
            seller_unique = True

            for seller_data in seller_data_list: # looping through stored seller data
                if seller_data == new_seller_data: # 
                    seller_unique = False # false 

            if seller_unique: # if unique  
                seller_data_list.append(copy.deepcopy(new_seller_data))

    #assert False
    return seller_data_list        

    