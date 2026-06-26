# ************************************************************************** #
#       _  _     ____                     ,~~.                               #
#      | || |   |___  \             ,   (  ^ )>                              #
#      | || |_    __) |             )\~~'   (       _      _      _          #
#      |__   _|  / __/             (  .__)   )    >(.)__ <(^)__ =(o)__       #
#         |_|   |_____| .fr         \_.____,*      (___/  (___/  (___/       #
#                                                                            #
# ************************************************************************** #
# @name   : search.py                                                        #
# @author : alebaron <alebaron@student.42lehavre.fr>                         #
#                                                                            #
# @creation : 2026/05/15 11:16:02 by alebaron                                #
# @update   : 2026/06/26 10:38:32 by alebaron                                #
# ************************************************************************** #

# +-------------------------------------------------------------------------+
# |                              Importation                                |
# +-------------------------------------------------------------------------+


import os
from ...utils.error import IndexError


# +-------------------------------------------------------------------------+
# |                                Methods                                  |
# +-------------------------------------------------------------------------+

def cli_search(question: str, k: int):

    # On chunk les documents si ça n'a pas déjà été fait

    index_path = "../data/processed/chunks/chunk.json"

    if (os.path.exists(index_path) is False):
        raise IndexError("Error: You must do indexing before searching.")

    # Et ensuite on cherche les documents pertinents

    