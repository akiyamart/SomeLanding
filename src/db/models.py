import uuid 
from enum import Enum
from sqlalchemy import String, Column, Boolean
from sqlalchemy.dialects.postgresql import UUID, ARRAY
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class PortalRole(str, Enum):
    ROLE_PORTAL_USER = "ROLE_PORTAL_USER"
    ROLE_PORTAL_ADMIN = "ROLE_PORTAL_ADMIN"
    ROLE_PORTAL_SUPERADMIN = "ROLE_PORTAL_SUPERADMIN"
class User(Base): 
    __tablename__ = "users"

    user_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    surname = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    is_active = Column(Boolean, default=True)
    hashed_password = Column(String, nullable=False)
    roles =  Column(ARRAY(String), nullable=False)

    @property
    def is_admin(self) -> bool: 
        return PortalRole.ROLE_PORTAL_ADMIN in self.roles
    
    @property
    def is_superadmin(self) -> bool: 
        return PortalRole.ROLE_PORTAL_SUPERADMIN in self.roles 
    
    def add_admin_privileges(self): 
        if not self.is_admin: 
            return {self.roles, PortalRole.ROLE_PORTAL_ADMIN}