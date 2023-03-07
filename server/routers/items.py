from fastapi import APIRouter, Response, status

from models.item import Item
from repository.file import FileRepository, NotFound

router = APIRouter()


@router.post("/items/", tags=["items"])
def create_item(item: Item):
    repo = FileRepository()
    data = repo.create(item.dict())
    item = Item(**data)
    return item


@router.get("/items/", tags=["items"])
def read_items():
    repo = FileRepository()
    data = repo.read()
    return [Item(**d) for d in data]


@router.get("/items/{_id}", tags=["items"])
def read_item(_id: str):
    repo = FileRepository()
    data = repo.get(_id)
    return Item(**data)


@router.put("/items/{_id}")
def update_item(item: Item, _id: str):
    repo = FileRepository()

    try:
        repo.update(item.dict())
    except NotFound:
        return Response(status_code=status.HTTP_404_NOT_FOUND)

    return item


@router.delete("/items/{_id}", tags=["items"])
def delete_item(_id: str):
    repo = FileRepository()
    try:
        repo.get(_id)
    except NotFound:
        return Response(status=status.HTTP_404_NOT_FOUND)
    else:
        repo.delete(_id)

    return Response(status_code=status.HTTP_204_NO_CONTENT)
