from typing import Literal

# Define role constants
ADMIN_ROLE = "admin"
USER_ROLE = "user"

# Define valid roles
VALID_ROLES =  {ADMIN_ROLE, USER_ROLE}


# Define accepted fields for sorting
SORTABLE_FIELDS = Literal[
    "pokemon_id", "name", "type_1", "type_2", "total",
    "hp", "attack", "defense", "sp_atk", "sp_def", "speed", "generation", "legendary"
]

# Validate keyword datatype based on the search column
int_columns = ["total", "hp", "attack", "defense", "sp_atk", "sp_def", "speed", "generation"]
bool_columns = ["legendary"]
string_columns = ["name", "type_1", "type_2"]