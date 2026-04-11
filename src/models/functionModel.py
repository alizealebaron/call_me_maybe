# ************************************************************************** #
#       _  _     ____                     ,~~.                               #
#      | || |   |___  \             ,   (  ^ )>                              #
#      | || |_    __) |             )\~~'   (       _      _      _          #
#      |__   _|  / __/             (  .__)   )    >(.)__ <(^)__ =(o)__       #
#         |_|   |_____| .fr         \_.____,*      (___/  (___/  (___/       #
#                                                                            #
# ************************************************************************** #
# @name   : functionModel.py                                                 #
# @author : alebaron <alebaron@student.42lehavre.fr>                         #
#                                                                            #
# @creation : 2026/04/06 10:32:38 by alebaron                                #
# @update   : 2026/04/11 13:29:17 by alebaron                                #
# ************************************************************************** #

# +-------------------------------------------------------------------------+
# |                               Importation                               |
# +-------------------------------------------------------------------------+


from pydantic import BaseModel


# +-------------------------------------------------------------------------+
# |                                  Class                                  |
# +-------------------------------------------------------------------------+

class FunctionModel(BaseModel):
    """
    A class representing a function model, containing the function's name,
    description, parameters, and return type.

    Attributes:
        name (str): The name of the function.
        description (str): A brief description of the function's purpose.
        parameters (dict[str, dict[str, str]]): A dictionary where each key
            is a parameter name and the value is another dictionary containing
            the parameter's type and description.
        returns (dict[str, str]): A dictionary containing the return type and
            description of the function's return value.
    """

    # +---------------------------------------------------------------------+
    # |                              Attributs                              |
    # +---------------------------------------------------------------------+

    name: str
    description: str
    parameters: dict[str, dict[str, str]]
    returns: dict[str, str]

    # +---------------------------------------------------------------------+
    # |                               Methods                               |
    # +---------------------------------------------------------------------+

    def to_string(this) -> str:
        """
        Return a string representation of the FunctionModel instance.

        Returns:
            str: A string representing the function model.
        """

        return f"Function: {this.name}\n" + \
            f"Description: {this.description}" + \
            f"\nParameters: {this.parameters}" + \
            f"\nReturns: {this.returns}"
