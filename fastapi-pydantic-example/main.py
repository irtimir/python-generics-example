import random
import string

from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError, HTTPException
from fastapi.utils import is_body_allowed_for_status_code
from starlette.exceptions import HTTPException
from starlette.responses import JSONResponse, Response
from starlette.requests import Request
from starlette.status import HTTP_422_UNPROCESSABLE_ENTITY

from schemas import ValidationError, ValidationErrorResp, Movie, MovieResponse, MoviesResponse, NokResp

app = FastAPI(
    responses={
        422: {
            'description': 'Validation Error',
            'model': ValidationErrorResp,
        },
    },
)


@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException) -> Response:
    headers = getattr(exc, 'headers', None)
    if not is_body_allowed_for_status_code(exc.status_code):
        return Response(status_code=exc.status_code, headers=headers)
    return JSONResponse(
        NokResp(msg=exc.detail).model_dump(), status_code=exc.status_code, headers=headers
    )


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    data = ValidationError(detail=jsonable_encoder(exc.errors()))
    return JSONResponse(
        content=jsonable_encoder(ValidationErrorResp(data=data).model_dump()),
        status_code=HTTP_422_UNPROCESSABLE_ENTITY,
    )


def random_string(n):
    return ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(n))


@app.get('/movies/')
async def get_movies() -> MoviesResponse:
    return MoviesResponse(data=[Movie(id=1, name=random_string(10))])


@app.get(
    '/movies/{item_id}',
    responses={
        404: {
            'description': 'Not found',
            'model': NokResp,
        },
    },
)
async def get_movie(item_id: int) -> MovieResponse:
    if item_id < 1 or item_id == 13:
        raise HTTPException(status_code=404, detail='Movie not found')
    return MovieResponse(data=Movie(id=item_id, name=random_string(10)))
