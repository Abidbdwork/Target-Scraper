import json
import re
import html2text
import scrapy


class TargetScraper(scrapy.Spider):
    name = "target"
    start_urls = ['https://www.target.com/p/apple-iphone-13-pro-max/-/A-84616123?preselect=84240109#lnk=sametab']

    def parse(self, response):
        self.api_keys = self.Api_Key_Parser(response)
        self.product_ids = self.Url_To_ProductId(response.url)
        self.api_key_in = 0
        yield scrapy.Request(self.Product_Details_Url(self.product_ids['product_id'], self.api_keys[self.api_key_in]),
                             callback=self.Product_Details_Parser)

    def QA_Parser(self, Response):
        qa_json = json.loads(Response.text)
        results = qa_json['results']
        questions = None
        if results:
            questions = [q['text'] for q in results if q.get('text')]
        print("questions:-------->", questions)
        return {"questions": questions}

    def Product_Details_Parser(self, Response):
        # print("Product Details parser:---", json.loads(response.url))
        Selected_id = self.product_ids.get('s_product')
        product_json = json.loads(Response.text)
        print(product_json)
        product_info = product_json['data']['product'].get('children', {})
        if product_info and Selected_id:
            for info in product_info:
                if info.get('tcin', '') == Selected_id:
                    product_info = info
                    break
        elif product_info and Selected_id is None:
            product_info = product_info[0]
        product_dsh = product_info.get('item', {}).get('product_description', {})
        specifications = '\n'.join([html2text.html2text(line) for line in product_dsh.get('bullet_descriptions', [])])
        title = product_dsh.get('title')
        description = html2text.html2text(product_dsh.get('downstream_description', ''))
        highlights = html2text.html2text(product_dsh.get('soft_bullet_description', ''))
        price = product_info.get('price', {}).get('current_retail')
        images = product_info.get('item', {}).get('enrichment', {}).get('images', {}).get('content_labels')
        image_urls = [url.get('image_url') for url in images]
        print("Title:-------->", title)
        print("Images:-------->", image_urls)
        print("price:-------->", price)
        print("Description:-------->", description)
        print("Highlights:-------->", highlights)
        print("Specifications:-------->", specifications)
        print(self.product_ids, self.api_keys[self.api_key_in])
        qa_url = self.QA_Url(self.product_ids['product_id'], self.api_keys[self.api_key_in])
        yield scrapy.Request(qa_url, callback=self.QA_Parser)
        yield {'title': title, "image_urls": image_urls, 'price': price, 'description': description,
               'highlights': highlights,
               'specifications': specifications}

    def Api_Key_Parser(self, Response):
        Pattern = r"(?:\"apikey\":\B.\w+\W)"
        All_Keys = [key.split(':')[-1].strip('"') for key in re.findall(Pattern, Response.text, re.IGNORECASE)]
        Api_Keys = []
        for key in All_Keys:
            if len(key) == 40 and key not in Api_Keys:
                Api_Keys.append(key)
        return Api_Keys

    def Url_To_ProductId(self, Url):
        ids = Url.split('/-/')[-1]
        product_id = ids.split('?')[0].split('-')[-1]
        if ids.__contains__('preselect='):
            selected_product = ids.split('preselect=')[-1].split('#')[0]
        else:
            selected_product = None
        return {'product_id': product_id, 's_product': selected_product}

    def QA_Url(self, Product_Id, Api_Key):
        Page = 0
        Size = 100
        return f"https://r2d2.target.com/ggc/Q&A/v1/question-answer?type=product&questionedId={Product_Id}&page={Page}&size={Size}&key={Api_Key}"

    def Product_Details_Url(self, Product_Id, Api_Key):
        return f"https://redsky.target.com/redsky_aggregations/v1/web/pdp_client_v1?tcin={Product_Id}&pricing_store_id=3991&key={Api_Key}"

