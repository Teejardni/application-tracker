from tortoise import models, fields


class ApplicationEvent(models.Model):
    id = fields.IntField(pk=True)

    application = fields.ForeignKeyField(
        "models.Application",
        related_name="events",
        on_delete=fields.CASCADE,
    )

    event_type = fields.CharField(max_length=50)
    event_date = fields.DatetimeField()
    metadata = fields.JSONField(null=True)

    class Meta:
        table = "application_events"

