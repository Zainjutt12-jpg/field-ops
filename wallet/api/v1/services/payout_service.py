from django.db import transaction
from rest_framework.exceptions import ValidationError

from wallet.models import PayoutRequest, PayoutStatus


class PayoutService:
    """Maker-checker payout flow (skeleton)."""

    @staticmethod
    @transaction.atomic
    def submit_for_approval(payout: PayoutRequest, actor: str) -> PayoutRequest:
        if payout.status != PayoutStatus.DRAFT:
            raise ValidationError("Only draft payouts can be submitted.")
        payout.status = PayoutStatus.PENDING_APPROVAL
        payout.last_modified_by = actor
        payout.save(update_fields=["status", "last_modified_by", "last_modified_at"])
        return payout

    @staticmethod
    @transaction.atomic
    def approve(payout: PayoutRequest, checker, actor: str) -> PayoutRequest:
        if payout.status != PayoutStatus.PENDING_APPROVAL:
            raise ValidationError("Only pending payouts can be approved.")
        if payout.maker_id == checker.id:
            raise ValidationError("Maker cannot approve their own payout.")
        payout.status = PayoutStatus.APPROVED
        payout.checker = checker
        payout.last_modified_by = actor
        payout.save(update_fields=["status", "checker", "last_modified_by", "last_modified_at"])
        return payout
