from app.repositories.dashboard_repository import DashboardRepository


class DashboardService:

    def __init__(self, db):
        self.repository = DashboardRepository(db)

    def get_summary(self, user_id: int) -> dict:
        return self.repository.get_summary(user_id)

    def get_category_expenses(self, user_id: int) -> list[dict]:
        return self.repository.get_category_expenses(user_id)

    def get_monthly_summary(self, user_id: int) -> list[dict]:
        return self.repository.get_monthly_summary(user_id)