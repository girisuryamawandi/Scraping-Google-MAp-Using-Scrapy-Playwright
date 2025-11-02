from audioop import add
import scrapy
from scrapy_playwright.page import PageMethod
from playwright_scraper.items import PlaywrightScraperItem

class GooglemapSpider(scrapy.Spider):
    name = "googlemap2"
    allowed_domains = ["www.google.com"]
    start_urls = ["https://www.google.com/maps"]

    async def start(self):
        # GET request
        yield scrapy.Request("https://www.google.com/maps", 
                        meta={"playwright": True,
                        "playwright_include_page": True,
                                "playwright_page_methods": [
                                    PageMethod("wait_for_selector", "xpath=//input[@id='searchboxinput']", timeout=10000),
                                    PageMethod("wait_for_timeout", 1000),
                                    PageMethod("click", "xpath=//input[@id='searchboxinput']"),
                                    PageMethod("wait_for_timeout", 1000),
                                    PageMethod("fill", "xpath=//input[@id='searchboxinput']", "Baso aci di Garut"),
                                    PageMethod("click", "xpath=//button[@id='searchbox-searchbutton']"),
                                    PageMethod("wait_for_timeout", 10000),
                                    PageMethod("evaluate","""
                                                async () => { 
                                                const element = document.querySelector('div[role="feed"]');
                                                var previousHeight = 0;
                                                var currentHeight = element.scrollHeight;
                                                var num_loop = 2 // number of loop
                                                var i = 0
                                                while (i<=num_loop)
                                                {{
                                                    previousHeight = currentHeight;
                                                    element.scrollTop = element.scrollHeight;
                                                    await new Promise(resolve => setTimeout(resolve, 3000));
                                                    currentHeight = element.scrollHeight;
                                                    i++;    
                                                    }}
                                                }
                                            """),
                                    PageMethod("wait_for_timeout", 5000),
                                ]
                        
                        }
                        )

    async def parse(self, response):

        item = PlaywrightScraperItem()

        page = response.meta['playwright_page']
        # await page.wait_for_timeout(2000)
        elements = await page.locator("xpath=//div[@role='feed']/div").all()

        all_elemnet = []

        number = 0
        print('masuk')
        print(len(elements))

        while number < len(elements):
            no_location = 3 + number * 2 
            print('masuk2')
            print(no_location)
            print(f"xpath=//div[@role='feed']/div[{no_location}]")
            all_elemnet.append(f"xpath=//div[@role='feed']/div[{no_location}]")
            print(all_elemnet)
            await page.click(f"xpath=//div[@role='feed']/div[{no_location}]")
            await page.wait_for_timeout(3000)
            google_map_link = await page.locator("xpath=//div[@role='feed']/div[3]//a[@class='hfpxzc']").get_attribute('href') 
            name = await page.locator('h1.DUwDvf.lfPIob').text_content()
            rating = await page.locator("xpath=//div[@class='F7nice ']//span[@role='img']").get_attribute('aria-label')
            rating_count = await page.locator("xpath=//div[@class='F7nice ']/span[2]/span/span").text_content()
            if await page.is_visible("xpath=//div[@class='m6QErb XiKgde ']/div[@class='RcCsl fVHpi w4vB1d NOE9ve M0S7ae AG25L '][1]//div[@class='Io6YTe fontBodyMedium kR99db fdkmkc ']"):
                address = await page.locator("xpath=//div[@class='m6QErb XiKgde ']/div[@class='RcCsl fVHpi w4vB1d NOE9ve M0S7ae AG25L '][1]//div[@class='Io6YTe fontBodyMedium kR99db fdkmkc ']").text_content()
            else:
                address = ''
            if await page.is_visible("xpath=//div[@class='m6QErb XiKgde ']/div[@class='RcCsl fVHpi w4vB1d NOE9ve M0S7ae AG25L '][2]//div[@class='Io6YTe fontBodyMedium kR99db fdkmkc ']"):
                phone_number =  await page.locator("xpath=//div[@class='m6QErb XiKgde ']/div[@class='RcCsl fVHpi w4vB1d NOE9ve M0S7ae AG25L '][2]//div[@class='Io6YTe fontBodyMedium kR99db fdkmkc ']").text_content()
            else:
                phone_number = ''
            number +=1
            await page.wait_for_timeout(1000)
            print(all_elemnet)
            item['google_map_link'] = google_map_link
            item['name'] = name
            item['rating'] = rating
            item['rating_count'] = rating_count
            item['address'] = address
            item['phone_number'] = phone_number
            yield item
           

        print('masuk')
        print(len(elements))
        
        await page.wait_for_timeout(2000)

        print(item)

        await page.close()