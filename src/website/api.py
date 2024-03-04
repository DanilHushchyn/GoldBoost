from django.core.files.storage.filesystem import FileSystemStorage
from ninja import Schema, Form
from ninja_extra import NinjaExtraAPI, api_controller, http_get,Router
from typing import List

api = Router()


# function based definition
@api.get("/add", tags=['Math'])
def add(request, a: int, b: int):
    return {"result": a + b}


#
# # class based definition
# @api_controller('/', tags=['Math'], permissions=[])
# class MathAPI:
#
#     @http_get('/subtract', )
#     def subtract(self, a: int, b: int):
#         """Subtracts a from b"""
#         return {"result": a - b}
#
#     @http_get('/divide', )
#     def divide(self, a: int, b: int):
#         """Divides a by b"""
#         return {"result": a / b}
#
#     @http_get('/multiple', )
#     def multiple(self, a: int, b: int):
#         """Multiples a with b"""
#         return {"result": a * b}
#
#
# api.register_controllers(
#     MathAPI
# )
#

class UserSchema(Schema):
    username: str
    is_authenticated: bool
    # Unauthenticated users don't have the following fields, so provide defaults.
    email: str = None
    first_name: str = None
    last_name: str = None


@api.get("/me", response=UserSchema)
def me(request):
    return request.user


@api.post("/me3", response=UserSchema)
def me(request, user: List[Form[UserSchema]]):
    return request.user


class Error(Schema):
    message: str


@api.get("/me2", response={200: UserSchema, 403: Error})
def me2(request):
    if not request.user.is_authenticated:
        return 403, {"message": "Please sign in first"}
    return request.user


from ninja import UploadedFile, File

STORAGE = FileSystemStorage()


@api.post("/upload")
def create_upload(request, cv: UploadedFile = File(...)):
    filename = STORAGE.save(cv.name, cv)
    # Handle things further


class MyInput(Schema):
    name: str


@api.post("/endpoint")
@api.get("/endpoint")
def my_endpoint(request):
    if request.method == "POST":
        data = MyInput(request.data)
        return {"message": f"Received POST request with name: {data.name}"}
    elif request.method == "GET":
        return {"message": "Received GET request"}


weapons = ["Ninjato", "Shuriken", "Katana", "Kama", "Kunai", "Naginata", "Yari"]


@api.get("/weapons/search")
def search_weapons(request, q: str, offset: int = 0):
    results = [w for w in weapons if q in w.lower()]
    return results[offset: offset + 10]


from pydantic import Field

from ninja import Query, Schema


class Filters(Schema):
    limit: int = 100
    offset: int = None
    query: str = None
    category__in: List[str] = Field(None, alias="categories")


@api.get("/filter")
def events(request, filters: Query[Filters]):
    return {"filters": filters.dict()}


@api.post("/upload-many")
def upload_many(request, files: List[UploadedFile] = File(...), files2: List[UploadedFile] = File(...)):
    return [f.name for f in files]


class UserDetails(Schema):
    first_name: str
    last_name: str


@api.post('/users')
def create_user(request, details: Form[UserDetails], file: File[UploadedFile]):
    return [details.dict(), file.name]
