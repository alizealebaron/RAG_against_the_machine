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
# @update   : 2026/05/12 15:34:22 by alebaron                                #
# ************************************************************************** #

# +-------------------------------------------------------------------------+
# |                               Importation                               |
# +-------------------------------------------------------------------------+


try:
    import sys
    import fire
    from src.cli_functions.index.index import cli_index
except Exception:
    print("ImportationError: Some package are not present. Please do "
          "`uv sync` to install a python env.")
    sys.exit(2)


# +-------------------------------------------------------------------------+
# |                              CLI functions                              |
# +-------------------------------------------------------------------------+


def index(max_chunk_size: int):
    cli_index(max_chunk_size)


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
