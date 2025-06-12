import scrapy
import pandas as pd
import re
import html

NUMBER_ARTICLES_BY_PAGE = 500
MAX_ARTICLES = 35000
START = 0
BASE_PAGE_URL = 'https://repositorio.utfpr.edu.br'
URL_QUERY = '/jspui/simple-search?location=&query=&rpp={page_size}&sort_by=dc.date.issued_dt&order=DESC&etal=0&submit_search=Atualizar&start={start}'


class TextCrawler(scrapy.Spider):
    name = 'utfpr_riut_spider'
    start_urls = [BASE_PAGE_URL + URL_QUERY.format(page_size=NUMBER_ARTICLES_BY_PAGE, start=START)]
    loop = 0
    start = START
        
    def parse(self, response):
        # taking all the url of blog posts
        print('start = ', self.start)
        self.start += NUMBER_ARTICLES_BY_PAGE
        urls = response.css('a[href*="/jspui/handle/"]').xpath('@href').extract()
        quantidade_mensagem = response.css('.discovery-result-pagination > .alert::text').extract_first()
        qtd = re.findall(r"\d+", quantidade_mensagem)
        pos = int(qtd[0])
        last = int(qtd[1])
        max = int(qtd[2])
        print("quantidade =", qtd)
        for url in urls:
            yield response.follow(url, callback = self.getContent)

        if(pos < MAX_ARTICLES and last < max):
            yield scrapy.Request(BASE_PAGE_URL + URL_QUERY.format(page_size=NUMBER_ARTICLES_BY_PAGE, start=last+NUMBER_ARTICLES_BY_PAGE), self.parse)

    def proccess_text(self, text):
        if text == None:
            return None
        return html.unescape(text)
        
    def getContent(self, response):
        # in each blog post take all text
        self.loop += 1
        
        title = self.proccess_text(response.css('.metadataFieldValue.dc_title::text').extract_first())
        title_alt = self.proccess_text(response.css('.metadataFieldValue.dc_title_alternative::text').extract_first())
        authors = response.css('.metadataFieldValue.dc_creator > a::text').extract()
        orientador1 = self.proccess_text(response.css('.metadataFieldValue.dc_contributor_advisor1::text').extract_first())
        orientador2 = self.proccess_text(response.css('.metadataFieldValue.dc_contributor_advisor2::text').extract_first())
        palavras_chave = self.proccess_text(response.css('.metadataFieldValue.dc_subject::text').extract())
        data = self.proccess_text(response.css('.metadataFieldValue.dc_date_issued::text').extract_first())
        editor = self.proccess_text(response.css('.metadataFieldValue.dc_publisher::text').extract_first())
        campus = self.proccess_text(response.css('.metadataFieldValue.dc_publisher_local::text').extract_first())
        citacao = self.proccess_text(response.css('.metadataFieldValue.dc_identifier_citation::text').extract_first())
        resumo = self.proccess_text(response.css('.metadataFieldValue.dc_description_resumo::text').extract_first())
        abstract = self.proccess_text(response.css('.metadataFieldValue.dc_description_abstract::text').extract_first())
        uri = response.css('.metadataFieldValue.dc_identifier_uri > a::attr(href)').extract_first()
        pdf_uri = response.css('a[href*="/jspui/bitstream/1/"]').xpath('@href').extract_first()
        
        yield {
            'title': title,
            'title_alt': title_alt,
            'authors': authors,
            'advisor1': orientador1,
            'advisor2': orientador2,
            'keywords': palavras_chave,
            'date': data,
            'publisher': editor,
            'campus': campus,
            'citation': citacao,
            'resumo': resumo,
            'abstract': abstract,
            'uri': uri,
            'pdf_uri': BASE_PAGE_URL + pdf_uri,
        }
