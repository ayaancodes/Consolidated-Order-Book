import sys
from collections import defaultdict

class MarketBook:

# The folllowing functions i'd consider them to be like the helper functions that actually perform the changes in
#the logic handling and the crud operations i'd like to say. 

    #Each order will be considered to be an object and each object will have certain properties that they will 
    #adhere to
    def __init__(self):
        # For each book we track orders by price and maintain an ordered list of prices.
        self.buy_orders = {}      # For BID orders: price → volume
        self.sell_orders = {}     # For OFFER orders: price → volume
        self.ordered_bids = []    # Sorted (descending) list of bid prices
        self.ordered_offers = []  # Sorted (ascending) list of offer prices

    def add_order(self, order_type, price, volume): 
        """Adds volume to a given price point (or creates a new one)."""
        if order_type == "BID":
            if price in self.buy_orders:
                self.buy_orders[price] += volume  #This adds different exchange quantities together if they exist 
                self.buy_orders[price] = volume #Creating a new item in the dictionary with the price and the quantity
                self.ordered_bids.append(price)
                self.ordered_bids.sort(reverse=True) #Descending order cause they represent levels so level 0 would be the 
        elif order_type == "OFFER":
            if price in self.sell_orders:
                self.sell_orders[price] += volume
            else:
                self.sell_orders[price] = volume
                self.ordered_offers.append(price)
                self.ordered_offers.sort()

    def update_order(self, order_type, price, volume):
        """(Not used in our examples—but here you would update an order's volume.)"""
        if order_type == "BID":
            if price in self.buy_orders:
                self.buy_orders[price] = volume
        elif order_type == "OFFER":
            if price in self.sell_orders:
                self.sell_orders[price] = volume

    def remove_order_by_index(self, order_type, idx):
        """
        Removes the order at the given index from the sorted list.
        Returns a tuple (price, volume) of the removed order.
        """
        
        if order_type == "BID":
            if 0 <= idx < len(self.ordered_bids):
                price = self.ordered_bids[idx]
                volume = self.buy_orders[price]
                del self.buy_orders[price]
                self.ordered_bids.pop(idx)
                return price, volume
        elif order_type == "OFFER":
            if 0 <= idx < len(self.ordered_offers):
                price = self.ordered_offers[idx]
                volume = self.sell_orders[price]
                del self.sell_orders[price]
                self.ordered_offers.pop(idx)
                return price, volume
        return None, 0

    def remove_order(self, order_type, price, volume):
        """
        Removes a given volume from the order at 'price'.
        If the remaining volume is 0 or less, the price is removed entirely.
        """
        if order_type == "BID" and price in self.buy_orders:
            self.buy_orders[price] -= volume
            #Don't really understand the purpose of this code
            if self.buy_orders[price] <= 0:
                #What is the 'del' functionality how does it work
                del self.buy_orders[price]
                self.ordered_bids.remove(price)
        elif order_type == "OFFER" and price in self.sell_orders:
            self.sell_orders[price] -= volume
            if self.sell_orders[price] <= 0:
                del self.sell_orders[price]
                self.ordered_offers.remove(price)

    def get_current_book(self):
        """Returns the current order book (for debugging, if needed)."""
        return {
            "BIDS": {price: self.buy_orders[price] for price in self.ordered_bids},
            "OFFERS": {price: self.sell_orders[price] for price in self.ordered_offers}
        }

def handle_input(input_lines):
    # Create one book per exchange and one consolidated book.
    exchange_books = defaultdict(MarketBook) #How do you manage the logic for this
    #defaultdict(MarketBook) is a Python trick that ensures a new MarketBook instance is created on demand each time you use a key that doesn’t already exist
    consolidated_book = MarketBook()
    results = [] 

    for line in input_lines:
        parts = line.strip().split(",") #Removes any trailing white lines and splits up each item an array
        exchange_id = parts[0] #Grabs the exchange id of line i 
        idx = int(parts[1]) # Grabs the level index of line
        action = parts[2] 
        order_type = parts[3]

        # For NEW (and UPDATE) actions we expect a price and volume.
        if action != "DELETE":
            price = int(parts[4])
            volume = int(parts[5])

        if action == "NEW":
            # Look up the previous aggregated volume for this price (if any)
            if order_type == "BID":
                prev_volume = consolidated_book.buy_orders.get(price, 0) #Explain this like i think if it's checkning if that price has any quantity but like what if the key doesn't exist?
            else:
                prev_volume = consolidated_book.sell_orders.get(price, 0)

            # Add the order to the specific exchange’s book.
            exchange_books[exchange_id].add_order(order_type, price, volume)
            # Then update the consolidated book (this aggregates volumes across exchanges).
            consolidated_book.add_order(order_type, price, volume)
            ##don't really understand this part of my code like how is this aggregating multiple different exchange information
            new_volume = (consolidated_book.buy_orders.get(price, 0)
                          if order_type == "BID" else
                          consolidated_book.sell_orders.get(price, 0))
            # If the price did not exist before, output a NEW event; otherwise, output an UPDATE.
            if prev_volume == 0:
                results.append(f"C,{idx},NEW,{order_type},{price},{volume}")
            else:
                results.append(f"C,{idx},UPDATE,{order_type},{new_volume}")

        elif action == "UPDATE":
            # (Not covered by the sample—but here you would adjust the order in the exchange book,
            # recalc the aggregated volume difference, update the consolidated book, and output an UPDATE.)

            #TEST MYSELF TOMORROW MORNING
            pass

        elif action == "DELETE":
            # For DELETE, use the provided index (idx) to remove the order from the exchange's sorted list.
            # Don't really understand delete functionality
            if order_type == "BID":
                #Dont understand hwo this is structured like python using price, removed_volume to set a variable
                price, removed_volume = exchange_books[exchange_id].remove_order_by_index(order_type, idx)
            else:
                price, removed_volume = exchange_books[exchange_id].remove_order_by_index(order_type, idx)

            if price is not None:
                # Get the previous aggregated volume from the consolidated book.
                if order_type == "BID":
                    #How does this work
                    prev_agg = consolidated_book.buy_orders.get(price, 0)
                else:
                    prev_agg = consolidated_book.sell_orders.get(price, 0)
                # Remove the removed volume from the consolidated book.
                consolidated_book.remove_order(order_type, price, removed_volume)
                #How does this work? Why is there two paranthesis 
                new_agg = (consolidated_book.buy_orders.get(price, 0)
                           if order_type == "BID" else
                           consolidated_book.sell_orders.get(price, 0))
                # If after deletion the aggregated volume is still positive, output an UPDATE event.
                # Otherwise, if it has dropped to zero, output a DELETE event.
                if new_agg > 0:
                    results.append(f"C,{idx},UPDATE,{order_type},{new_agg}")
                else:
                    results.append(f"C,{idx},DELETE,{order_type}")
            # If no order was removed, nothing is output.

    return results

def main():
    input_file = sys.argv[1]   # e.g. input.txt
    output_file = sys.argv[2]  # e.g. output.txt

    with open(input_file, "r") as f: #opens the file in the directory aliased to input_file in read mode.
        input_lines = f.read().strip().split("\n")  #takes the list of result lines and joins them into a single string, with each line separated by a newline

    result = handle_input(input_lines)

    with open(output_file, "w") as f:
        f.write("\n".join(result) + "\n")

if __name__ == "__main__":
    main()
