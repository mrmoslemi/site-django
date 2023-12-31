from django.db import models
import uuid


class PhraseField(models.JSONField):
    # TODO
    pass


class MultiSizeImageField(models.ImageField):
    # TODO
    pass


class BaseModel(models.Model):
    class Meta:
        abstract = True

    uuid = models.UUIDField(
        unique=True, db_index=True, default=uuid.uuid4, editable=False
    )


class CreatableModel(BaseModel):
    class Meta:
        abstract = True

    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(
        to="authentication.User",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        default=None,
    )


class UpdatableModel(BaseModel):
    class Meta:
        abstract = True

    updated_by = models.DateTimeField(auto_now_add=True)
    updated_at = models.ForeignKey(
        to="authentication.User",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        default=None,
    )


class DeletableModel(BaseModel):
    class Meta:
        abstract = True

    deleted_at = models.DateTimeField(auto_now_add=True)
    deleted_by = models.ForeignKey(
        to="authentication.User",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        default=None,
    )


class OrderedModel(BaseModel):
    class Meta:
        abstract = True
        ordering = ["order"]

    order = models.FloatField(default=0)


class AuditableModel(CreatableModel, UpdatableModel, DeletableModel):
    class Meta:
        abstract = True


class SuperModel(AuditableModel, OrderedModel):
    class Meta:
        abstract = True
