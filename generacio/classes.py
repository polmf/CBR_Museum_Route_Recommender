
class Autor:
    def __init__(self, nom=None, epoca=None, estils=None, nacionalitat=None, es_troba_a=None):
        self.nom = nom
        self.epoca = epoca if epoca else []
        self.estils = estils if estils else []
        self.nacionalitat = nacionalitat
        self.es_troba_a = es_troba_a

    def to_dict(self):
        return {
            'nom': self.nom,
            'epoca': self.epoca,
            'estils': self.estils,
            'nacionalitat': self.nacionalitat,
            'es_troba_a': self.es_troba_a
        }

    @staticmethod
    def from_dict(data):
        return Autor(
            nom=data.get('nom'),
            epoca=data.get('epoca'),
            estils=data.get('estils'),
            nacionalitat=data.get('nacionalitat'),
            es_troba_a=data.get('es_troba_a')
        )



class Quadre:
    def __init__(self, nom=None, dim_cm2=None, any=None, autor=None, estil=None, complexitat=None, rellevancia=None, constituent_id=None, sala=None):
        self.nom = nom
        self.dim_cm2 = dim_cm2
        self.any = any
        self.autor = autor
        self.estil = estil
        self.complexitat = complexitat
        self.rellevancia = rellevancia
        self.constituent_id = constituent_id
        self.sala = sala

    def to_dict(self):
        return {
            'nom': self.nom,
            'dim_cm2': self.dim_cm2,
            'any': self.any,
            'autor': self.autor,
            'estil': self.estil,
            'complexitat': self.complexitat,
            'relevancia': self.rellevancia,
            'constituent_id': self.constituent_id,
            'sala': self.sala
        }

    @staticmethod
    def from_dict(data):
        return Quadre(
            nom=data.get('nom'),
            dim_cm2=data.get('dim_cm2'),
            any=data.get('any'),
            autor=data.get('autor'),
            estil=data.get('estil'),
            complexitat=data.get('complexitat'),
            rellevancia=data.get('relevancia'),
            constituent_id=data.get('constituent_id'),
            sala=data.get('sala')
        )


class Sala:
    def __init__(self, sala=None, conte_estil=None):
        self.sala = sala
        self.conte_estil = conte_estil
        self.quadres = []

    def afegir_quadre(self, quadre):
        self.quadres.append(quadre)

    def to_dict(self):
        return {
            'sala': self.sala,
            'conte_estil': self.conte_estil,
            'quadres': [quadre.to_dict() for quadre in self.quadres]
        }

    @staticmethod
    def from_dict(data):
        sala = Sala(
            sala=data.get('sala'),
            conte_estil=data.get('conte_estil')
        )
        # Aquí añadimos los quadres, deserializándolos desde el diccionario
        for quadre_data in data.get('quadres', []):
            sala.afegir_quadre(Quadre.from_dict(quadre_data))
        return sala



class Visitant:
    def __init__(self, visites=None, companyia=None, dies=None, hores=None, edat=None, estudis=None, coneixement=None, quizz=None, interessos_autor=None, interessos_estils=None):
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
        self.feedback = None

    def get_visites(self):
        return self.visites

    def get_companyia(self):
        return self.companyia

    def get_dies(self):
        return self.dies

    def get_hores(self):
        return self.hores

    def get_edat(self):
        return self.edat

    def get_estudis(self):
        return self.estudis

    def get_coneixements(self):
        return self.coneixements

    def get_quizz(self):
        return self.quizz

    def get_interessos_autor(self):
        return self.interessos_autor

    def get_interessos_estils(self):
        return self.interessos_estils

    def get_feedback(self):
        return self.feedback
