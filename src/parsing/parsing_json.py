# ************************************************************************** #
#       _  _     ____                     ,~~.                               #
#      | || |   |___  \             ,   (  ^ )>                              #
#      | || |_    __) |             )\~~'   (       _      _      _          #
#      |__   _|  / __/             (  .__)   )    >(.)__ <(^)__ =(o)__       #
#         |_|   |_____| .fr         \_.____,*      (___/  (___/  (___/       #
#                                                                            #
# ************************************************************************** #
# @name   : parsing_json.py                                                  #
# @author : alebaron <alebaron@student.42lehavre.fr>                         #
#                                                                            #
# @creation : 2026/04/04 16:00:28 by alebaron                                #
# @update   : 2026/04/04 16:33:45 by alebaron                                #
# ************************************************************************** #

# +-------------------------------------------------------------------------+
# |                               Importation                               |
# +-------------------------------------------------------------------------+


import json
from typing import Tuple
from src.utils.error import exit_error, ParsingError


# +-------------------------------------------------------------------------+
# |                                 Methods                                 |
# +-------------------------------------------------------------------------+

def check_json(file_path: dict[str, str]) -> Tuple[dict, dict]:

    try:
        with open(file_path["--functions_definition"], "r") as file:
            dict_func = json.load(file)

        with open(file_path["--input"], "r") as file:
            dict_input = json.load(file)

    except Exception as e:
        exit_error(ParsingError(), str(e))

    return (dict_func, dict_input)
