import scrapy
from scrapy_kbo_tp.items import EjusticeItem  # Assurez-vous d'importer votre item
from scrapy_kbo_tp.utils import lire_numero_entreprises  # Import de la fonction pour récupérer les numéros d'entreprises

class EjusticeSpider(scrapy.Spider):
    name = "ejustice_spider"
    allowed_domains = ["ejustice.just.fgov.be"]
    
    def start_requests(self):
        for numero in lire_numero_entreprises():
            url = f"https://www.ejustice.just.fgov.be/cgi_tsv/list.pl?btw={numero}&lang=fr&page=1"
            yield scrapy.Request(
                url,
                callback=self.parse,
                meta={"numero": numero},
                headers={"Accept-Language": "fr"}
            )

    def parse(self, response):
        # Initialisation de l'item
        item = EjusticeItem()
        item["numero"] = response.meta["numero"]

        item["publications"] = []
        # Extraction des publications
        for block in response.css("div.list-item"):
            # 1) Extraire le titre de la publication depuis <p class="list-item--subtitle">
            subtitle = block.css("p.list-item--subtitle font::text").get()

            if subtitle:
                # 2) Extraction des autres informations sous forme de liste
                lines = block.css("a.list-item--title::text").getall()
                lines = [line.strip() for line in lines if line.strip()]  # Nettoyage des espaces

                # Vérifier si les informations nécessaires sont présentes
                if len(lines) >= 4:
                    adresse = lines[0] 
                    bce = lines[1]  
                    type_pub = lines[2] 
                    date_ref = lines[3]  

                    # On prépare l'objet publication
                    publication = {
                        "titre": subtitle,
                        "adresse": adresse,
                        "bce": bce,
                        "type": type_pub,
                        "date_ref": date_ref,
                    }

                    # Extraction du lien de l'image, si présent
                    image_url = block.css("a.standard::attr(href)").get()
                    if image_url:
                        publication["image"] = response.urljoin(image_url)
                    else:
                        publication["image"] = None
                    # Ajout de la publication à la liste
                    item["publications"].append(publication)

        # Pagination : passer à la page suivante si elle existe
        next_page = response.css("a.pagination-next::attr(href)").get()
        if next_page:
            yield response.follow(next_page, callback=self.parse, meta={"numero": item["numero"]})
        else:
            # Dernière page, renvoyer l'item avec les publications
            yield item



        
        

