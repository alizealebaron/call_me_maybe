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
# @creation : 2026/04/04 10:38:21 by alebaron                                #
# @update   : 2026/04/04 12:24:33 by alebaron                                #
# ************************************************************************** #

# +-------------------------------------------------------------------------+
# |                               Importation                               |
# +-------------------------------------------------------------------------+


import sys
import os
from src.parsing.parsing_args import check_args


# +-------------------------------------------------------------------------+
# |                                  Main                                   |
# +-------------------------------------------------------------------------+

def main():

    # === Get Main arguments ===

    argc = len(sys.argv)
    argv = sys.argv

    # === Parsing arguments ===

    file_path = check_args(argc, argv)


if __name__ == "__main__":
    # try:
    main()
    # except KeyboardInterrupt:
    #     os.system("clear")
    #     file = open("src/utils/interrupt.txt", "r", encoding='utf-8')
    #     content = file.read()
    #     print(content)
    # except Exception as e:
    #     print(f"Error: {e}")
