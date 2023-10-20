from main import *
from General_Functions.General_functions import *


class Pagination:
    def __init__(self,crtieria):
        self.limit = int(crtieria["limit"])
        self.page = int(crtieria["page"])


    def data(self, get_filter_args, document_count): # this function decribes that the feth the data with the criterira pf limit and pages.
        skip = (self.page - 1) * self.limit # Calculate the number of items to skip in the pagination based on the current page and items per page.

        # Count the number of documents in the Movies Collection.
        total_movies = document_count

        # this function return the how many pages need for the all documents
        def total_no_pages():
            if total_movies % self.limit == 0:
               return total_movies // self.limit
            else:
                return ((total_movies // self.limit) + 1)

        pages = [i for i in range(1, total_no_pages()+1)] # after getting the how many pages it will store in the list by separate value. ex: no.of.pages = 3. in this list store like this = [1,2,3]
        items = (get_filter_args.skip(skip).limit(self.limit))
        print((items))

        # after getting the all elements calling the pagination_response_data function by respective arguments.
        return  response_data(data=items,message="Movies Listed successfully", next=self.page + 1,page=self.page, pages=pages, prev=self.page - 1, status=200,success=True, total=total_no_pages(), total_records=total_movies)