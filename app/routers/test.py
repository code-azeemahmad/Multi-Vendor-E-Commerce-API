from typing import Annotated

from fastapi import APIRouter, Depends

from app.dependencies import (
    require_admin,
    require_vendor,
    require_customer,
)
from app.models.user import User

router = APIRouter(prefix="/test", tags=["RBAC Test"])


@router.get("/admin")
async def admin_test(
    current_user: Annotated[User, Depends(require_admin)],
):
    return {
        "message": "Welcome Admin",
        "user": current_user.email,
    }


@router.get("/vendor")
async def vendor_test(
    current_user: Annotated[User, Depends(require_vendor)],
):
    return {
        "message": "Welcome Vendor",
        "user": current_user.email,
    }


@router.get("/customer")
async def customer_test(
    current_user: Annotated[User, Depends(require_customer)],
):
    return {
        "message": "Welcome Customer",
        "user": current_user.email,
    }