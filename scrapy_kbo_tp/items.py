import scrapy

# 🕷 Spider 1 : KBO – Informations générales
class KboItem(scrapy.Item):
    numero = scrapy.Field()  # numéro d’entreprise
    EnterpriseNumber = scrapy.Field()
    generalites = scrapy.Field()
    fonctions = scrapy.Field()
    capacites = scrapy.Field()
    qualites = scrapy.Field()
    autorisations = scrapy.Field()
    nace_codes = scrapy.Field()
    donnees_financieres = scrapy.Field()
    liens_entites = scrapy.Field()
    activites = scrapy.Field()    
    liens_externes = scrapy.Field()

# 🕷 Spider 2 : eJustice – Publications Moniteur Belge
class EjusticeItem(scrapy.Item):
    numero = scrapy.Field()  # numéro d’entreprise
    publications = scrapy.Field()  # liste de publications
    

# 🕷 Spider 3 : NBB – Comptes annuels
class NbbItem(scrapy.Item):
    numero = scrapy.Field()  # numéro d’entreprise
    comptes_annuels = scrapy.Field()  # liste de comptes annuels
    
