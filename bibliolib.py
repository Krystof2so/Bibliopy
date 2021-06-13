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
    
    def __init__(self, my_biblio):
        """Initialise.

        Args:
            my_biblio (str): Nom de la bibliographie
        """
        self.my_biblio = my_biblio
        self.dir_biblio = DIR_DATAS / str(my_biblio)
    
    def create_dir_biblio(self) -> str:
        """Création des répertoires pour l'enregistrement des données.

        Returns:
            str: Nom de la bibliographie.
        """
        # in liste des répertoires dans .bibliopyDatas
        if self.my_biblio in [b.name for b in DIR_DATAS.iterdir() if b.is_dir()]:
            pass
        else: 
            self.dir_biblio.mkdir()
        return self.my_biblio


class BookRef:
    """Classe pour définir la référence d'un livre selon les informations fournies."""
    def __init__(self, book_datas):
        """Initialise.

        Args:
            book_datas (dict): Informations sur le livre saisi par l'utilisateur.
        """
        self.book_datas = book_datas
        self.type_doc = book_datas.get("document")
        self.n_author = book_datas.get("nom")
        self.first_n_author = book_datas.get("prenom")
        self.book_title = book_datas.get("ouvrage")
        self.year = book_datas.get("an_parution")
        self.mag = book_datas.get("revue")
        self.start_page = book_datas.get("pp")
        self.end_page = book_datas.get("pps")
        self.editing = book_datas.get("edition")
        self.nb_pages = book_datas.get("nb_pages")
        self.isbn = book_datas.get("ISBN")
    
    def __str__(self):
        """Pour l'affichage.

        Returns:
            str: Phrase pour l'affichage.
        """
        return f"'{self.book_title}' écrit par {self.first_n_author} {self.n_author}"
    
    def id_and_ref_title(self):
        """Création de la référence.

        Returns:
            str: référence livre.
        """
        td = self.type_doc
        n = self.n_author[:4]
        p = self.first_n_author[:4]
        t = self.book_title[:4]
        y = self.year
        ref = f"{td}{n}{p.lower()}{y}{t.capitalize()}"
        return ref


class SaveBook(BookRef):
    """Classe pour l'enregistrement des données dans les fichiers idoines."""
    
    def __init__(self, ref_with_book, my_biblio, book_datas):
        """Initialise.

        Args:
            ref_with_book (str): Référence du livre.
        """
        super().__init__(book_datas)
        self.book_datas = book_datas
        self.my_biblio = my_biblio
        self.ref_with_book = ref_with_book
        self.file_json = DIR_DATAS / self.my_biblio / (self.my_biblio + ".json")
    
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
            if self.ref_with_book not in checklist:
                checklist.append(self.ref_with_book)
                with open(self.file_json, 'w') as file_b2:
                    json.dump(checklist, file_b2, indent=4, ensure_ascii=False)
                return True
            else:
                return False
    
    def save_livre_data(self):
        """Pour l'enregistrement dans la base de données (SQLite).
        
        Nécessité de retravailler cette fonction...
        """
        biblio_database = sqlite3.connect(DIR_DATAS / "bibliography.db")
        cur = biblio_database.cursor()
        if self.book_datas.get("document") == "A-":
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
            dict_mag = {"Identifiant": self.ref_with_book, "Auteur": self.book_datas.get("nom"),
                      "Prenom": self.book_datas.get("prenom"), "Titre": self.book_datas.get("ouvrage"),
                      "Parution": self.book_datas.get("an_parution"), "Revue": self.book_datas.get("revue"),
                      "Pages": f"{self.book_datas.get('pp')} - {self.book_datas.get('pps')}",
                      "Theme": self.my_biblio}
            cur.execute("""
                        INSERT INTO Articles VALUES
                        (:Identifiant, :Auteur, :Prenom, :Titre, 
                        :Parution, :Revue, :Pages, :Theme)
                        """, dict_mag)
        elif self.book_datas.get("document") == "L-":
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
            dict_book = {"Identifiant": self.ref_with_book, "Auteur": self.book_datas.get("nom"),
                         "Prenom": self.book_datas.get("prenom"), "Titre": self.book_datas.get("ouvrage"),
                         "Parution": self.book_datas.get("an_parution"), "Editeur": self.book_datas.get("edition"),
                         "Pages": self.book_datas.get("nb_pages"), "ISBN": self.book_datas.get("ISBN"),
                         "Theme": self.my_biblio}
            cur.execute("""
                        INSERT INTO Livres VALUES
                        (:Identifiant, :Auteur, :Prenom, :Titre, 
                        :Parution, :Editeur, :Pages, :ISBN, :Theme)
                        """, dict_book)
        biblio_database.commit()
        cur.close()        
        biblio_database.close()
