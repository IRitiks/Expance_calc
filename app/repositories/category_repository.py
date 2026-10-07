from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.category import Category


class CategoryRepository:

    def __init__(self, db: Session):
        self.db = db

    def create(self, category: Category) -> Category:
        self.db.add(category)
        self.db.commit()
        self.db.refresh(category)

        return category

    def get_by_id(
        self,
        category_id: int,
        user_id: int,
    ) -> Category | None:

        statement = select(Category).where(
            Category.id == category_id,
            Category.user_id == user_id,
        )

        return self.db.scalar(statement)

    def get_all(
        self,
        user_id: int,
    ) -> list[Category]:

        statement = (
            select(Category)
            .where(Category.user_id == user_id)
            .order_by(Category.name)
        )

        return list(self.db.scalars(statement).all())

    def delete(self, category: Category) -> None:
        self.db.delete(category)
        self.db.commit()