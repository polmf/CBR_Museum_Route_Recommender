class Autor:
    def __init__(self, nom = None, epoca=None, estils=None, nacionalitat=None, es_troba_a=None):
        self.nom = nom
        self.epoca = epoca if epoca else []
        self.estils = estils if estils else []
        self.nacionalitat = nacionalitat
        self.es_troba_a = es_troba_a

class Quadre:
    def __init__(self, nom=None, alçada=None, amplada=None, any=None, autor=None, sala=None, complexitat=None, conservacio=None, 
                 tema=None, epoca=None, estil=None, rellevancia=None):
        self.nom = nom
        self.alçada = alçada
        self.amplada = amplada
        self.any = any
        self.autor = autor
        self.sala = sala
        self.complexitat = complexitat
        self.conservacio = conservacio
        self.tema = tema
        self.epoca = epoca
        self.estil = estil
        self.rellevancia = rellevancia

class Sala:
    def __init__(self, sala=None, conte_estil=None, contigua=None, es_troba_a=None):
        self.sala = sala
        self.conte_estil = conte_estil
        self.contigua = contigua if contigua else []
        self.es_troba_a = es_troba_a

class Visitant:
    def __init__(self, visites=None, companyia=None, dies=None, hores=None, edat=None, estudis=None,  coneixement=None, quizz=None, interessos_autor=None, interessos_estils=None):
        self.visites = visites
        self.companyia = companyia
        self.dies = dies
        self.hores = hores
        self.edat = edat
        self.estudis = estudis
        self.coneixements = coneixement
        self.quizz = quizz
        self.interessos_autor = interessos_autor if interessos_autor else []
        self.interessos_estils = interessos_estils if interessos_estils else []
