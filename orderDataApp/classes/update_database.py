import datetime

from decimal import Decimal

class UpdateDatabase:

    def __init__(self, order_data):

        self.order_data = order_data

        self.row_break_err = False
        self.row_break_err_list = []

    def update_db(self):

        for row in self.order_data:

            new_order, error, error_list =self.create_order(row) 


    def create_order(self, row):

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
        order_dict["payment_live"]  = row["Payment Is Live"]
        order_dict["payment_response"]  = row["Payment Response"]


        # translate {Yes/No} to True/False
        if row["Payment Successful"] == "Yes":
            order_dict["payment_successful"]  = True
        else:
            order_dict["payment_successful"]  = False


        
        return order_dict # , error, error_list

        
    def create_order_item(self):
        pass

    def create_seller(self):
        pass

    
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
        
            
        
        