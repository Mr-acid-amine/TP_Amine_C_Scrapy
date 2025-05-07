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
        def extract(possible_labels):
            """
            Essaie chaque label de la liste possible_labels (FR + NL)
            et renvoie le premier texte trouvé (strip()), ou ''.
            """
            for label in possible_labels:
                txt = response.xpath(
                    f'//td[normalize-space()="{label}"]'
                    '/following-sibling::td[1]//text()'
                ).get()
                if txt:
                    return txt.strip()
            return ''
 
        item = KboItem()
        item['EnterpriseNumber'] = response.meta['num']
 
        # ---- Généralités (bilingue) ----
        item['generalites'] = {
            'nom':             extract(['Dénomination:', 'Naam:']),
            'statut':          extract(['Statut:',       'Status:']),
            'forme_juridique': extract(['Forme légale:', 'Rechtstoestand:']),
            'date_debut':      extract(['Date de début:','Begindatum:']),
            'adresse': [
                line.strip()
                for line in response.xpath(
                    # union FR + NL
                    '//td[normalize-space()="Adresse du siège:"]'
                    '/following-sibling::td[1]//text()'
                    ' | '
                    '//td[normalize-space()="Adres van de zetel:"]'
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
 
        # ---- Qualités / Hoedanigheden (dynamique) ----
        # repérer le <tr> du titre (FR ou NL)…
        qual_trs = response.xpath(
            '//tr[td/h2[normalize-space(.)="Qualités" or normalize-space(.)="Hoedanigheden"]]'
            '/following-sibling::tr'
        )
        qualites = []
        for tr in qual_trs:
            # dès qu'on tombe sur l'entête Autorisations/Toelatingen on arrête
            if tr.xpath(
                'td/h2[normalize-space(.)="Autorisations" or normalize-space(.)="Toelatingen"]'
            ):
                break
            # sinon on collecte tous les textes non vides
            for txt in tr.xpath('.//td//text()').getall():
                t = txt.strip()
                if t and not t.lower().startswith('pas de données'):
                    qualites.append(t)
        item['qualites'] = qualites
 
        # ---- Données financières (bilingue) ----
        item['donnees_financieres'] = {
            'reunion_annuelle': extract(['Assemblée générale', 'Jaarvergadering']),
            'fin_exercice':    extract(["Date de fin de l'année comptable", 'Einddatum boekjaar'])
        }
 
        # ---- Liens ----
        item['liens_entites']  = []
        item['liens_externes'] = response.css('a.external::attr(href)').getall()
 
        yield item