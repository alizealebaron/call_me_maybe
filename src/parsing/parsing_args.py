# ************************************************************************** #
#       _  _     ____                     ,~~.                               #
#      | || |   |___  \             ,   (  ^ )>                              #
#      | || |_    __) |             )\~~'   (       _      _      _          #
#      |__   _|  / __/             (  .__)   )    >(.)__ <(^)__ =(o)__       #
#         |_|   |_____| .fr         \_.____,*      (___/  (___/  (___/       #
#                                                                            #
# ************************************************************************** #
# @name   : parsing_args.py                                                  #
# @author : alebaron <alebaron@student.42lehavre.fr>                         #
#                                                                            #
# @creation : 2026/04/04 11:04:41 by alebaron                                #
# @update   : 2026/04/04 12:22:19 by alebaron                                #
# ************************************************************************** #

# +-------------------------------------------------------------------------+
# |                               Importation                               |
# +-------------------------------------------------------------------------+


from src.utils.error import ArgumentError, exit_error


# +-------------------------------------------------------------------------+
# |                                 Methods                                 |
# +-------------------------------------------------------------------------+

def check_args(argc: int, argv: list[str]) -> dict[str, str]:

    # === Déclaration des options valides ====

    valid_options = {"--functions_definition": "data/input/"
                     "functions_definition.json",
                     "--input": "data/input/function_calling_tests.json",
                     "--output": "data/output/function_calls.json"
                     }

    # === Vérification du nombre d'arguments ====

    if (argc != 1 and argc % 2 == 0):
        exit_error(ArgumentError(), "Wrong Argument. Please provide a path "
                   "and an option together.")

    # === Vérification des arguments ===

    i = 0

    for args in argv:

        if args not in valid_options:
            i += 1
            continue

        if args == "--functions_definition" or args == "--input":
            check_file(argv[i + 1])

        valid_options[args] = argv[i + 1]

        i += 1

    # === Vérification des doublons ===

    if (valid_options["--functions_definition"] == valid_options["--output"] or
       valid_options["--input"] == valid_options["--output"]):

        exit_parsing_error("The output cannot be the same file as the input "
                           "or the functions", valid_options["--output"])

    # === Renvoie des données vérifiées ===

    return valid_options


def check_file(filename: str) -> None:
    """
    Checks if the file exists and is accessible.

    Args:
        filename (str): The path to the file to check.

    Raises:
        ParsingError: If the file is missing, inaccessible,
        or is a directory.
    """
    try:
        with open(filename, "r") as file:
            lines = file.read().splitlines()
        if (len(lines) == 0):
            raise ArgumentError("Empty files are not allowed.")

    except FileNotFoundError:
        exit_parsing_error("File not found. Check the path and "
                           "try again.", filename)

    except PermissionError:
        exit_parsing_error("No permission to access the file."
                           " Check your access rights.", filename)

    except IsADirectoryError:
        exit_parsing_error("Expected a file, but got directory "
                           ". Please provide a file.", filename)

    except ArgumentError as e:
        exit_parsing_error(str(e), filename)

    except Exception as e:
        exit_parsing_error(f"Unexcepted exception ({e}).", filename)


# +-------------------------------------------------------------------------+
# |                              Error Methods                              |
# +-------------------------------------------------------------------------+

def exit_parsing_error(message: str, file: str) -> None:
    """
    Exit the program with a parsing error message.

    Args:
        message (str): The error message to display.
        file (str): The file where the error occurred.
    """

    exit_error(ArgumentError(), message + f" (File: {file})")
