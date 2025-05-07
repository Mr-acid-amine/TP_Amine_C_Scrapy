import scrapy
import pandas as pd
from scrapy_kbo_tp.items import NbbItem
from scrapy_kbo_tp.utils import lire_numero_entreprises

class ConsultSpider(scrapy.Spider):
    name = "consult_spider"
    allowed_domains = ["consult.cbso.nbb.be"]

    def start_requests(self):
        for numero in lire_numero_entreprises():
            url = f"https://consult.cbso.nbb.be/consult-enterprise/{numero}"
            yield scrapy.Request(url, callback=self.parse, meta={"numero": str(numero)})

    def parse(self, response):
        item = NbbItem()
        item["numero"] = response.meta["numero"]
        item["comptes_annuels"] = []

        for block in response.xpath("//div[contains(@class, 'publication-block')]"):
            compte = {
                "titre": block.xpath(".//h3/text()").get(),
                "reference": block.xpath(".//span[contains(text(),'Référence')]/following-sibling::span/text()").get(),
                "date_depot": block.xpath(".//span[contains(text(),'Déposé le')]/following-sibling::span/text()").get(),
                "fin_exercice": block.xpath(".//span[contains(text(),'Fin de l’exercice')]/following-sibling::span/text()").get(),
                "langue": block.xpath(".//span[contains(text(),'Langue')]/following-sibling::span/text()").get()
            }
            item["comptes_annuels"].append(compte)

        yield item
