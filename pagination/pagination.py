from main import *
from General_Functions.General_functions import *
from bson import json_util,ObjectId

class Pagination:
    def __init__(self,limit,page):
        self.limit = int(limit)
        self.page = int(page)
        self.items_per_page = 4
    def data(self): # this function decribes that the feth the data with the criterira pf limit and pages.

        skip = (self.page - 1) * self.items_per_page # Calculate the number of items to skip in the pagination based on the current page and items per page.

        # Count the number of documents in the Movies Collection.
        total_movies = movies.count_documents({})

        # this function return the how many pages need for the all documents
        def total_no_pages():
            if total_movies % self.limit == 0:
               return total_movies // self.limit
            else:
                return ((total_movies // self.limit) + 1)

        pages = [i for i in range(1, total_no_pages()+1)] # after getting the how many pages it will store in the list by separate value. ex: no.of.pages = 3. in this list store like this = [1,2,3]


        items = list(movies.find().skip(skip).limit(self.items_per_page)) # This query fetching the movies with given limit and given page.

        all_items = [] # after getting the all movies. The movies stored in this list by following for loop.
        for item in items:
            all_items.append({"movie_name": item["movie_name"], "Director_name": item["DirectorName"]})

        # after getting the all elements calling the pagination_response_data function by respective arguments.
        return  pagination_response_date(data=all_items,message="Movies Listed successfully", next=self.page + 1,page=self.page, pages=pages, prev=self.page - 1, status=200,success=True, total=total_no_pages(), total_records=total_movies)


