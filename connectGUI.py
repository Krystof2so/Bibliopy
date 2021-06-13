"""Fichier provisoire qui sert pour l'instant à faire tourner le programme en CLI.
Modifications à prévoir en vue de de connecter ces actions à une app GUI.
"""

import bibliolib as biblib


# PushButton "Créer bibliographie"
def run_bibliopy() -> str:
	"""Créer un bibliographie.

    Returns:
        str: nom de la bibliographie.
    """
	my_biblio = biblib.Bibliography(input("Nom de la bibliographie que vous voulez créer: "))  # A modifier pour le GUI
	return my_biblio.create_dir_biblio()


# PushButton "Saisir livre"
def btn_input_book(my_biblio):
	"""Fonction lancer l'enregistrer des informations fournies pour un livre.

    Args:
        my_biblio (str): Ensemble des informartions relatives à un livre.
    """
	donnes_du_livre = enter_book()
	print(donnes_du_livre)
	the_book = biblib.BookRef(donnes_du_livre)
	# enter_book() retourne le dictionnaire des données saisies par l'utilisateur
	registration_request = input(f"Souhaitez-vous enregistrer l'ouvrage {str(the_book)} ? (o/n) ")  #  Prévoir un LineEdit
	if registration_request == "o" or registration_request == "o".upper():  # Prévoir une saisie utilisateur en GUI
		register_book = biblib.SaveBook(the_book.id_and_ref_title(), my_biblio, donnes_du_livre)
		register_book.check_json_file()
		rec = register_book.save_ref()
		if rec:
			register_book.save_livre_data()
			print(f"Enregistrement de {str(the_book)} effectué.")
		else:
			print(f"{str(the_book)} est déjà dans la base de données.")
	else:
		print("Pas d'enregistrement effectué")


def check_type_doc():  # item à sélectionner
	"""Choix du type de document

    Returns:
        str: reférence type de document.
    """
	ctd = False
	while not ctd:
		type_d = input("S'agit t'il d'un (A)rticle ou d'un (L)ivre ? Votre choix: ")
		if type_d == "a" or type_d == "A":
			return "A-"
		elif type_d == "l" or type_d == "L":
			return "L-"
		else:
			ctd = False


def enter_book():  #  Prévoir un LineEdit pour l'affichage et les widgets de saisie
	""" Pour la saisie des informations relatives à un livre."""
	author = input("Nom de l'auteur: ").upper()
	author2 = input("Prénom de l'auteur: ").capitalize()
	title_book = input("Titre de son livre/article: ").title()
	year = check_int("Année de parution: ")
	type_doc = check_type_doc()
	if type_doc == "A-":
		periodic = input("Nom de la revue dans laquelle l'article a été publié: ").title()
		first_page = check_int("Numéro de la première page: ")
		end_page = check_int("Numéro de la dernière page: ")
		return {"document": type_doc, "nom": author,
				"prenom": author2, "ouvrage": title_book,
				"an_parution": year, "revue": periodic,
				"pp": first_page, "pps": end_page}
	else:
		editing = input("Edition: ").capitalize()
		nber_pages = check_int("Nombre de pages: ")
		isbn = input("Numéro ISBN: ")
		return {"document": type_doc, "nom": author,
				"prenom": author2, "ouvrage": title_book,
				"an_parution": year, "edition": editing,
				"nb_pages": nber_pages, "ISBN": isbn}


def check_int(question):
	"""Verifier si la valeur saisie est de type 'int'.

    Args:
        question (str): Question posée en vue de la saisie.

    Returns:
        int: Nombre répondu à la question.
    """
	t = True
	while t:
		number = input(question)
		try:
			check_number = int(number)
		except ValueError:  # Exception qui évite la sortie de boucle
			print("Veuillez saisir un nombre...")
			t = True
		else:  # actions réalisées si aucune exception
			return check_number
