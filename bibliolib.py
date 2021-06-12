"""
Classes utiles pour manipuler l'objet "livre" et ses références,
ainsi que les enregistrements.
Classe et méthode pour la manipulation des répertoires de données - Gestion des bibliographies.
"""

import json
import sqlite3

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
        self.book_datas = book_datas
        self.type_doc = book_datas.get("document")
        self.n_author = book_datas.get("nom")
        self.first_n_author = book_datas.get("prenom")
        self.book_title = book_datas.get("ouvrage")
        self.year = book_datas.get("an_parution")
    
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
        td = self.type_doc
        n = self.n_author[:4]
        p = self.first_n_author[:4]
        t = self.book_title[:4]
        y = self.year
        ref = f"{td}{n}{p.lower()}{y}{t.capitalize()}"
        return {ref: self.book_datas}


class SaveBook:
    """Classe pour l'enregistrement des données dans les fichiers idoines."""
    
    def __init__(self, book_data, my_biblio):
        """Initialise.

        Args:
            book_data (dict): Informations sur un livre saisies par l'utilisateur.
            my_biblio (str): Nom de la bibliogrpraphie.
        """
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
        """Pour l'enregistrement dans la base de données (SQLite).
        
        Nécessité de retravailler cette fonction...
        """
        dict_datadb = (list(self.dict_info.values())[0])
        ref_of_book = (list(self.dict_info.keys())[0])
        biblio_database = sqlite3.connect(DIR_DATAS / "bibliography.db")
        cur = biblio_database.cursor()
        if dict_datadb.get("document") == "A-":
            cur.execute("""
                        CREATE TABLE IF NOT EXISTS Articles(
                            Identifiant TEXT,
                            Auteur TEXT,
                            Prenom TEXT,
                            Titre TEXT,
                            Parution INTEGER,
                            Revue TEXT,
                            Pages INTEGER,
                            Theme TEXT
                            )
                        """)
            dict_mag = {"Identifiant": ref_of_book, "Auteur": dict_datadb.get("nom"),
                      "Prenom": dict_datadb.get("prenom"), "Titre": dict_datadb.get("ouvrage"),
                      "Parution": dict_datadb.get("an_parution"), "Revue": dict_datadb.get("revue"),
                      "Pages" : f"{dict_datadb.get('pp')} - {dict_datadb.get('pps')}",
                      "Theme": self.my_biblio}
            cur.execute("""
                        INSERT INTO Articles VALUES
                        (:Identifiant, :Auteur, :Prenom, :Titre, 
                        :Parution, :Revue, :Pages, :Theme)
                        """,dict_mag)
        elif dict_datadb.get("document") == "L-":
            cur.execute("""
                        CREATE TABLE IF NOT EXISTS Livres(
                            Identifiant TEXT,
                            Auteur TEXT,
                            Prenom TEXT,
                            Titre TEXT,
                            Parution INTEGER,
                            Editeur TEXT,
                            Pages INTEGER,
                            ISBN TEXT,
                            Theme TEXT
                            )
                        """)
            dict_book = {"Identifiant": ref_of_book, "Auteur": dict_datadb.get("nom"),
                         "Prenom": dict_datadb.get("prenom"), "Titre": dict_datadb.get("ouvrage"),
                         "Parution": dict_datadb.get("an_parution"), "Editeur": dict_datadb.get("edition"),
                         "Pages" : dict_datadb.get("nb_pages"), "ISBN": dict_datadb.get("ISBN"),
                         "Theme": self.my_biblio}
            cur.execute("""
                        INSERT INTO Livres VALUES
                        (:Identifiant, :Auteur, :Prenom, :Titre, 
                        :Parution, :Editeur, :Pages, :ISBN, :Theme)
                        """,dict_book)
        biblio_database.commit()
        cur.close()        
        biblio_database.close()
