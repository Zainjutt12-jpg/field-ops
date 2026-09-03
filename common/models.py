from django.db import models
from django.utils import timezone


class SoftDeleteQuerySet(models.QuerySet):
    def delete(self):
        return super().update(is_deleted=True, deleted_at=timezone.now())

    def hard_delete(self):
        return super().delete()

    def alive(self):
        return self.filter(is_deleted=False)


class SoftDeleteManager(models.Manager):
    def get_queryset(self):
        return SoftDeleteQuerySet(self.model, using=self._db).filter(is_deleted=False)


class BaseModel(models.Model):
    """Audit fields shared across domain entities."""

    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.CharField(max_length=200, null=True, blank=True)
    last_modified_at = models.DateTimeField(auto_now=True, null=True, blank=True)
    last_modified_by = models.CharField(max_length=200, null=True, blank=True)

    class Meta:
        abstract = True


class SoftDeletedModel(BaseModel):
    is_deleted = models.BooleanField(default=False)
    deleted_at = models.DateTimeField(null=True, blank=True)
    deleted_by = models.CharField(max_length=200, null=True, blank=True)

    objects = SoftDeleteManager()
    original = models.Manager()

    class Meta:
        abstract = True

    def soft_delete(self, deleted_by: str | None = None):
        self.is_deleted = True
        self.deleted_at = timezone.now()
        self.deleted_by = deleted_by
        self.save(update_fields=["is_deleted", "deleted_at", "deleted_by", "last_modified_at"])
