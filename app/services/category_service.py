from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.category import Category
from app.repositories.category_repository import CategoryRepository
from app.schemas.category import CategoryCreate, CategoryUpdate


class CategoryService:

    def __init__(self, db: Session):
        self.repository = CategoryRepository(db)

    def create(
        self,
        category_data: CategoryCreate,
        user_id: int,
    ) -> Category:

        category = Category(
            name=category_data.name,
            type=category_data.type,
            user_id=user_id,
        )

        return self.repository.save(category)

    def get_all(
        self,
        user_id: int,
    ) -> list[Category]:

        return self.repository.get_all(user_id)

    def get_by_id(
        self,
        category_id: int,
        user_id: int,
    ) -> Category:

        category = self.repository.get_by_id(
            category_id,
            user_id,
        )

        if not category:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Category not found",
            )

        return category

    def update(
        self,
        category_id: int,
        category_data: CategoryUpdate,
        user_id: int,
    ) -> Category:

        category = self.get_by_id(
            category_id,
            user_id,
        )

        if category_data.name is not None:
            category.name = category_data.name

        if category_data.type is not None:
            category.type = category_data.type

        return self.repository.save(category)

    def delete(
        self,
        category_id: int,
        user_id: int,
    ) -> None:

        category = self.get_by_id(
            category_id,
            user_id,
        )

        self.repository.delete(category)

    def save(self, category: Category) -> Category:
        self.db.add(category)
        self.db.commit()
        self.db.refresh(category)

        return category

    