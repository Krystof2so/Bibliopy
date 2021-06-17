"""Module de gestion de la base de données."""

import sqlite3

from const import DIR_DATAS


class MyDB:
	"""Classe qui utilise la référence d'un livre, ses données et son nom.
	
	En vue des créer la bases de données et les tables nécessaires.
	"""
	def __init__(self, ref, book_datas, my_biblio):

		self.ref_with_book = ref
		self.book_datas = book_datas
		self.my_biblio = my_biblio

	def add_table_article(self) -> None:
		"""Création de la table 'article'."""
		biblio_database = sqlite3.connect(DIR_DATAS / "bibliography.db")
		cur = biblio_database.cursor()
		dict_mag = {"Identifiant": self.ref_with_book, "Auteur": self.book_datas.get("nom"),
					"Prenom": self.book_datas.get("prenom"), "Titre": self.book_datas.get("ouvrage"),
					"Parution": self.book_datas.get("an_parution"), "Revue": self.book_datas.get("revue"),
					"Pages": f"{self.book_datas.get('pp')} - {self.book_datas.get('pps')}",
					"Theme": self.my_biblio}
		cur.execute("""INSERT INTO Articles VALUES(
					:Identifiant, :Auteur, :Prenom, :Titre,
					:Parution, :Revue, :Pages, :Theme)
					""", dict_mag)
		biblio_database.commit()
		cur.close()
		biblio_database.close()

	def add_table_book(self) -> None:
		"""Création de la table 'livre'."""
		biblio_database = sqlite3.connect(DIR_DATAS / "bibliography.db")
		cur = biblio_database.cursor()
		dict_book = {"Identifiant": self.ref_with_book, "Auteur": self.book_datas.get("nom"),
					 "Prenom": self.book_datas.get("prenom"), "Titre": self.book_datas.get("ouvrage"),
					 "Parution": self.book_datas.get("an_parution"), "Editeur": self.book_datas.get("edition"),
					 "Pages": self.book_datas.get("nb_pages"), "ISBN": self.book_datas.get("ISBN"),
					 "Theme": self.my_biblio}
		cur.execute("""INSERT INTO Livres VALUES(
					:Identifiant, :Auteur, :Prenom, :Titre,
					:Parution, :Editeur, :Pages, :ISBN, :Theme)
					""", dict_book)
		biblio_database.commit()
		cur.close()
		biblio_database.close()


def create_db() -> None:
	"""Creation de la base de données."""
	biblio_database = sqlite3.connect(DIR_DATAS / "bibliography.db")
	cur = biblio_database.cursor()
	# TABLE 'Articles'
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
	# Table 'Livre'
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
	biblio_database.commit()
	cur.close()
	biblio_database.close()
