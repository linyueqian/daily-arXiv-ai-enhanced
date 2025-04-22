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
            # 获取论文的类别
            categories = paper.css("span.list-identifier a::text").getall()
            # 只保留我们感兴趣的类别
            valid_categories = [cat for cat in categories if cat in self.target_categories]
            
            if valid_categories:  # 如果论文属于我们感兴趣的类别
                yield {
                    "id": paper.css("a[title='Abstract']::attr(href)")
                    .get()
                    .split("/")[-1],  # 提取论文链接
                    "categories": valid_categories  # 保存有效的类别
                }
