# sds_scrape
Uses scrapy/selenium to scrape the internet for SDS using a csv file loaded with location, name, cas, manufacturer.

This project was based on the need to maintain RTK/OSHA standards of having a physical SDS in every room located at my organization. 

Using an inventory list in a csv file with rows containing room/location, name of chemical, cas number, and manufacturer, this webcrawler (sds_scrape.py) was able to find, download and rename pdfs. 

The second script (pdf_spread.py) is able to take the location and item and create folders for each location and fill it with the containing chemical SDS's. 
