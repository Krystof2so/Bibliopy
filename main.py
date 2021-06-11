"""MAIN."""

from const import DIR_DATAS
from connectGUI import btn_input_book, run_bibliopy

if __name__ == "__main__":
    
    DIR_DATAS.mkdir(exist_ok=True)
    
    my_biblio = run_bibliopy()
    btn_input_book(my_biblio)
