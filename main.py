"""MAIN."""

import manageDB as mngDB
from const import DIR_DATAS
from connectGUI import btn_input_book, run_bibliopy


if __name__ == "__main__":
    
    DIR_DATAS.mkdir(exist_ok=True)
    mngDB.create_db()
    
    r = True
    while r:
        my_biblio = run_bibliopy()
        btn_input_book(my_biblio)
        choice = input("Quitter (o = Oui / Autre touche = Non): ")
        if choice.lower() == 'o':
            r = False
        else:
            r = True
