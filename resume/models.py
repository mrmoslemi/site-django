from django.db import models
from django.utils import timezone


class Experience(models.Model):
    class Meta:
        ordering = ["-start_date"]

    company = models.CharField(max_length=100)
    logo = models.ImageField(null=True, blank=True, default=None)
    role = models.CharField(max_length=100)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True, default=None)
    skills = models.ManyToManyField(to="Skill", blank=True, related_name="experiences")
    def __str__(self) -> str:
        return self.company
    @property
    def duration(self):
        if self.end_date:
            return self.end_date - self.start_date
        else:
            return timezone.now().date() - self.start_date


class Link(models.Model):
    class Meta:
        ordering = ["work__start_date","id"]
    work = models.ForeignKey(to='Experience',on_delete=models.CASCADE)
    url = models.URLField()
    title = models.CharField(max_length=20)


class Description(models.Model):
    class Meta:
        ordering = ["order"]

    experience = models.ForeignKey(
        to=Experience, on_delete=models.CASCADE, related_name="descriptions"
    )
    order = models.FloatField(default=0)
    description = models.CharField(max_length=200)


def get_next_order():
    if Skill.objects.all().exists():
        return Skill.objects.last().order + 1
    else:
        return 1


class SkillType(models.Model):
    class Meta:
        ordering = ["order"]

    name = models.CharField(max_length=100)
    order = models.FloatField(default=0)

    def __str__(self) -> str:
        return self.name


class Skill(models.Model):
    class Meta:
        ordering = ["type__order", "order"]

    order = models.FloatField(default=get_next_order)
    name = models.CharField(max_length=50)
    type = models.ForeignKey(
        to="SkillType", null=True, blank=True, default=None, on_delete=models.SET_NULL
    )

    def __str__(self) -> str:
        return self.name

    @property
    def used_count(self):
        return self.experiences.count()
