from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from uuid import UUID
from typing import Optional

from backend.core.database import get_db
from backend.middleware.rbac import RoleChecker
from backend.modules.payments.schema import PayoutLogRequest, PayoutResponse, PaymentRosterResponse
from backend.modules.payments.service import PaymentService

router = APIRouter(tags=["Payments"])

# Role guards
admin_guard = RoleChecker(allowed_roles=["ADMIN"])
user_guard = RoleChecker(allowed_roles=["MEMBER", "LEADER", "ADMIN", "DEVELOPER"])

def map_payment_to_response(tx) -> dict:
    """Helper to cleanly serialize DB PaymentTransaction model into the API schema shape."""
    return {
        "transaction_id": tx.id,
        "claim_id": tx.claim_id,
        "user_id": tx.user_id,
        "amount": float(tx.amount),
        "transaction_reference": tx.transaction_reference,
        "status": tx.status,
        "paid_at": tx.paid_at
    }

@router.get("/payments", response_model=PaymentRosterResponse)
def get_payment_history(
    page: int = 1,
    limit: int = 20,
    status_filter: Optional[str] = None,
    filter_user_id: Optional[UUID] = None,
    db: Session = Depends(get_db),
    auth_user: dict = Depends(user_guard)
):
    """
    Fetch paginated lists of logged payment transactions.
    - Standard citizens strictly retrieve their own payment summaries.
    - Admins query global ledgers.
    """
    user_id = UUID(auth_user.get("sub"))
    role = auth_user.get("role")
    service = PaymentService(db)
    
    result = service.get_payment_logs(
        user_id=user_id,
        role=role,
        page=page,
        limit=limit,
        status=status_filter,
        filter_user_id=filter_user_id
    )
    return {
        "items": [map_payment_to_response(tx) for tx in result["items"]],
        "total": result["total"],
        "page": result["page"],
        "limit": result["limit"]
    }

@router.post("/admin/payments/{id}/paid", response_model=PayoutResponse)
def process_manual_payout(
    id: UUID,
    payload: PayoutLogRequest,
    db: Session = Depends(get_db),
    auth_user: dict = Depends(admin_guard)
):
    """
    Logs administrative manual reference disbursement details for a pending payout transaction.
    Transitioning this transaction to PAID automatically marks the corresponding Claim as PAID
    and unlocks the milestone level progression block.
    Restricted strictly to administrators.
    """
    admin_id = UUID(auth_user.get("sub"))
    service = PaymentService(db)
    try:
        tx = service.disburse_manual_payout(admin_id, id, payload)
        return map_payment_to_response(tx)
    except ValueError as e:
        err = str(e)
        if err == "TRANSACTION_NOT_FOUND":
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail={"code": "TRANSACTION_NOT_FOUND", "message": "No payment transaction found matching the provided identifier."}
            )
        elif err == "TRANSACTION_ALREADY_PAID":
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail={"code": "TRANSACTION_ALREADY_PAID", "message": "This payout transaction has already been processed and paid."}
            )
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"code": "PAYMENT_DISBURSEMENT_FAILED", "message": err}
        )
