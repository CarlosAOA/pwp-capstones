# TomeRater project
# Carlos A. Otero Alza

class User(object):
    def __init__(self, name, email):
        self.name = name
        self.email = email
        self.books_read = {}

    def get_email(self):
        return self.email

    def change_email(self, address):
        self.email = address
        print("""{name}'s email has been updated to {new_email}.""".format(name=self.name, new_email=address))

    def __repr__(self):
        return """User {name}, email: {email}, books read: {books_n}""".format(name=self.name, email=self.email, books_n=len(self.books_read))

    def __eq__(self, other_user):
        return self.name == other_user.name and self.email == other_user.email

    def read_book(self, book, rating=None):
        if type(rating) != int and type(rating) != float and rating != None:
            print("""Invalid Rating""")
        else:
            self.books_read[book] = rating
    
    def get_average_rating(self):
        rating_accum = 0
        for value in self.books_read.values():
            if value != None:
                rating_accum += value
        return rating_accum / len(self.books_read)
    
    def __hash__(self):
        return hash((self.name, self.email))

class Book(object):
    def __init__(self, title, isbn, price=None):
        self.title = title
        self.isbn = isbn
        self.price = price
        self.ratings = []
    
    def get_title(self):
        return self.title
    
    def get_isbn(self):
        return self.isbn
    
    # Need this method to prevent the error in the sorting part of the get_n_most method from the TomeRater
    # class when the price of a book is not given.
    def get_price(self):
        if self.price == None:
            return 0
        else:
            return self.price
        
    def set_isbn(self, isbn_new):
        self.isbn = isbn_new
        print("""{}'s ISBN has been updated.""".format(self.title))
    
    def add_rating(self, rating):
        if rating == None or (type(rating) != int and type(rating) != float):
            pass
        elif rating >= 0 and rating <= 4:
            self.ratings.append(rating)
        else:
            print("""Invalid Rating""")
    
    def __eq__(self, other_book):
        return self.title == other_book.title and self.isbn == other_book.isbn

    def get_average_rating(self):
        if len(self.ratings) < 1:
            print("""No ratings provided""")
        else:
            return sum(self.ratings) / len(self.ratings)
    
    def __hash__(self):
        return hash((self.title, self.isbn))
    
    def __repr__(self):
        return """{}""".format(self.title)

class Fiction(Book):
    def __init__(self, title, author, isbn, price=None):
        super().__init__(title, isbn, price)
        self.author = author
    
    def get_author(self):
        return self.author
    
    def __repr__(self):
        return """{title} by {author}""".format(title=self.title, author=self.author)
    
class Non_Fiction(Book):
    def __init__(self, title, subject, level, isbn, price=None):
        super().__init__(title, isbn, price)
        self.subject = subject
        self.level = level
    
    def get_subject(self):
        return self.subject
    
    def get_level(self):
        return self.level
    
    def __repr__(self):
        return """{title}, a {level} manual on {subject}""".format(title=self.title, level=self.level, subject=self.subject)

class TomeRater(object):
    def __init__(self):
        self.users = {}
        self.books = {}
    
    def create_book(self, title, isbn, price=None):
        book = Book(title, isbn, price)
        return book
    
    def create_novel(self, title, author, isbn, price=None):
        fiction = Fiction(title, author, isbn, price)
        return fiction
    
    def create_non_fiction(self, title, subject, level, isbn, price=None):
        non_fiction = Non_Fiction(title, subject, level, isbn, price)
        return non_fiction
    
    def add_book_to_user(self, book, email, rating=None):
        if not self.users[email]:
            print("""No user with email {}!""".format(email))
        else:
            c = 0
            book_stored_title = ""
            for book_stored in self.books:
                if book.isbn == book_stored.isbn and book.title != book_stored.title:
                    c +=1
                    book_stored_title = book_stored.title
            if c == 0:
                self.users[email].read_book(book, rating)
                book.add_rating(rating)
                if book in self.books:
                    self.books[book] += 1
                else:
                    self.books[book] = 1
            else:
                print("""There is already a book stored with the ISBN {isbn}: {title}""".format(isbn=book.isbn, title=book_stored_title))
    
    def add_user(self, name, email, books=None):
        if not "@" in email or not any(domain in email for domain in(".com", ".edu", ".org")):
            print("""Invalid email address""")
        else:
            if email in self.users:
                print("""This user already exists""")
            else:
                user = User(name, email)
                self.users[email] = user
                if books != None:
                    for book in books:
                        self.add_book_to_user(book, email)
    
    def print_catalog(self):
        for book in self.books.keys():
            print(book)
    
    def print_users(self):
        for user in self.users.values():
            print(user)
    
    def most_read_book(self):
        c = 0
        most_read = ""
        for book, times in self.books.items():
            if times > c:
                c = times
                most_read = book
            if c == 0:
                print("""No books have been read.""")
        return most_read
    
    def highest_rated_book(self):
        c = 0
        highest_rated = ""
        for book in self.books.keys():
            if book.get_average_rating() > c:
                c = book.get_average_rating()
                highest_rated = book
            if c == 0:
                print("""No books have ratings.""")
        return highest_rated
    
    def most_positive_user(self):
        c = 0
        most_positive = ""
        for user in self.users.values():
            if user.get_average_rating() > c:
                c = user.get_average_rating()
                most_positive = user
            if c == 0:
                print("""No users have ratings""")
        return most_positive
    
    def __repr__(self):
        return """This is the TomeRater application. {users} users and {books} books stored at the moment.""".format(users=len(self.users), books=len(self.books))
    
    def __eq__(self, other_TR):
        return self.users == other_TR.users and self.books == other_TR.books
    
    # For the get_n_most methods in the case of ties I decided to return all the items involved, that's why I included their "place in the line"
    # and the value inside the list as strings.
    def get_n_most(self, n, main_data, main_subject):
        n_most = []
        c1 = 0
        c2 = 0
        def take_value(item):
            return item[1]
        main_data.sort(key=take_value, reverse=True)
        while c1 < n:
            if c2 < len(main_data):
                n_most.append(("""Place {}""".format(c1+1),main_data[c2][0],"""{subject}: {value}""".format(subject=main_subject,value=main_data[c2][1])))
                if c2+1 == len(main_data):
                    c1 += 1
                else:
                    if not main_data[c2][1] == main_data[c2+1][1]:
                        c1 += 1
                c2 += 1
            else:
                break
        return n_most
        
    def get_n_most_read_books(self, n):
        main_data = []
        main_subject = """Times read"""
        for key,value in self.books.items():
            main_data.append((key,value))
        return self.get_n_most(n, main_data, main_subject)
    
    # In the instructions the description of get_n_most_prolific_readers is the same as get_n_most_read_books
    # so I assumed that the value of comparison is the number of books read by the users.
    # When this method is called it returns the number of books read 2 times. This happens because of the __repr__ defined
    # for the User class that already includes this number. I decided to leave it this way just to fulfill the instructions
    # for the User class part. Otherwise, I would erase this part of the string in __repr__.
    def get_n_most_prolific_readers(self, n):
        main_data = []
        main_subject = """Number of books read"""
        for value in self.users.values():
            main_data.append((value,len(value.books_read)))
        return self.get_n_most(n, main_data, main_subject)
    
    def get_n_most_expensive_books(self, n):
        main_data = []
        main_subject = """Price"""
        for key in self.books.keys():
            main_data.append((key,key.get_price()))
        return self.get_n_most(n, main_data, main_subject)
    
    def get_worth_of_user(self, user_email):
        if not self.users[user_email]:
            print("""No user with email {}!""".format(user_email))
        else:
            total_worth = 0
            for book in self.users[user_email].books_read:
                total_worth += book.get_price()
            return total_worth
    
    def get_n_most_spender(self, n):
        worth_of_user = {}
        for user_email in self.users:
            worth_of_user[self.users[user_email]] = self.get_worth_of_user(user_email)
        main_data = []
        main_subject = """Total worth of books"""
        for key,value in worth_of_user.items():
            main_data.append((key,value))
        return self.get_n_most(n, main_data, main_subject)
    
    def get_n_most_rated_books(self, n):
        main_data = []
        main_subject = """Average rating"""
        for key in self.books.keys():
            main_data.append((key, key.get_average_rating()))
        return self.get_n_most(n, main_data, main_subject)
