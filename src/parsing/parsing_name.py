# ************************************************************************** #
#       _  _     ____                     ,~~.                               #
#      | || |   |___  \             ,   (  ^ )>                              #
#      | || |_    __) |             )\~~'   (       _      _      _          #
#      |__   _|  / __/             (  .__)   )    >(.)__ <(^)__ =(o)__       #
#         |_|   |_____| .fr         \_.____,*      (___/  (___/  (___/       #
#                                                                            #
# ************************************************************************** #
# @name   : parsing_name.py                                                  #
# @author : alebaron <alebaron@student.42lehavre.fr>                         #
#                                                                            #
# @creation : 2026/04/09 10:54:35 by alebaron                                #
# @update   : 2026/04/11 13:32:45 by alebaron                                #
# ************************************************************************** #

# +-------------------------------------------------------------------------+
# |                               Importation                               |
# +-------------------------------------------------------------------------+


from typing import Tuple


# +-------------------------------------------------------------------------+
# |                                 Methods                                 |
# +-------------------------------------------------------------------------+

def get_dir_and_name(full_path: str) -> Tuple[str, str]:
    """
    Get the directory and name from a full path.

    Args:
        full_path (str): The full path to be processed.

    Returns:
        Tuple[str, str]: A tuple containing the directory and name extracted
            from the full path.
    """

    path_split = full_path.split("/")

    name = path_split[(len(path_split) - 1)]
    path_split.pop((len(path_split) - 1))
    dir = "/".join(path_split)

    return (dir, name)
