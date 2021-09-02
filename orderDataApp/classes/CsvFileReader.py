
import csv
import copy

from collections import OrderedDict


class CsvFileReader:
        
    def make_order_item_key(self, property_name, num):
        """ Returns the property formatted with an integer based on format of CSV.
            If num equals 0, returs as is; concatenates " num+1" to property_name if num > 0
            @param property_name
            @param num  
        
        """
        
        if num == 0:
            return property_name

        elif num > 0:
            new_property_name = property_name + " " + str(num + 1)
            return new_property_name



    def build_seller_dict (self, order_items_dict_list):
        """ Returns lsit of order items dict with selle data construct in an ordered dict with each item dict
            @param order_items_dict_list       
        
        """
        seller_info_keys_list = ["Order Item Seller Uid","Order Item Seller Code",
                                "Order Item Seller Name","Order Item Seller Company",
                                "Order Item Seller Email"]
        
        seller_info_dict = OrderedDict()

        for item_dict in order_items_dict_list:
            
            for key in seller_info_keys_list:
                if key in item_dict:
                    poped_value = item_dict.pop(key) # remove key,value pair from the orderItem dict
                    seller_info_dict[key] = poped_value # add pair to seller info dict 
            
            item_dict["seller"] = copy.deepcopy(seller_info_dict) # add deep copy of seller info dict to item_dict: key="seller" 
            seller_info_dict.clear()
        
        return order_items_dict_list


    def process_file(self, uploaded_csv_file):

        try: 
        #with open( uploaded_csv_file, newline='') as csvfile:
            decoded_file = uploaded_csv_file.read().decode('utf-8').splitlines()
            reader = csv.DictReader(decoded_file)
            # print(reader)
            line_count = 0

            csv_data_list = [] #list obj to store transformed data

            for row in reader:
            # if line_count <=20:
                # make a deep copy of the row
                row_copy = copy.deepcopy(row)

                # list of all orderItem key names in the CSV
                order_item_keys_list = ["Order Item Item Uid","Order Item Source Id","Order Item Quantity",
                                    "Order Item Product Id","Order Item Product Type","Order Item Product Title",
                                    "Order Item Local Sku","Order Item Manufacturer Sku","Order Item Manufacturer Id",
                                    "Order Item Manufacturer Title","Order Item Features","Order Item Variant Id",
                                    "Order Item Variant Title","Order Item Variant Sku","Order Item Seller Uid",
                                    "Order Item Seller Code","Order Item Seller Name","Order Item Seller Company",
                                    "Order Item Seller Email","Order Item Seller Money Back","Order Item Seller Flat Shipping",
                                    "Order Item Seller Whats In Box","Order Item Return Days","Order Item Exchange Days",
                                    "Order Item Cost Price","Order Item Price Margin","Order Item Price Percent Margin",
                                    "Order Item List Price","Order Item Calculated Price","Order Item Override Price",
                                    "Order Item Product Price","Order Item Sales Price","Order Item Variant Price",
                                    "Order Item Basic Price","Order Item Discount Amount","Order Item Tax Amount",
                                    "Order Item Sub Total","Order Item Shipping Rule","Order Item Shipping Service",
                                    "Order Item Shipping Free","Order Item Shipping Amount","Order Item Shipping Tbd",
                                    "Order Item Shipping Note"]


                order_items_list = []  # list of order items

                number = 0
                order_item_first_key = self.make_order_item_key("Order Item Item Uid", number)
                
                
                while (order_item_first_key in row_copy ): # loop to evalauate if "property name + index" in each row and value isn't "None"
                    

                    # check if item is empty in CSV file                    
                    if row_copy[order_item_first_key] == '':

                        for property_name in order_item_keys_list:
                            new_property_name = self.make_order_item_key(property_name, number)

                            # if the corresponding key is found, delete item
                            if (new_property_name in row_copy):
                                del row_copy[new_property_name]
                        
                    else:
                        item_dict = OrderedDict() # a dict represent a single order item
                        # loop through the list of orderItem  key names
                        for property_name in order_item_keys_list:
                            new_property_name = self.make_order_item_key(property_name, number)

                            # if the corresponding key id found, pop item
                            if (new_property_name in row_copy):
                                                            
                                poped_value = row_copy.pop(new_property_name) 
                                item_dict[property_name] = poped_value                

                        order_items_list.append(copy.deepcopy(item_dict)) # deepcopy the item dict and append to the list of order items 
                        item_dict.clear()

                    # "number" to re-evaluate the loop 
                    number = number + 1
                    order_item_first_key = self.make_order_item_key("Order Item Item Uid", number)
                    
                
                # add the order items list to the row and clear list
                order_item_list_with_seller = self.build_seller_dict(copy.deepcopy(order_items_list))
                row_copy['order_items'] = order_item_list_with_seller
                order_items_list.clear()

                csv_data_list.append(copy.deepcopy(row_copy))
                line_count +=  1

            summary = "Number of processed rows: %d." % line_count 

            return csv_data_list, summary # return => "transformed csv data", summary

        except:
            raise


