from tortoise import models, fields


class Application(models.Model):
    id = fields.IntField(pk=True)

    company = fields.CharField(max_length=255)
    role_title = fields.CharField(max_length=255)

    location = fields.CharField(max_length=255, null=True)
    source = fields.CharField(max_length=100, null=True)

    date_applied = fields.DateField()
    status = fields.CharField(max_length=50)

    salary_min = fields.IntField(null=True)
    salary_max = fields.IntField(null=True)

    relocation = fields.BooleanField(null=True)
    visa_sponsorship = fields.CharField(max_length=50, null=True)

    notes = fields.TextField(null=True)
    last_updated = fields.DatetimeField(auto_now=True)

    class Meta:
        table = "applications"

