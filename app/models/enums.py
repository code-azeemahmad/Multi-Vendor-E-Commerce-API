from enum import Enum


class UserRole(str, Enum):
    ADMIN = "admin"
    VENDOR = "vendor"
    CUSTOMER = "customer"
    
    
class TokenType(str, Enum):
    ACCESS = "access"
    REFRESH = "refresh"