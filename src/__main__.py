# ************************************************************************** #
#       _  _     ____                     ,~~.                               #
#      | || |   |___  \             ,   (  ^ )>                              #
#      | || |_    __) |             )\~~'   (       _      _      _          #
#      |__   _|  / __/             (  .__)   )    >(.)__ <(^)__ =(o)__       #
#         |_|   |_____| .fr         \_.____,*      (___/  (___/  (___/       #
#                                                                            #
# ************************************************************************** #
# @name   : __main__.py                                                      #
# @author : alebaron <alebaron@student.42lehavre.fr>                         #
#                                                                            #
# @creation : 2026/05/07 11:47:53 by alebaron                                #
# @update   : 2026/05/07 15:25:45 by alebaron                                #
# ************************************************************************** #

# +-------------------------------------------------------------------------+
# |                               Importation                               |
# +-------------------------------------------------------------------------+


import fire


# +-------------------------------------------------------------------------+
# |                              CLI functions                              |
# +-------------------------------------------------------------------------+


def index(max_chunk_size: int):
    print("Vous avez sélectionné l'option \"index\" !")


def search():
    print("Vous avez sélectionné l'option \"search\" !")


def search_dataset():
    print("Vous avez sélectionné l'option \"search_dataset\" !")


def answer():
    print("Vous avez sélectionné l'option \"answer\" !")


def answer_dataset():
    print("Vous avez sélectionné l'option \"answer_dataset\" !")


def evaluate():
    print("Vous avez sélectionné l'option \"evaluate\" !")


# +-------------------------------------------------------------------------+
# |                                  Main                                   |
# +-------------------------------------------------------------------------+

if __name__ == '__main__':
    fire.Fire()
