# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import arxiv


class DailyArxivPipeline:
    def __init__(self):
        self.page_size = 100
        self.client = arxiv.Client(self.page_size)
        self.processed_ids = set()  # Set to store processed paper IDs

    def process_item(self, item: dict, spider):
        # Check if paper ID has been processed
        if item["id"] in self.processed_ids:
            spider.logger.info(f"Duplicate paper found: {item['id']}, skipping...")
            return None  # Skip duplicate papers
            
        # Add ID to processed set
        self.processed_ids.add(item["id"])
        
        item["pdf"] = f"https://arxiv.org/pdf/{item['id']}"
        item["abs"] = f"https://arxiv.org/abs/{item['id']}"
        search = arxiv.Search(
            id_list=[item["id"]],
        )
        paper = next(self.client.results(search))
        item["authors"] = [a.name for a in paper.authors]
        item["title"] = paper.title
        item["categories"] = paper.categories
        item["comment"] = paper.comment
        item["summary"] = paper.summary
        spider.logger.info(f"Processing paper: {item['id']}")
        return item
