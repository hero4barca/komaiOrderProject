import copy
from django.shortcuts import render


from django.http import HttpResponse, HttpResponseRedirect
from .forms import CsvUploadForm
from orderDataApp.classes.update_database import UpdateDatabase

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
            return HttpResponseRedirect('/extract_data/')
    else:
        form = CsvUploadForm()
    return render(request, 'loadcsv.html', {'form': form})



def extract_data(request):
    
    
    try:
        order_data = request.session.get('order_data')
        summary = request.session.get('summary')
        err_msg = False
        seller_data_list =  make_seller_list(order_data)
    except Exception as err:
        err_msg = "Can't access data from sessions."
        order_data, summary, seller_data_list = None



    return render (request, 'extract_csv.html', {'err_msg':err_msg,
                                                  "summary": summary,
                                                  'seller_data_list': seller_data_list,
                                                  'order_data': order_data  
                                                  })

def show_data (request):
    return HttpResponse(request.session['order_data'])


def update_data (request):

    new_orders_num, new_sellers_num, new_orderitems_number = 0,0,0
    processed_rows_num = 0
    data_update_errors = []
    
    error = False
    error_msg = ""

    try:
        order_data = request.session.get('order_data')
        summary = request.session.get('summary')

        new_db_update = UpdateDatabase(order_data)
        new_db_update.update_data()
        data_update_errors = new_db_update.get_data_errors()
        new_orders_num, new_sellers_num, new_orderitems_number = new_db_update.get_number_of_new_records()
        processed_rows_num = new_db_update.get_number_of_row_processed()
    except Exception as err:
        error = True
        error_msg = str(err)
        #raise err # hide later
        #order_data, summary, seller_data_list = None

    return render (request, 'update_data.html', {"error": error,
                                                 "err_msg": error_msg,  
                                                  "data_update_errors": data_update_errors,
                                                   "new_orders": new_orders_num,
                                                   "new_sellers": new_sellers_num,
                                                   "new_orderitems": new_orderitems_number,
                                                   "rows_processed": processed_rows_num})






# ************** ordinary functions **************

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

 

    