# ************************************************************************** #
#       _  _     ____                     ,~~.                               #
#      | || |   |___  \             ,   (  ^ )>                              #
#      | || |_    __) |             )\~~'   (       _      _      _          #
#      |__   _|  / __/             (  .__)   )    >(.)__ <(^)__ =(o)__       #
#         |_|   |_____| .fr         \_.____,*      (___/  (___/  (___/       #
#                                                                            #
# ************************************************************************** #
# @name   : error.py                                                         #
# @author : alebaron <alebaron@student.42lehavre.fr>                         #
#                                                                            #
# @creation : 2026/02/27 14:26:28 by alebaron                                #
# @update   : 2026/04/04 10:56:27 by alebaron                                #
# ************************************************************************** #

# +--------------------------------------------------------------------------+
# |                                  Class                                   |
# +--------------------------------------------------------------------------+


class ParsingError(Exception):
    """
    Exception raised for errors in the configuration.
    """
    pass


class ArgumentError(Exception):
    """
    Exception raised for errors in arguments.
    """
    pass


# +--------------------------------------------------------------------------+
# |                                 Function                                 |
# +--------------------------------------------------------------------------+

def exit_error(error_type: Exception, message: str) -> None:
    """
    Print an error message and exit the program.

    Args:
        error_type (Exception): The type of error to be printed.
        message (str): The error message to be printed.
    """
    print(f"{error_type.__class__.__name__}: {message}")
    exit(2)


def print_error(error_type: Exception, message: str) -> None:
    """
    Print an error message without exiting the program.
    Args:
        error_type (Exception): The type of error to be printed.
        message (str): The error message to be printed.
    """
    print(f"{error_type.__class__.__name__}: {message}")
