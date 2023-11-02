from django.contrib import admin
from . import models


class InlineDescription(admin.TabularInline):
    model = models.Description
    fields = ["description"]


class InlineLink(admin.TabularInline):
    model = models.Link
    fields = ["title", "url"]


@admin.register(models.Experience)
class ExperienceAdmin(admin.ModelAdmin):
    list_display = ["company", "role", "start_date", "end_date", "duration"]
    inlines = [InlineDescription, InlineLink]
@admin.register(models.Link)
class LinkAdmin(admin.ModelAdmin):
    list_display = ["title","url","work"]

@admin.register(models.Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ["name", "type", "used_count"]


@admin.register(models.SkillType)
class SkillAdmin(admin.ModelAdmin):
    list_display = ["name", "order"]
