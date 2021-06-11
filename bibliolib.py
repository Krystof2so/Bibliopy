"""
Classes utiles pour manipuler l'objet "livre" et ses références,
ainsi que les enregistrements.
Classe et méthode pour la manipulation des répertoires de données - Gestion des bibliographies.
"""

import json

from const import DIR_DATAS


class Bibliography:
    """Classe utilisée pour la création de la bibliographie et des répertoires idoines."""
    
    def __init__(self, name_biblio):
        """Initialise.

        Args:
            name_biblio (str): Nom de la bibliographie
        """
        self.name_biblio = name_biblio
        self.dir_biblio = DIR_DATAS / str(name_biblio)
    
    def create_dir_biblio(self):
        """Création des répertoires pour l'enregistrement des données.

        Returns:
            str: Nom de la bibliographie.
        """
        if self.name_biblio in [b.name for b in DIR_DATAS.iterdir() if b.is_dir()]:
            pass
        else: 
            self.dir_biblio.mkdir()
        return self.name_biblio


class BookRef:
    """Classe pour définir la référence d'un livre selon les informations fournies."""
    def __init__(self, book_datas):
        """Initialise.

        Args:
            book_datas (dict): Informations sur un livre saisies par l'utilisateur.
        """
        self.book_datas_dir = book_datas
        self.n_author = book_datas.get("nom")
        self.first_n_author = book_datas.get("prenom")
        self.book_title = book_datas.get("ouvrage")
    
    def __str__(self):
        """Pour l'affichage.

        Returns:
            str: Phrase pour l'affichage.
        """
        return f"'{self.book_title}' écrit par {self.first_n_author} {self.n_author}"
    
    def id_and_ref_title(self):
        """Création de la référence.

        Returns:
            dict: {référence: {données sur le livre}}.
        """
        n = self.n_author[:4]
        p = self.first_n_author[:4]
        t = self.book_title[:4]
        ref = f"{n}{p.lower()}{t.capitalize()}"
        return {ref: self.book_datas_dir}


class SaveBook:
    """Classe pour l'enregistrement des données dans les fichiers idoines."""
    
    def __init__(self, book_data, my_biblio):
        """Initialise.

        Args:
            book_data (dict): Informations sur un livre saisies par l'utilisateur.
            my_biblio (str): Nom de la bibliogrpraphie.
        """
        self.ref = book_data.keys()
        self.dict_info = book_data
        self.my_biblio = my_biblio
        self.file_json = DIR_DATAS / my_biblio / (self.my_biblio + ".json")
    
    def check_json_file(self):
        """Vérification des références contenus dans le fichier .json idoine."""
        if self.file_json.exists():
            pass
        else:
            self.file_json.touch()
            with open(self.file_json, 'w') as file_b:
                json.dump([], file_b, indent=4, ensure_ascii=False)
            
    def save_ref(self):
        """Enregistrement de la référence dans le fichier .json idoine.

        Returns:
            bool: True ou False
        """
        with open(self.file_json, 'r') as file_b:
            checklist = json.loads(file_b.read())
            for k in self.dict_info.keys():
                if k not in checklist:
                    checklist.append(k)
                    with open(self.file_json, 'w') as file_b2:
                        json.dump(checklist, file_b2, indent=4, ensure_ascii=False)
                    return True
                else:
                    return False
    
    def save_livre_data(self):
        # Enregistrer 'self.dict_info' avec SQLite
        pass
