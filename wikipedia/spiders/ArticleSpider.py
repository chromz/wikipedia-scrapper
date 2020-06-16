from bs4 import BeautifulSoup
import scrapy
from nltk import word_tokenize, sent_tokenize

class ArticleSpider(scrapy.Spider):
    name = "articles"
    start_urls = [
        "https://en.wikipedia.org/wiki/Wikipedia:Featured_articles"
    ]

    token_count = 0

    def parse(self, response):
        for art_list in response.css("span.featured_article_metadata.has_been_on_main_page a"):
            if self.token_count >= 1000000:
                break
            next_article = art_list.css("a::attr(href)").get()
            yield response.follow(next_article, callback=self.parse_article)

    def parse_article(self, response):
        text = ""
        html = ""
        for paragraphs in response.css("div.mw-body-content p"):
            html += paragraphs.get()
        soup = BeautifulSoup(html)
        text = soup.get_text()
        tokenized_text = [word_tokenize(sent) for sent in sent_tokenize(text)]
        self.token_count += len(tokenized_text)
        print(self.token_count)
