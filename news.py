from newsapi import NewsApiClient
from datetime import datetime
from vars import source_list, api_key, the_path, source_set
from fpdf import FPDF
import os

print()
print("Welcome to my Kindle News Aggregator!")
print()

class News:

    def __init__(self, api_key):

        self.newsapi = NewsApiClient(api_key=api_key)

        self.keywords = None
        self.sources = None
        self.breaking = True
        self.all = False
        self.from_when = None
        self.till_when = None
    
        self.info_functions()
       
    def info_functions(self):

        self.get_sources()
        self.get_keywords()
        self.from_date()
        self.to_date()
        self.breaking_or_all()


    def get_sources(self):

        my_source_list = source_list

        sources_set = source_set

        requested_sources = self.get_requested_sources(my_source_list, sources_set)
        
        if (not requested_sources):
            print("There were no requested sources. Please try again.")
            exit(0)

        self.sources = requested_sources

    def get_requested_sources(self, source_list, sources_set):

        requested_sources = []

        while True:

            source = input("Enter a source (or 'n' to go to next page, 's' to show available sources): ").lower()

            if (source == 'n'):
                break
            elif (source == 's'):
                print(source_list)
            elif (source not in sources_set):
                print("This source is not in the list. Please try again.")
            elif (source in requested_sources):
                print("This source is already in your list.")
            else:
                requested_sources.append(source)

        return requested_sources
    
    def get_keywords_helper(self):

        keywords = []
        
        while True:

            keyword = input("Enter a keyword (or 'n' for the next page): ").lower()
            if (keyword == 'n'):
                break
            keywords.append(keyword)

        return keywords
    
    def generate_keywords_dict(self, keywords):

        keywords_dict = {}

        for i in range(len(keywords)):
            keywords_dict[keywords[i]] = i

        return keywords_dict
    
    def get_user_choice(self, prompt):
        
        while True:
            
            choice = input(prompt).lower()

            if (choice in ('y', 'n')):
                return choice == 'y'
            
            print("Please enter 'y' or 'n'.")

    def get_keywords(self):
        
        print()

        if (self.get_user_choice("Would you like to search by keywords? (y/n): ")):
            
            keywords = self.get_keywords_helper()
            self.keywords_advanced(keywords)
        
            self.keywords = keywords

    def modify_keyword(self, keywords, keywords_dict, prompt, modifier):

        word = input(prompt)

        while word.lower() != 'n':
            
            if word not in keywords_dict:
                print("This keyword wasn't one you initially added. Please enter one of the keywords you added.")
                word = input(prompt)
            
            else:
                word_idx = keywords_dict[word]
                keywords[word_idx] = modifier + word + (modifier if modifier == '"' else "")
                word = input(prompt)

    def keywords_advanced(self, keywords):

        keywords_dict = self.generate_keywords_dict(keywords)

        self.print_advanced_search_options()
        
        if self.get_user_choice("Search for an exact match of a keyword? (y/n): "):

            self.modify_keyword(keywords, keywords_dict, "Enter a keyword for exact match (or 'n' for the next page): ", '"')

        if self.get_user_choice("Search for a keyword that must appear? (y/n): "):

            self.modify_keyword(keywords, keywords_dict, "Enter a keyword that must appear (or 'n' for the next page): ", '+')

        if self.get_user_choice("Search for a keyword that must not appear? (y/n): "):

            self.modify_keyword(keywords, keywords_dict, "Enter a keyword that must not appear (or 'n' for the next page): ", '-')

        if self.get_user_choice("Use AND/OR/NOT between keywords? (y/n): "):

            self.apply_conditions(keywords, keywords_dict)

    def print_advanced_search_options(self):

        print()
        print("With this API, you can conduct an advanced search between the keywords you've used.")
        print("The advanced search can provide the following: ")
        print()
        print("1. An exact match for a keyword you've entered")
        print("2. Words that MUST appear in the article")
        print("3. Words that MUST NOT appear in the article")
        print("4. Use AND/OR/NOT to represent a relationship between the keywords")
        print()
    
    def apply_conditions(self, keywords, keywords_dict):

        condition = input("Enter condition between keywords using AND/OR/NOT: ")
        condition_list = condition.split()

        for word in condition_list:

            if word in keywords_dict:
                keywords.pop(keywords_dict[word])
                keywords_dict = self.generate_keywords_dict(keywords)

        keywords.append(' '.join(condition_list))
            
    def breaking_or_all(self):
        
        print()
        print("This program can return either breaking news or all pertinent news. Which would you like? Enter 'b' for breaking, and 'a' for all.")
        
        while True:

            b_or_a = input("Enter 'a' or 'b' here: ").lower()

            if b_or_a in ('a', 'b'):
                break

            print("Please enter 'a' or 'b'.")
        
        if b_or_a == 'b':
            self.breaking = True
        else:
            self.all = True
            self.breaking = False

    def from_date(self):
        print()

        self.from_when = self.get_date("Enter the start date (YYYY-MM-DD) or 'n' for the next page: ")

    def to_date(self):
        print()
        self.till_when = self.get_date("Enter the end date (YYYY-MM-DD) or 'n' for the next page: ")

    def get_date(self, prompt):

        while True:
            date_input = input(prompt)
            if date_input.lower() == 'n':
                print("No date entered.")
                break
            try:
                date_obj = datetime.strptime(date_input, "%Y-%m-%d")
                break
            except ValueError:
                print("Invalid date format. Please enter the date in YYYY-MM-DD format.")
    
    
    def generate_query(self):
        
        query_dict = {}
        query_dict["q"] = None
        query_dict["sources"] = None
        query_dict["from_param"] = None
        query_dict["to"] = None

        if (self.keywords is not None):

            keyword_string = ""
            for i in range(len(self.keywords)-1):
                keyword_string += self.keywords[i] + ", "
            keyword_string += self.keywords[len(self.keywords)-1]
            query_dict["q"] = keyword_string
            

        if (self.sources is not None):

            sources_string = ""
            for i in range(len(self.sources)-1):
                sources_string += self.sources[i] + ", "
            sources_string += self.sources[len(self.sources)-1]
            query_dict["sources"] = sources_string

        if (self.from_when is not None):
            query_dict["from_param"] = self.from_when
        
        if (self.till_when is not None):
            query_dict["to"] = self.till_when

        return query_dict 

    def get_news_api(self):
        return self.newsapi   

    # might be able to use one bool instead
    def get_all_or_breaking(self):
        return self.breaking

class NewsClass:

    def __init__(self, title, url, outlet):
        self.title = title
        self.url = url
        self.outlet = outlet

class GetNewsInfo:

    def __init__(self, api_key, query_dict, breaking):
        self.news_client = NewsApiClient(api_key=api_key)
        self.query_dict = query_dict
        self.breaking = breaking
        self.title_news_dict = {}

    def get_news_articles_json(self):

        if (self.breaking):
            return (self.news_client.get_top_headlines(q = self.query_dict["q"], sources = self.query_dict["sources"]))
        
        else:
            return (self.news_client.get_everything(q = self.query_dict["q"], sources = self.query_dict["sources"], 
                                            from_param=self.query_dict["from_param"], to=self.query_dict["to"]))
            
    def generate_title_news_dict(self):

        my_json = self.get_news_articles_json()
        articles = my_json['articles']

        for article in articles:

            source = article['source']['id']
            url = article['url']
            title = article['title']

            self.title_news_dict[title] = NewsClass(title, url, source)

class PDFGenerator:

    def __init__(self, title_news_dict):
        self.title_news_dict = title_news_dict

    def generate_pdf(self, directory, filename='news.pdf'):
        
        # Create the full file path with a timestamp to ensure uniqueness

        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        name = timestamp + "_" + filename
        file_path = os.path.join(directory, name)

        pdf = FPDF()
        pdf.set_auto_page_break(auto=True, margin=15)
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        
        if (len(self.title_news_dict) == 0):
            print("The inputs you provided yielded no results. Please try again.")
            return

        i = 1

        for title, news in self.title_news_dict.items():

            pdf.set_font("Arial", 'B', 16)
            title_text = f"{i}. {title}".encode('latin1', 'replace').decode('latin1')
            pdf.multi_cell(0, 10, title_text)
            
            pdf.set_font("Arial", size=12)
            source_text = f"Source: {news.outlet}".encode('latin1', 'replace').decode('latin1')
            pdf.multi_cell(0, 10, source_text)
            
            url_text = news.url.encode('latin1', 'replace').decode('latin1')
            pdf.multi_cell(0, 10, url_text)
            
            pdf.ln(10)
            
            i += 1 
        
        pdf.output(file_path)
        print(f"PDF generated: {file_path}")

# Put your API key in the "vars" file

the_api_key = api_key

news = News(api_key=the_api_key)
news_query_dict = news.generate_query()
my_news_api = news.get_news_api()
all_or_breaking = news.get_all_or_breaking()

process_query = GetNewsInfo(api_key = the_api_key, query_dict=news_query_dict, breaking = all_or_breaking)

process_query.generate_title_news_dict()

# Insert your path in the "vars" file

my_path = the_path

generate_pdf = PDFGenerator(process_query.title_news_dict)
generate_pdf.generate_pdf(directory=my_path)