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
# @update   : 2026/04/06 10:46:05 by alebaron                                #
# ************************************************************************** #

# +-------------------------------------------------------------------------+
# |                               Importation                               |
# +-------------------------------------------------------------------------+


import json
from typing import Tuple
from src.utils.error import exit_error, ParsingError
from src.models.functionModel import FunctionModel
from src.models.promptModel import PromptModel


# +-------------------------------------------------------------------------+
# |                                 Methods                                 |
# +-------------------------------------------------------------------------+

def check_json(file_path: dict[str, str]) -> Tuple[list[FunctionModel],
                                                   list[PromptModel]]:

    try:
        with open(file_path["--functions_definition"], "r") as file:
            data = json.load(file)
            list_func = [FunctionModel(**arg) for arg in data]

        with open(file_path["--input"], "r") as file:
            data = json.load(file)
            list_prompt = [PromptModel(**arg) for arg in data]

    except Exception as e:
        exit_error(ParsingError(), str(e))

    return (list_func, list_prompt)
