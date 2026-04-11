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
# @update   : 2026/04/11 11:17:20 by alebaron                                #
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
            params = this.gen_func_param(prompt, func_name)
            prompt_output['parameters'] = params

            output.append(prompt_output)

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
        full_prompt += f"\nResolve the following prompt: {prompt.prompt}\n" + \
            "function name: "
        full_prompt_tokens = this.__llm.encode(full_prompt)

        # Récupération des données utiles
        full_prompt_tokens = [t for sublist in full_prompt_tokens
                              for t in sublist]

        # === Boucle de génération ===

        current_output = ""
        current_tokens: List[int] = []

        while (True):

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

            if not valid_tokens:
                break

            # Constrained Decoding: appliquer le masque
            logits_masked = np.full_like(logits, -np.inf, dtype=float)
            for token_id in valid_tokens:
                logits_masked[token_id] = logits[token_id]

            # Sélectionner le meilleur token valide
            best_token_id = int(np.argmax(logits_masked))

            current_tokens.append(best_token_id)
            # Convertir en texte et ajouter
            token_string = this.__dict_vocab.get(best_token_id, "")
            current_output += token_string

            # Sécurité: si token vide, arrêter pour éviter boucle infinie
            if not token_string:
                break

            # Vérifier si on a trouvé un nom complet
            if current_output in this.__list_name_function:
                break

        return current_output

    def gen_func_param(this, prompt: PromptModel,
                       func_name: str) -> Dict[Any, Any]:

        # Récupération des paramètres demandés
        func_params = this.get_func_para_by_name(func_name)

        # Génération des paramètres
        output: Dict[str, Any] = {}
        previous_gen = ""
        for param in func_params:

            previous_gen = ""
            for arg in output.keys():
                previous_gen = previous_gen + arg + "="
                previous_gen += str(output[arg]) + "\n"

            previous_gen = previous_gen + param + "="
            if func_params[param]["type"] == "string":
                output[param] = this.gen_str_parameter(
                    prompt.prompt, func_name, previous_gen)
            elif func_params[param]["type"] == "number":
                output[param] = this.gen_int_parameter(
                    prompt.prompt, func_name, previous_gen)
        return output

    def gen_int_parameter(this, prompt: str, func_name: str,
                          previous_gen: str) -> float | None:

        # === Préparation des données ===

        func = this.get_func_by_name(func_name)

        # Construire le prompt
        full_prompt = f"To solve the prompt {prompt}, you " + \
            f"will use the following function: {func}." + \
            " Provide each parameter. Keep it concise and don't add" + \
            " custom fields."

        full_prompt = f"<|im_start|>user\n{full_prompt}<|im_end|>\n" + \
            f"<|im_start|>assistant\n<think>\n\n</think>\n\n{previous_gen}"

        # Caractères valides pour un float
        valid_chars = set('-0123456789.\n')

        # Créer dictionnaire: caractère -> tokens qui le représentent
        char_to_tokens: Dict[str, List[int]] = {}
        for char in valid_chars:
            char_tokens = this.__llm.encode(char)
            char_tokens = [t for sublist in char_tokens for t in sublist]
            char_to_tokens[char] = char_tokens

        # Encodage du prompt
        full_prompt_tokens = this.__llm.encode(full_prompt)
        full_prompt_tokens = [t for sublist in full_prompt_tokens
                              for t in sublist]

        # === Boucle de génération ===

        current_output = ""
        current_tokens: List[int] = []
        max_tokens = 20  # Sécurité en cas de mauvaise génération
        consecutive_rejects = 0
        max_consecutive_rejects = 5

        while len(current_tokens) < max_tokens:

            # Combiner les tokens: prompt + sortie actuelle
            all_tokens = full_prompt_tokens + current_tokens

            # Récupération des logits
            logits = this.__llm.get_logits_from_input_ids(all_tokens)

            # Identifier les tokens valides
            valid_tokens: set = set()
            for char in valid_chars:
                for token_id in char_to_tokens[char]:
                    valid_tokens.add(token_id)

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

            temp_output = current_output + token_string

            # === Validation des règles de nombre ===
            is_valid = True

            # Pas deux '.'
            if temp_output.count('.') >= 2:
                is_valid = False

            # Pas deux '-'
            elif temp_output.count('-') >= 2:
                is_valid = False

            # '-' seulement au début
            elif temp_output.count('-') == 1 and temp_output[0] != '-':
                is_valid = False

            if not is_valid:
                current_tokens.pop()
                consecutive_rejects += 1
                if consecutive_rejects >= max_consecutive_rejects:
                    break
                continue

            current_output = temp_output

            # Vérifier si on a un nombre valide complet
            try:
                float(current_output)
                if token_string not in '0123456789.-':
                    break
            except ValueError:
                pass

            # Si '\n' rencontré, extraire et retourner
            if '\n' in current_output:
                current_output = current_output.split('\n')[0]
                try:
                    return float(current_output)
                except ValueError:
                    return None

        # Garder seulement les caractères valides pour un nombre
        cleaned_output = ""
        for char in current_output:
            if char in '-0123456789.':
                cleaned_output += char

        # Retourner ce qu'on a généré
        try:
            return float(cleaned_output)
        except ValueError:
            return None

    def gen_str_parameter(this, prompt: str, func_name: str,
                          previous_gen: str) -> str:

        # === Préparation des données ===

        func = this.get_func_by_name(func_name)

        # Construire le prompt
        full_prompt = f"To solve the prompt {prompt}, you " + \
            f"will use the following function: {func.to_string()}.\n" + \
            "Provide each parameter. Keep it concise." + \
            " End each parameter with an new ligne."

        full_prompt = f"<|im_start|>user\n{full_prompt}<|im_end|>\n" + \
            f"<|im_start|>assistant\n<think>\n\n</think>\n\n{previous_gen}"

        # Encodage du prompt
        full_prompt_tokens = this.__llm.encode(full_prompt)
        full_prompt_tokens = [t for sublist in full_prompt_tokens
                              for t in sublist]

        # === Boucle de génération ===

        current_output = ""
        current_tokens: List[int] = []
        max_tokens = 50  # Les strings peuvent être plus longues

        while len(current_tokens) < max_tokens:

            # Combiner les tokens: prompt + sortie actuelle
            all_tokens = full_prompt_tokens + current_tokens

            # Récupération des logits
            logits = this.__llm.get_logits_from_input_ids(all_tokens)

            # Sélectionner le meilleur token
            best_token_id = int(np.argmax(logits))

            # Ajouter le token
            current_tokens.append(best_token_id)

            # Convertir en texte et ajouter
            token_string = this.__dict_vocab.get(best_token_id, "")

            # Sécurité: si token vide, arrêter
            if not token_string or token_string.strip() == "":
                break

            current_output += token_string

            # Arrêter si caractère spécial \u010a rencontré
            if '\u010a' in current_output:
                current_output = current_output.split('\u010a')[0]
                break

            # Arrêter si '\n' rencontré
            if '\n' in current_output:
                current_output = current_output.split('\n')[0]
                break

            # Arrêter si plusieurs espaces consécutifs
            if '  ' in current_output:
                current_output = current_output.split('  ')[0]
                break

        # Nettoyer: supprimer les espaces extra et caractères indésirables
        final_value = current_output.strip()
        # Supprimer les caractères spéciaux
        final_value = final_value.replace('\u0120', ' ')
        final_value = final_value.replace('  ', '')

        return final_value

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

    def get_func_para_by_name(this, name: str) -> str | None:

        for func in this.__list_function:
            if func.name == name:
                return func.parameters
        return None

    def get_func_by_name(this, name: str) -> FunctionModel | None:

        for func in this.__list_function:
            if func.name == name:
                return func
        return None
