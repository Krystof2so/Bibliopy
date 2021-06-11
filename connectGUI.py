import bibliolib as biblib 

# PushButton "Créer bibliographie"
def run_bibliopy():
    """Créer un bibliographie.

    Returns:
        str: nom de la bibliographie.
    """
    my_biblio = biblib.Bibliography(input("Nom de la bibliographie que vous voulez créer: ")) # A modifier pour le GUI
    return my_biblio.create_dir_biblio()

# PushButton "Saisir livre"
def btn_input_book(my_biblio):
    """Fonction lancer l'enregistrer des informations fournies pour un livre.

    Args:
        my_biblio (dict): Ensemble des informartions relatives à un livre.
    """
    The_book = biblib.BookRef(enter_book())
    registration_request = input(f"Souhaitez-vous enregistrer l'ouvrage {str(The_book)} ? (o/n) ") # Prévoir un LineEdit
    if registration_request == "o" or registration_request == "o".upper(): # Prévoir une saisie utilisateur en GUI
        register_book = biblib.SaveBook(The_book.id_and_ref_title(), my_biblio)
        register_book.check_json_file()
        rec = register_book.save_ref()
        if rec:
            register_book.save_livre_data()
            print(f"Enregistrement de {str(The_book)} effectué.")
        else:
            print(f"{str(The_book)} est déjà dans la base de données.")
    else:
        print("Pas d'enregistrement effectué")
    
def enter_book(): # Prévoir un LineEdit pour l'affichage et les widgets de saisie
    """ Pour la saisie des informations relatives à un livre."""  
    author = input("Nom de l'auteur: ").upper()
    author2 = input("Prénom de l'auteur: ").capitalize()
    title_book = input("Titre de son livre: ").title()
    return {"nom": author, "prenom": author2, "ouvrage": title_book}
