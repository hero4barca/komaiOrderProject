import datetime

class UpdateDatabase:

    def __init__(self, order_data):

        self.order_data = order_data


    def update_db(self):

        for row in self.order_data:

            new_order, error, error_list =self.create_order(row) 


    def create_order(self, row):

        order_dict = {}
        error = False
        error_list = []

    

        order_dict["order_number"] = row["Order Number"]

        # convert date string to datetime obj
        try:
            order_datetime = datetime.datetime.strptime(row["Order Date"], "%Y-%m-%d %H:%M:%S" )
            order_date = order_datetime.date()
            order_time = order_datetime.time()
        except:
            order_date, order_time = None # assign none to date and time 
            
            error = True

            datetime_conversion_err_str = "Couldn't convert for order -> %s" % order_dict["order_number"] # detailerror in error list
            error_list.append(datetime_conversion_err_str)
        
        # assign date,time to dict        
        order_dict["order_date"] = order_date 
        order_time["order_time"] = order_time


        order_dict["customer_uid"] = row["Customer Uid"]
        order_dict["customer_name"] = row["Customer Name"]
        order_dict["customer_email"] = row["Customer Email"]

        order_dict["billing_name"] = row["Bill To Name"]
        order_dict["billing_address"] = row["Bill To Address"]
        order_dict["billing_district"] = row["Bill To District"]
        order_dict["billing_state"] = row["Bill To State"]
        order_dict["billing_zip_code"] = row["Bill To Zip"]
        order_dict["billing_country"] = row["Bill To Country"]
        order_dict["billing_phone_No"] = row["Bill To Mobile"]

        order_dict["shipping_name"]  = row["Ship To Name"]
        order_dict["shipping_address"]  = row["Ship To Address"]
        order_dict["shipping_district"]  = row["Ship To District"]
        order_dict["shipping_state"]  = row["Ship To State"]
        order_dict["shipping_zip_code"]  = row["Ship To Zip"]
        order_dict["shipping_country"]  = row["Ship To Country"]
        order_dict["shipping_phone_No"]  = row["Ship To Mobile"]


        order_dict["order_currency"]  = row["Order Currency"]
        order_dict["order_total"]  = row["Order Total"]
        order_dict["order_taxes"]  = row["'Order Taxes"]
        order_dict["order_discounts"]  = row["Order Discounts"]
        order_dict["order_subtotal"]  = row["'Order Subtotal"]

        # cast all to decimal
        order_dict["order_shipping_cost"]  = row["Order Shipping"]
        order_dict["order_ship_TBD"]  = row["Order Ship Tbd"]
        order_dict["order_cart_total"]  = row["Order Cart Total"]
        order_dict["order_cart_taxes"]  = row["Order Cart Taxes"]
        order_dict["order_cart_discount"]  = row["Order Cart Discounts"]
        order_dict["order_grand_total"]  = row["'Order Grand Total"]
        order_dict["order_coupon_value"]  = row["Order Coupon Value"]
        order_dict["payment_fee"]  = row["Payment Fee"]
        order_dict["payment_amount"]  = row["Payment Amount"]

        order_dict["order_coupon_code"]  = row["Order Coupon Code"] 

        order_dict["order_status"]  = row["Order Status"]


        order_dict["payment_method"]  = row["Payment Method"]
        order_dict["payment_live"]  = row["Payment Is Live"]
        order_dict["payment_response"]  = row["Payment Response"]
        order_dict["payment_successful"]  = row["Payment Successful"]

        
        return order_dict, error, error_list

        
    def create_order_item(self):
        pass

    def create_seller(self):
        pass

    
        