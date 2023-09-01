from typing import Generic, List, Literal, Optional, TypeVar

from pydantic import BaseModel

T = TypeVar('T')


class BaseResp(BaseModel, Generic[T]):
    success: bool
    data: Optional[T]
    msg: Optional[str] = None


class OkResp(BaseResp):
    success: Literal[True] = True


class BaseNokResp(BaseResp):
    success: Literal[False] = False


class NokResp(BaseNokResp):
    data: Literal[None] = None


class ValidationError(BaseModel):
    detail: List[dict]


class ValidationErrorResp(BaseNokResp[ValidationError]):
    ...


class Movie(BaseModel):
    id: int
    name: str


class MoviesResponse(OkResp[List[Movie]]):
    ...


class MovieResponse(OkResp[Movie]):
    ...
