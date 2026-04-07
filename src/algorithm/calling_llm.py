# ************************************************************************** #
#       _  _     ____                     ,~~.                               #
#      | || |   |___  \             ,   (  ^ )>                              #
#      | || |_    __) |             )\~~'   (       _      _      _          #
#      |__   _|  / __/             (  .__)   )    >(.)__ <(^)__ =(o)__       #
#         |_|   |_____| .fr         \_.____,*      (___/  (___/  (___/       #
#                                                                            #
# ************************************************************************** #
# @name   : calling_llm.py                                                   #
# @author : alebaron <alebaron@student.42lehavre.fr>                         #
#                                                                            #
# @creation : 2026/04/06 10:51:17 by alebaron                                #
# @update   : 2026/04/07 11:39:16 by alebaron                                #
# ************************************************************************** #

# +-------------------------------------------------------------------------+
# |                               Importation                               |
# +-------------------------------------------------------------------------+


import json
import numpy as np
from typing import Any, Dict, List
from llm_sdk import Small_LLM_Model
from src.models.functionModel import FunctionModel
from src.models.promptModel import PromptModel
from src.utils.error import exit_error


# +-------------------------------------------------------------------------+
# |                            Méthode principale                           |
# +-------------------------------------------------------------------------+

class Call_Me_Maybe():

    # +---------------------------------------------------------------------+
    # |                             Constructeur                            |
    # +---------------------------------------------------------------------+

    def __init__(this, list_prompt: list[PromptModel],
                 list_function: list[FunctionModel],
                 llm: Small_LLM_Model):

        this.__list_prompt = list_prompt
        this.__list_function = list_function
        this.__list_name_function = [func.name for func in
                                     this.__list_function]
        this.__llm = llm

        vocab_path = this.__llm.get_path_to_vocab_file()
        this.__dict_vocab = this.get_id_to_token_vocab(vocab_path)

    # +---------------------------------------------------------------------+
    # |                         Méthode principale                          |
    # +---------------------------------------------------------------------+

    def process(this) -> List[Any]:

        # === Boucle sur tous les prompts ===

        output = []

        for prompt in this.__list_prompt:

            prompt_output: Dict[Any, Any] = {}

            # Récupération du prompt
            prompt_output['prompt'] = prompt.prompt

            # Récupération du nom
            func_name = this.gen_function_name(prompt)
            prompt_output['name'] = func_name

            # Récupération des paramètres
            # params = self.generate_parameters(prompt, fn_name)
            # prompt_output['parameters'] = params

            output.append(prompt_output)

            print(prompt_output)

        return output

    # +---------------------------------------------------------------------+
    # |                         Méthodes secondaires                        |
    # +---------------------------------------------------------------------+

    def gen_function_name(this, prompt: PromptModel) -> str:

        # === Préparation des données ===

        available_function = this.get_available_func()

        # Récupération des noms des fonctions encodés en tokens
        dict_token_sequences: Dict[str, List[int]] = {}
        for func in this.__list_function:

            token_sequence = this.__llm.encode(func.name)
            token_sequence = [t for sublist in token_sequence for t
                              in sublist]

            dict_token_sequences[func.name] = token_sequence

        # Encodage du prompt
        full_prompt = available_function
        full_prompt += f"\nResolve the following prompt: {prompt.prompt}\n"
        full_prompt_tokens = this.__llm.encode(full_prompt)

        # Récupération des données utiles
        full_prompt_tokens = [t for sublist in full_prompt_tokens
                              for t in sublist]

        # === Boucle de génération ===

        current_output = ""
        current_tokens: List[int] = []
        while True:

            # Combiner les tokens: prompt + sortie actuelle
            all_tokens = full_prompt_tokens + current_tokens

            # Récupération des logits
            logits = this.__llm.get_logits_from_input_ids(all_tokens)

            # Identifier les tokens valides
            valid_tokens: set = set()
            for name in this.__list_name_function:

                if name.startswith(current_output):
                    name_encoding = dict_token_sequences[name]
                    next_position = len(current_tokens)
                    if next_position < len(name_encoding):
                        valid_tokens.add(name_encoding[next_position])

            # Si aucun token valide, arrêter
            if not valid_tokens:
                break

            # Constrained Decoding: appliquer le masque
            logits_masked = np.full_like(logits, -np.inf, dtype=float)
            for token_id in valid_tokens:
                logits_masked[token_id] = logits[token_id]

            # Sélectionner le meilleur token valide
            best_token_id = int(np.argmax(logits_masked))

            # Ajouter le token
            current_tokens.append(best_token_id)
            # Convertir en texte et ajouter
            token_string = this.__dict_vocab.get(best_token_id, "")
            current_output += token_string

            # Vérifier si on a trouvé un nom complet
            if current_output in this.__list_name_function:
                break

        return current_output

    # +---------------------------------------------------------------------+
    # |                         Méthodes utilitaires                        |
    # +---------------------------------------------------------------------+

    def get_available_func(this) -> str:

        available_func = "List of all available functions :\n"

        for func in this.__list_function:

            available_func += f'- {func.name}\n'
            available_func += f"\t- Description: {func.description}\n"

            available_func += "\t- Parameters: "

            list_param = []
            for param, param_info in func.parameters.items():
                list_param.append(f"{param} ({param_info['type']})")

            available_func += ", ".join(list_param) + "\n"

        return available_func

    def get_id_to_token_vocab(self, path: str) -> dict[int, str]:

        try:
            with open(path, "r") as file:
                vocab = json.load(file)

            rev_vocab = {}
            for key, value in vocab.items():
                rev_vocab[value] = key

            return rev_vocab

        except Exception as e:
            exit_error(Exception(), e)
