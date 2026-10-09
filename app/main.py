from fastapi import FastAPI

from app.routers import auth, users, categories,transactions
from app.routers import dashboard

app = FastAPI(
    title="Expense tracker",
    description="Using my backend skills to buid the expense tracter ",
    version="1.0"
)

app.include_router(auth.router)
app.include_router(users.router)
app.include_router(categories.router)
app.include_router(transactions.router)
app.include_router(dashboard.router)


@app.get("/health")
def health_check():
    return {
        "status": "ok"
    }
