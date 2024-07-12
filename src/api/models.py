import re 
import uuid 
from fastapi import HTTPException 
from pydantic import BaseModel, EmailStr, field_validator, Field, ConfigDict
from typing import Optional


LETTER_MATCH_PATTERN = re.compile(r"^[a-zA-Zа-яА-Я\-]+$")

# User
class TunedModel(BaseModel): 
    class Config(ConfigDict): 
        """говорит pydantic конвертировать не только dict в json"""
        from_attributes = True
        """json-фицирует всё что входит в этот класс"""

class DeletedUserResponse(BaseModel): 
    delete_user_id: uuid.UUID
class ShowUser(TunedModel): 
    user_id: uuid.UUID
    name: str 
    surname: str
    email: EmailStr
    is_active: bool 

class UserCreate(BaseModel): 
    name: str
    surname: str
    email: EmailStr
    password: str

    @field_validator("name")
    def validate_name(cls, value): 
        if not LETTER_MATCH_PATTERN.match(value): 
            raise HTTPException(
                status_code=422, detail="Name should contain only letters"
            )
        return value 
    
    @field_validator("surname")
    def validate_surname(cls, value): 
        if not LETTER_MATCH_PATTERN.match(value):
            raise HTTPException ( 
                status_code=422, detail="Surname should contain only letters"
            )
        return value
    
class UpdatedUserResponse(BaseModel):
    updated_user_id: uuid.UUID
class UpdatedUserRequest(BaseModel): 
    name: Optional[str] = Field(None, min_length=1)
    surname: Optional[str] = Field(None, min_length=1)
    email: Optional[EmailStr] = Field(None, min_length=1) 

    @field_validator("name")
    def validate_name(cls, value): 
        if not LETTER_MATCH_PATTERN.match(value): 
            raise HTTPException(
                status_code=422, detail="Name should contain only letters"
            )
        return value 
    
    @field_validator("surname")
    def validate_surname(cls, value): 
        if not LETTER_MATCH_PATTERN.match(value):
            raise HTTPException ( 
                status_code=422, detail="Surname should contain only letters"
            )
        return value
    
# Login 
class Token(BaseModel): 
    access_token: str
    token_type: str
