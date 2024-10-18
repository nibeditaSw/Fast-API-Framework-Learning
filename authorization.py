from fastapi import Header, HTTPException

# Define available roles
VALID_ROLES = {"admin", "user"}

# Role-based authentication dependency
def role_required(allowed_roles: list[str]):
    def wrapper(role: str = Header(...)):
        if role not in VALID_ROLES:
            print(f"Invalid role '{role}' provided.")
            raise HTTPException(status_code=400, detail="Invalid role provided")
        
        if role not in allowed_roles:
            print(f"Access denied for role '{role}'. Allowed roles: {allowed_roles}.")
            raise HTTPException(status_code=403, detail="Access forbidden for your role")
        
        print(f"Access granted for role '{role}'.")
        return role
    return wrapper
