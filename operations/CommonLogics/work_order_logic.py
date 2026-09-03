from django.db import transaction
from django.utils import timezone

from catalog.models import WorkOrderStatus
from operations.models import WorkOrder


class WorkOrderLogic:
    """Business rules for work-order lifecycle — kept out of views."""

    @staticmethod
    def next_reference(client_code: str) -> str:
        stamp = timezone.now().strftime("%y%m%d%H%M%S")
        return f"WO-{client_code.upper()}-{stamp}"

    @staticmethod
    @transaction.atomic
    def assign(work_order: WorkOrder, technician, actor: str) -> WorkOrder:
        assigned = WorkOrderStatus.objects.get(code="assigned")
        work_order.assigned_to = technician
        work_order.status = assigned
        work_order.last_modified_by = actor
        work_order.save(
            update_fields=["assigned_to", "status", "last_modified_by", "last_modified_at"]
        )
        return work_order

    @staticmethod
    @transaction.atomic
    def complete(work_order: WorkOrder, actor: str) -> WorkOrder:
        done = WorkOrderStatus.objects.get(code="completed")
        work_order.status = done
        work_order.completed_at = timezone.now()
        work_order.last_modified_by = actor
        work_order.save(
            update_fields=["status", "completed_at", "last_modified_by", "last_modified_at"]
        )
        return work_order
