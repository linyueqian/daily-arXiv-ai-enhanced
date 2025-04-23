import scrapy
import os


class ArxivSpider(scrapy.Spider):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 默认类别与配置文件保持一致
        self.target_categories = os.environ.get("CATEGORIES", "cs.CV, cs.CL").split(",")
        self.target_categories = list(map(str.strip, self.target_categories))
        self.start_urls = [
            f"https://arxiv.org/list/{cat}/new" for cat in self.target_categories
        ]  # 起始URL（计算机科学领域的最新论文）

    name = "arxiv"  # 爬虫名称
    allowed_domains = ["arxiv.org"]  # 允许爬取的域名

    def parse(self, response):
        # 提取每篇论文的信息
        for paper in response.css("dl dt"):
            paper_id = paper.css("a[title='Abstract']::attr(href)").get()
            
            if paper_id:  # 确保我们有有效的论文ID
                paper_id = paper_id.split("/")[-1]
                # Get the corresponding dd element which contains author and other info
                dd = paper.xpath('./following-sibling::dd[1]')
                
                # Extract categories text content
                subjects_div = dd.css('div.list-subjects')
                subjects_text = subjects_div.xpath('string()').get()
                
                # Check if any of our target categories are in the subjects text
                categories = []
                if subjects_text:
                    for cat in self.target_categories:
                        if cat in subjects_text:
                            categories.append(cat)
                
                if categories:  # 如果论文属于我们感兴趣的类别
                    self.logger.info(f"Found paper: {paper_id} with categories: {categories}")
                    
                    yield {
                        "id": paper_id,
                        "pdf": f"https://arxiv.org/pdf/{paper_id}",
                        "abs": f"https://arxiv.org/abs/{paper_id}",
                        "authors": dd.css("div.list-authors a::text").getall(),
                        "title": dd.css("div.list-title::text").get().strip() if dd.css("div.list-title::text").get() else "",
                        "categories": categories,
                        "comment": dd.css("div.list-comments::text").get(),
                        "summary": ""  # We'll get this from the API in the pipeline
                    }
