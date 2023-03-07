from fastapi import APIRouter, Response, status
from decimal import Decimal

from models.item import Item
from repository.file import FileRepository, NotFound

router = APIRouter()


@router.post("/items/", tags=["items"])
def create_item(item: Item):
    repo = FileRepository()

    data = repo.read()

    item.id = len(data) + 1
    data.append(item.dict())

    repo.save(data)

    return item


@router.get("/items/", tags=["items"])
def read_items():
    repo = FileRepository()
    data = repo.read()
    print(data)
    return [Item(**d) for d in data]


@router.get("/items/{_id}", tags=["items"])
def read_item(_id: int):
    repo = FileRepository()
    data = repo.get(_id)
    print(data)
    return Item(**data)


@router.put("/items/{_id}")
def update_item(item: Item, _id: int):
    repo = FileRepository()

    try:
        repo.update(item)
    except NotFound:
        return Response(status_code=status.HTTP_404_NOT_FOUND)

    return item


@router.delete("/items/{_id}", tags=["items"])
def delete_item(_id: int):
    repo = FileRepository()
    try:
        repo.get(_id)
    except NotFound:
        return Response(status=status.HTTP_404_NOT_FOUND)
    else:
        repo.delete(_id)

    return Response(status_code=status.HTTP_204_NO_CONTENT)
