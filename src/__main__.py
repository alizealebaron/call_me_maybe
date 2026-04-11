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
# @update   : 2026/04/11 11:11:56 by alebaron                                #
# ************************************************************************** #

# +-------------------------------------------------------------------------+
# |                               Importation                               |
# +-------------------------------------------------------------------------+


import sys
import os
import json
import time
from llm_sdk import Small_LLM_Model
from src.parsing.parsing_args import check_args
from src.parsing.parsing_json import check_json
from src.parsing.parsing_name import get_dir_and_name
from src.algorithm.calling_llm import Call_Me_Maybe


# +-------------------------------------------------------------------------+
# |                                  Main                                   |
# +-------------------------------------------------------------------------+

def main():

    # === Starting time ===

    start_time = time.time()

    # === Get Main arguments ===

    argc = len(sys.argv)
    argv = sys.argv

    # === Parsing arguments ===

    file_path = check_args(argc, argv)
    list_function, list_prompt = check_json(file_path)

    # === Calling (Maybe) the LLM ===

    llm = Small_LLM_Model()
    cmm = Call_Me_Maybe(list_prompt, list_function, llm)

    results = cmm.process()

    # === Save results to output file ===

    out_dir, out_name = get_dir_and_name(file_path["--output"])

    os.makedirs(out_dir, exist_ok=True)

    output_file = os.path.join(out_dir, out_name)
    with open(output_file, "w") as f:
        json.dump(results, f, indent=2)

    # === Calculate time ===

    end_time = time.time()
    prog_time = end_time - start_time

    minutes = int(prog_time // 60)
    seconds = int(prog_time % 60)
    print(f"Programme executed in {minutes} min {seconds} sec")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        os.system("clear")
        file = open("src/utils/interrupt.txt", "r", encoding='utf-8')
        content = file.read()
        print(content)
    except Exception as e:
        print(f"Error: {e}")
