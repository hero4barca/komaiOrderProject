import datetime
import copy

from decimal import Decimal
from orderDataApp.models import Order, Seller, OrderItem


class UpdateDatabase:

    def __init__(self, order_data):

        self.order_data = order_data
        self.data_errors_list = []

        self.new_orders_created = 0
        self.new_sellers_created = 0
        self.new_orderitems_created = 0

        self.row_break_err = False
        self.row_break_err_list = []



    def update_data(self):

        for row in self.order_data:

            # create order_dict for db
            new_order =self.create_order(row) 

            #retrieve list of order items from row
            order_items = row['order_items']

            # create order_items for db
            order_items_cleaned = self.create_order_items(order_items)

            # reate seller for db
            cleaned_order_items_with_sellers = self.create_seller(order_items_cleaned)
            
            
            #check for row break error
            if self.row_break_err:

                # copy break_errs to rows_error_list
                for error in self.row_break_err_list:
                    self.data_errors_list.append(copy.deepcopy(error))

                self.row_break_err_list.clear()
                self.row_break_err = False

            else:
                # try-> except for this
                self.save_to_db(new_order, cleaned_order_items_with_sellers)
                
            
                    
                        


    def create_order(self, row):
        """Creates an order object corresponding to the Order model
        """

        order_dict = {}
        #error = False
        #error_list = []

        #break_err= False
        #break_err_list = []

        order_number = row["Order Number"]
        order_dict["order_number"] = order_number

        # convert date string to datetime obj
        try:
            order_datetime = datetime.datetime.strptime(row["Order Date"], "%Y-%m-%d %H:%M:%S" )
            order_date = order_datetime.date()
            order_time = order_datetime.time()
        except:
            order_date, order_time = None # assign none to date and time 
            
            #error = True
            #datetime_conversion_err_str = "Couldn't convert for order -> %s" % order_dict["order_number"] # detailerror in error list
            #error_list.append(datetime_conversion_err_str)
        
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

        order_dict["order_currency"] = row["Order Currency"]

        # convert order total to decimal
        order_total, total_err, total_err_msg = self.str_to_decimal(order_number, row["Order Total"], 
                                                                    "Order Total", True)
        order_dict["order_total"]  = order_total 
        self.update_row_err(total_err,total_err_msg)
 
        #convert order_taxes to decimal 
        order_taxes, order_taxes_err, order_taxes_err_msg = self.str_to_decimal(order_number, 
                                                                            row["Order Taxes"], 
                                                                            "Order Taxes")
        order_dict["order_taxes"]  = order_taxes

        # convert order_discount to decimal
        order_discounts, order_discounts_err, order_discounts_err_msg = self.str_to_decimal(order_number, 
                                                                            row["Order Discounts"], 
                                                                            "Order Discounts")                
        order_dict["order_discounts"]  = order_discounts

        # convert order_taxes to decimal
        order_subtotal, order_subtotal_err, order_subtotal_err_msg = self.str_to_decimal(order_number, 
                                                                            row["Order Subtotal"], 
                                                                            "Order Subtotal", True)        
        order_dict["order_subtotal"]  = order_subtotal # deal 
        self.update_row_err(order_subtotal_err, order_discounts_err_msg)

        # convert shipping cost to decimal
        order_shipping_cost, order_shipping_cost_err, order_shipping_cost_err_msg = self.str_to_decimal(order_number, 
                                                                            row["Order Shipping"], 
                                                                            "Order Shipping", True)        
        order_dict["order_shipping_cost"]  = order_shipping_cost 
        self.update_row_err(order_shipping_cost_err, order_shipping_cost_err_msg)

        # convert shipping_TBD to decimal
        order_shipping_TBD, order_shipping_TBD_err, order_shipping_TBD_err_msg = self.str_to_decimal(order_number, 
                                                                            row["Order Ship Tbd"], 
                                                                            "Order Ship Tbd")        
        order_dict["order_ship_TBD"]  = order_shipping_TBD
        
        # convert cart_total
        order_cart_total, order_cart_total_err, order_cart_total_err_msg = self.str_to_decimal(order_number, 
                                                                            row["Order Cart Total"], 
                                                                            "Order Cart Total", True)        
        order_dict["order_cart_total"]  = order_cart_total 
        self.update_row_err(order_cart_total_err, order_cart_total_err_msg)

        # convert  Cart Taxes to decimal
        order_cart_taxes, order_cart_taxes_err, order_cart_taxes_err_msg = self.str_to_decimal(order_number, 
                                                                            row["Order Cart Taxes"], 
                                                                            "Order Cart Taxes")        
        order_dict["order_cart_taxes"]  = order_cart_taxes
        
        # convert  Cart Discount to decimal
        order_cart_discount, order_cart_discount_err, order_cart_discount_err_msg = self.str_to_decimal(order_number, 
                                                                            row["Order Cart Discounts"], 
                                                                            "Order Cart Discounts")        
        order_dict["order_cart_discount"]  = order_cart_discount

        # convert Grand Total
        order_grand_total, order_grand_total_err, order_grand_total_err_msg = self.str_to_decimal(order_number, 
                                                                            row["Order Grand Total"], 
                                                                            "Order Grand Total", True)        
        order_dict["order_grand_total"]  = order_grand_total
        self.update_row_err(order_grand_total_err, order_grand_total_err_msg)

        # convert  coupon value to decimal
        order_coupon_value, order_coupon_value_err, order_coupon_value_err_msg = self.str_to_decimal(order_number, 
                                                                            row["Order Coupon Value"], 
                                                                            "Order Coupon Value")        
        order_dict["order_coupon_value"]  = order_coupon_value

        # convert  Payment fee to decimal
        order_payment_fee, order_payment_fee_err, order_payment_fee_err_msg = self.str_to_decimal(order_number, 
                                                                            row["Payment Fee"], 
                                                                            "Payment Fee")        
        order_dict["payment_fee"]  = order_payment_fee

        # convert  payment amt to decimal
        order_payment_amt, order_payment_amt_err, order_payment_amt_err_msg = self.str_to_decimal(order_number, 
                                                                            row["Payment Amount"], 
                                                                            "Payment Amount", True)        
        order_dict["payment_amount"]  = order_payment_amt 
        self.update_row_err(order_payment_amt_err, order_payment_amt_err_msg)

        order_dict["order_coupon_code"]  = row["Order Coupon Code"] 
        order_dict["order_status"]  = row["Order Status"]

        order_dict["payment_method"]  = row["Payment Method"]
        order_dict["payment_response"]  = row["Payment Response"]

        # Translate Yes/NO to True/false
        if row["Payment Is Live"] == "No":
            order_dict["payment_live"]  = False
        else:
            order_dict["payment_live"]  = True

        # translate {Yes/No} to True/False
        if row["Payment Successful"] == "Yes":
            order_dict["payment_successful"]  = True
        else:
            order_dict["payment_successful"]  = False
        
        return order_dict # , error, error_list



    def create_order_items(self, order_items_list):
        """Creates a list of order items corresponding to the Order Items model
        @param order_items_list: raw list of order items retrieved from sessions
        @return item_obj_list: list of dict objects corresponding to the definition of the order_item model
        """

        item_obj_list =[]

        new_item = {}
       
        for item in order_items_list: # loop through items in the list
    
            new_item['item_uid'] = order_items_list["Order Item Item Uid"]

            # cast quantity to integer and assign
            item_quantity_str = order_items_list["Order Item Quantity"]
            if str.isdigit(item_quantity_str):
                new_item['item_quantity'] = int(item_quantity_str)
            else:
               new_item['item_quantity'] = 0
            
            new_item['item_product_id'] = order_items_list["Order Item Product Id"]
            new_item['item_product_type'] = order_items_list["Order Item Product Type"]
            new_item['item_product_title'] = order_items_list["Order Item Product Title"]
            
            # cast return_days to integer and assign
            item_return_days_str = order_items_list["Order Item Return Days"]
            if str.isdigit(item_return_days_str):
                new_item['item_return_days'] = int(item_return_days_str)
            else:
               new_item['item_return_days'] = 0

            # cast exchnage_days to integer and assign
            item_exchange_days_str = order_items_list["Order Item Exchange Days"]
            if str.isdigit(item_exchange_days_str):
                new_item['item_exchange_days'] = int(item_exchange_days_str)
            else:
               new_item['item_exchange_days'] = 0

            # item product price
            try:
                new_item['item_product_price'] = Decimal(order_items_list['Order Item Product Price'])
            except:
                new_item['item_product_price'] = 0.0

            # item basic price
            try:
                new_item['item_basic_price'] = Decimal(order_items_list['Order Item Basic Price'])
            except:
                new_item['item_basic_price'] = 0.0
            
            # discount amount
            try:
                new_item['item_discount_amount'] = Decimal(order_items_list['Order Item Discount Amount'])
            except:
                new_item['item_discount_amount'] = 0.0

            # tax amount
            try:
                new_item['item_tax_amount'] = Decimal(order_items_list['Order Item Tax Amount'])
            except:
                new_item['item_tax_amount'] = 0.0

            try:
                new_item['item_sub_total'] = Decimal(order_items_list['Order Item Sub Total'])
            except:
                new_item['item_sub_total'] = 0.0

            #********
            new_item['seller'] = order_items_list['seller']
            

            item_obj_list.append(copy.deepcopy(new_item))
            new_item.clear()

        return item_obj_list



    def create_seller(self, order_items_with_sellers):
        """Create seller dicts with keys that correspond to the Seller Model
        @param items_sellers, list of items seller retrieved from saved sessions variable
        @return sellers_list  
    
        """
        seller = {}

        for item in order_items_with_sellers:

            item_seller = item.pop("seller")

            seller['seller_uid'] = item_seller['Order Item Seller Uid']
            seller['seller_unique_code'] = item_seller['Order Item Seller Code']
            seller['seller_name'] = item_seller['Order Item Seller Name']
            seller['seller_company'] = item_seller['Order Item Seller Company']
            seller['seller_email'] = item_seller['Order Item Seller Email']

            item['seller'] =  copy.deepcopy(seller)
            seller.clear()

        return order_items_with_sellers



    def str_to_decimal(self, order_number, decimal_str, key, break_on_err=False):
        """Converts string values to decimal 
        @param order_number: order number
        @param decimal_str -> value to be converted to decimal
        @param key -> dict key of the var (decimal str)
        @param break_on_err, Boolean, how to handle conversion exception 
        
        """
        break_err = False
        break_err_msg = ""

        try:
            decimal_value = Decimal(decimal_str)            
        except:
            if break_on_err: # assign none to value and generate error 
                decimal_value = None
                break_err = True
                break_err_msg = "Couldn't convert %s to decimal for order '%s' " % key, order_number
            else:
                decimal_value = 0.00 # assign 0.00 to decimal value
               
        return decimal_value, break_err, break_err_msg 



    def update_row_err( self, err, err_msg):

        if err:
            self.row_break_err = True
            self.row_break_err_list.append(err_msg)
        
            
    def save_to_db(self, order_dict, order_items_dict_list):

        order_model_obj, order_created = Order.objects.get_or_create(**order_dict)

        if order_created:
            
            self.new_orders_created += 1 # increase count of new orders created  

            new_seller = {}
            for item_with_seller in order_items_dict_list:

                # pop seller from dict and save to database
                new_seller = item_with_seller.pop("seller") 
                seller_model_obj, seller_created = Seller.objects.get_or_create(**new_seller)
                
                if seller_created:
                    self.new_sellers_created += 1

                # pass newly created seller obj as foreign key to seller
                item_with_seller['seller'] = seller_model_obj
                
                # pass newly created order as foreign key to order
                item_with_seller['order'] = order_model_obj
                
                orderitem_model_obj, orderitem_created = OrderItem.objects.get_or_create(**item_with_seller)
                
                if orderitem_created:
                    self.new_orderitems_created += 1

                new_seller.clear()

    def num_of_new_records(self):

        return self.new_orders_created, self.new_sellers_created, self.new_orderitems_created
   



        