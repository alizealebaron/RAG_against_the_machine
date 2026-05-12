# ************************************************************************** #
#       _  _     ____                     ,~~.                               #
#      | || |   |___  \             ,   (  ^ )>                              #
#      | || |_    __) |             )\~~'   (       _      _      _          #
#      |__   _|  / __/             (  .__)   )    >(.)__ <(^)__ =(o)__       #
#         |_|   |_____| .fr         \_.____,*      (___/  (___/  (___/       #
#                                                                            #
# ************************************************************************** #
# @name   : chunk.py                                                         #
# @author : alebaron <alebaron@student.42lehavre.fr>                         #
#                                                                            #
# @creation : 2026/05/12 15:21:04 by alebaron                                #
# @update   : 2026/05/12 17:13:52 by alebaron                                #
# ************************************************************************** #

# +-------------------------------------------------------------------------+
# |                               Importation                               |
# +-------------------------------------------------------------------------+


from typing import List


# +-------------------------------------------------------------------------+
# |                                  Main                                   |
# +-------------------------------------------------------------------------+

def make_chunk_recrusive(text: str, chunk_max_size: int, separators: List[str]) -> list[str]:

    if separators is None:
        separators = ["\n\n", "\n", ". "]

    if not separators:
        # Plus de séparateurs : découpage brutal
        return [text[i:i+chunk_max_size] for i in range(0, len(text), chunk_max_size)]

    sep = separators[0]
    parts = text.split(sep)

    chunks = []
    current_chunk = ""

    for part in parts:
        # Si ajouter cette partie dépasse la limite
        if len(current_chunk) + len(part) + len(sep) > chunk_max_size:
            if current_chunk:
                chunks.append(current_chunk.strip())

            # Si la partie seule est trop grande, récursion
            if len(part) > chunk_max_size:
                chunks.extend(make_chunk_recrusive(part, chunk_max_size, separators[1:]))
                current_chunk = ""
            else:
                current_chunk = part
        else:
            current_chunk += (sep if current_chunk else "") + part

    if current_chunk.strip():
        chunks.append(current_chunk.strip())

    return chunks
