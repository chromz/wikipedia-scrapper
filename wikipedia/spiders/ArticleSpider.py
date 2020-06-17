from bs4 import BeautifulSoup
import scrapy
from nltk import RegexpTokenizer, sent_tokenize

class ArticleSpider(scrapy.Spider):
    name = "articles"
    start_urls = [
        "https://en.wikipedia.org/wiki/Wikipedia:Featured_articles"
    ]

    tokens_count = 0
    document_num = 0


    def parse(self, response):
        for art_list in response.css("span.featured_article_metadata.has_been_on_main_page a"):
            next_article = art_list.css("a::attr(href)").get()
            yield response.follow(next_article, callback=self.parse_article)

    def parse_article(self, response):
        print(self.tokens_count)
        if self.tokens_count >= 1000000:
            raise scrapy.exceptions.CloseSpider("Token limit reached")
        text = ""
        html = ""
        for paragraphs in response.css("div.mw-body-content p"):
            html += paragraphs.get()
        soup = BeautifulSoup(html)
        text = soup.get_text()
        tokenizer = RegexpTokenizer(r"\w+")
        tokenized_text = []
        for sent in sent_tokenize(text):
            tokenized_text += tokenizer.tokenize(sent)
        self.tokens_count += len(tokenized_text)
        with open(f"documents/doc_{self.document_num}.txt", "w+") as f:
            f.write(" ".join(tokenized_text))
        self.document_num += 1
