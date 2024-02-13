from pydantic import BaseModel

class SuapLoginDTO(BaseModel):
    username: str
    password: str