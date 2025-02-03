import sys
from collections import defaultdict

class MarketBook:
    def __init__(self):
        self.buy_orders = {} #Maps price → volume for all active bid orders
        self.sell_orders = {} #Maps price → volume for all active offer orders
        self.ordered_bids = [] #List of all bid prices but they're ordered decrementally
        self.ordered_offers = [] #List of all offers orderd incrementally
    
    #Updating all lists with the order
    def add_order(self, order_type, price, volume):
        if order_type == "BID":
            self.buy_orders[price] = volume #Updating dictionary (key/value) --> this might not be a good idea if there already is a bid
            self.ordered_bids.append(price) #Updating pricing list --> Would this create a duplicate in the ordered_bids list
            self.ordered_bids.sort(reverse=True)
        elif order_type == "OFFER":
            self.sell_orders[price] = volume
            self.ordered_offers.append(price)
            self.ordered_offers.sort()

    def modify_order(self, order_type, price, volume):
        if order_type == "BID" and price in self.buy_orders:
            self.buy_orders[price] = volume #Shouldn't this add onto the existing volume instead of replace it?
        elif order_type == "OFFER" and price in self.sell_orders:
            self.sell_orders[price] = volume #Shouldn't this add onto the existing volume instead of replace it?

    def remove_order(self, order_type, price):
        if order_type == "BID" and price in self.buy_orders:
            del self.buy_orders[price] 
            self.ordered_bids.remove(price)
        elif order_type == "OFFER" and price in self.sell_orders:
            del self.sell_orders[price]
            self.ordered_offers.remove(price)
    
    #NOt used but only used to see the current state of a book
    def get_current_book(self):
        return {
            "BIDS": {price: self.buy_orders[price] for price in self.ordered_bids},
            "OFFERS": {price: self.sell_orders[price] for price in self.ordered_offers}
        }

def handle_input(input_lines):
    exchange_books = defaultdict(MarketBook) #Instantiating a new Marketbook object for every single Exchange reference
    #defaultdict(MarketBook) is a Python trick that ensures a new MarketBook instance is created on demand each time you use a key that doesn’t already exist
    consolidated_book = MarketBook() #Creates one object instance for the consolidated/master book
    
    results = [] #Used to store the outputs
    
    for line in input_lines:
        parts = line.strip().split(",") #Removes any trailing white lines and splits up each item an array
        
        if parts[2] == "DELETE":
            exchange_id, idx, action, order_type = parts 
            idx = int(idx)
            price = None ##Delete lines don't provide this
            volume = None ##Delete lines don't provide this
        else:
            exchange_id, idx, action, order_type, price, *volume = parts
            idx, price = int(idx), int(price)
            volume = int(volume[0]) if volume else None #Why wouldn't volume exist in this case?
        
        exchange_book = exchange_books[exchange_id] #We are addressing this line of the exchange book for the following lines for processing
        
        if action == "NEW":
            exchange_book.add_order(order_type, price, volume)
        elif action == "UPDATE":
            exchange_book.modify_order(order_type, price, volume)
        elif action == "DELETE":
            exchange_book.remove_order(order_type, price)
        
        #Updating the consolidated book with a new order
        if action != "DELETE":
            consolidated_book.add_order(order_type, price, volume) #Not a good setup as deletion does not update in the consolidated view


        results.append(f"C,{idx},{action},{order_type},{price if price else '' },{volume if volume else ''}".strip(",")) #.strip(",") takes car of trailing commas
        #In what case would the price be none like I don't think that would work
        #In what case would the volume be none?
    
    return results

def main():
    
    input_file = sys.argv[1] #This takes the second argument after the code running script
    output_file = sys.argv[2] #This takes the second argument after the code running script
    
    with open(input_file, "r") as f: #opens the file aliased to input_file in read mode.
        input_lines = f.read().strip().split("\n") #f.read() puts f into one whole string, then strip it with any blankspace and split them based on each line
    
    result = handle_input(input_lines) 
    
    with open(output_file, "w") as f: #creates or writes to output_file
        f.write("\n".join(result) + "\n") #takes the list of result lines and joins them into a single string, with each line separated by a newline

    
#This is a python idiom that basically calls this function if and only if the script was called directly and not imported
if __name__ == "__main__":
    main()
