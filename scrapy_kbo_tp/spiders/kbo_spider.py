import scrapy
from scrapy_kbo_tp.items import KboItem
from scrapy_kbo_tp.utils import lire_numero_entreprises

class KboSpider(scrapy.Spider):
    name = 'kbo_spider'

    def start_requests(self):
        for num in lire_numero_entreprises():
            url = (
                'https://kbopub.economie.fgov.be'
                '/kbopub/toonondernemingps.html'
                f'?language=fr&ondernemingsnummer={num}'
            )
            yield scrapy.Request(
                url,
                callback=self.parse,
                headers={'Accept-Language': 'fr'},
                meta={'num': num}
            )

    def parse(self, response):
        def extract(french_label):
            """
            Extrait uniquement le texte associé à un label en français.
            """
            txt = response.xpath(
                f'//td[normalize-space()="{french_label}"]'
                '/following-sibling::td[1]//text()'
            ).get()
            return txt.strip() if txt else ''

        item = KboItem()
        item['EnterpriseNumber'] = response.meta['num']

        # ---- Généralités FR
        item['generalites'] = {
            'nom':             extract('Dénomination:'),
            'statut':          extract('Statut:'),
            'forme_juridique': extract('Forme légale:'),
            'date_debut':      extract('Date de début:'),
            'adresse': [
                line.strip()
                for line in response.xpath(
                    '//td[normalize-space()="Adresse du siège:"]'
                    '/following-sibling::td[1]//text()'
                ).getall()
                if line.strip()
            ]
        }

        # ---- Sections sans données ----
        item['fonctions']     = []
        item['capacites']     = []
        item['autorisations'] = []
        item['nace_codes']    = []

        # ---- Qualités (FR uniquement) ----
        qual_trs = response.xpath(
            '//tr[td/h2[normalize-space(.)="Qualités"]]/following-sibling::tr'
        )
        qualites = []
        for tr in qual_trs:
            if tr.xpath('td/h2[normalize-space(.)="Autorisations"]'):
                break
            for txt in tr.xpath('.//td//text()').getall():
                t = txt.strip()
                if t and not t.lower().startswith('pas de données'):
                    qualites.append(t)
        item['qualites'] = qualites

        # ---- Données financières (FR uniquement) ----
        item['donnees_financieres'] = {
            'reunion_annuelle': extract('Assemblée générale'),
            'fin_exercice':     extract("Date de fin de l'année comptable")
        }

        # ---- Liens ----
        item['liens_entites']  = []
        item['liens_externes'] = response.css('a.external::attr(href)').getall()

        yield item
