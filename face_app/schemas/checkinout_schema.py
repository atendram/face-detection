from numpy import double
from pydantic import BaseModel
from typing import List,Optional

class checkInOutSchecma(BaseModel):
    checkType:str
    checkBy:int
