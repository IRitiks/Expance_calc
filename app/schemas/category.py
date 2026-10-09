from pydantic import BaseModel, Field

from app.models.category import CategoryType


class CategoryCreate(BaseModel):
    name: str = Field(
        min_length=1,
        max_length=100
    )
    # user_id:int
    trnx_type: CategoryType = Field(..., validation_alias="type")

class CategoryUpdate(BaseModel):
    name: str | None = Field(
        default=None,
        min_length=1,
        max_length=100
    )

    trnx_type: CategoryType | None = None

class CategoryResponse(BaseModel):
    category_id: int
    name: str
    trnx_type: CategoryType

    model_config = {
        "from_attributes": True
    }