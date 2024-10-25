from fastapi import Header, HTTPException
from typing import List
from constants import VALID_ROLES


# Role-based authentication dependency
def role_required(allowed_roles: List[str]):
    """
    Dependency function to enforce role-based access control.

    Args:
        allowed_roles (List[str]): List of roles permitted to access the endpoint.

    Returns:
        Callable: A dependency function that checks the role in the request header.
    """
    def wrapper(role: str = Header(...)):
        """
        Inner function to validate the role from the request header.

        Args:
            role (str): The role provided in the request header.

        Raises:
            HTTPException: Raised if the role is invalid or not allowed access.

        Returns:
            str: Returns the role if it is valid and authorized.
        """
        if role not in VALID_ROLES:
            print(f"Invalid role '{role}' provided.")
            raise HTTPException(status_code=400, detail="Invalid role provided")
        
        if role not in allowed_roles:
            print(f"Access denied for role '{role}'. Allowed roles: {allowed_roles}.")
            raise HTTPException(status_code=403, detail="Access forbidden for your role")
        
        print(f"Access granted for role '{role}'.")
        return role
    return wrapper
