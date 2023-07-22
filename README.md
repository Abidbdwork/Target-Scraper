This one scrape data using api
## Requirements
    
    $ pip install scrapy
    $ pip install html2text


## Running the spiders

You can run a spider using the `scrapy crawl` command, such as:

    $ scrapy crawl target

If you want only output data, you can pass the `--nolog` option:
    
    $ scrapy crawl target --nolog

If you want to save the scraped data to a file, you can pass the `-o` option:
    
    $ scrapy crawl target -o result.json
