from datetime import datetime

class Book:
    def __init__(self, isbn,title,year,price):
        self.isbn = isbn
        self.title = title
        self.year = year
        self.price = price

    def is_buyable(self):
        return True
    
    def send_to_client(self,email,address,quantity):
        raise NotImplementedError("This method is not implemented")

class PaperBook(Book):
    def __init__(self, isbn,title,year,price,stock):
        super().__init__(isbn,title,year,price)
        self.stock = stock
    
    def send_to_client(self,email,address,quantity):
        if self.stock >= quantity:
            self.stock -= quantity
            print(f"Book Store: Sending PaperBook to {address}")
        else:
            raise Exception(f"Book Store: Not enough stock for {quantity} PaperBooks")

class EBook(Book):
    def __init__(self, isbn,title,year,price,filetype):
        super().__init__(isbn,title,year,price)
        self.filetype = filetype
    
    def send_to_client(self,email,address,quantity):
        print(f"Book Store: Sending EBook to {email}")

class Demo(Book):
    def is_buyable(self):
        return False
    
class Inventory:
    def __init__(self) -> None:
        self.books = {}
    
    def add_book(self,book):
        self.books[book.isbn] = book
    
    def remove_outdated_books(self,outdate):
        curr_year = datetime.now().year
        removed =[]
        for isbn,book in list(self.books.items()):
            if curr_year - book.year > outdate:
                removed.append(self.books.pop(isbn))
        return removed
    
    def get_book(self,isbn):
        if isbn  not in self.books:
            raise Exception("Book not found")
        return self.books[isbn]

class Store:
    def __init__(self,inventory) -> None:
        self.inventory = inventory
    
    def buy_book(self, isbn, quantity, email, address):
        book:Book = self.inventory.get_book(isbn)
        if not book.is_buyable():
            raise Exception("The book is for ShowCase not for sale")
        total = book.price * quantity
        book.send_to_client(email,address,quantity)
        print(f"Book Store: Purchase successful. Total paid: ${total}")
        return total
    
class Test:
    @staticmethod
    def run():
        inventory = Inventory()
        store = Store(inventory)
        
        inventory.add_book(PaperBook("ISBN001", "Paper Book",2018, 100, 10))
        inventory.add_book(EBook("ISBN002", "EBook", 2020, 50, "PDF"))
        inventory.add_book(Demo("ISBN003", "Demo Book", 2010, 0))

        removed = inventory.remove_outdated_books(10)
        for b in removed:
            print(f"Book store: Removed outdated book {b.title}")
        
        try:
            store.buy_book("ISBN001", 2, "customer@example.com", "123 Street")
            store.buy_book("ISBN002", 1, "customer@example.com", "")
            store.buy_book("ISBN003", 1, "customer@example.com", "") 
        except Exception as e:
            print(e)

        
if __name__ == "__main__":
    Test.run()