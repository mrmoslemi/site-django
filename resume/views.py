from django.shortcuts import render
from rest_framework import serializers
from .models import Skill, SkillType, Experience, Description, Link
from django.utils import timezone


class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = ["name", "type"]

    type = serializers.SerializerMethodField()

    def get_type(self, obj):
        return obj.type.name


class LinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Link
        fields = ["url", "title"]


class DescriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Description
        fields = ["description"]


class ExperienceSerialzier(serializers.ModelSerializer):
    class Meta:
        model = Experience
        fields = [
            "company",
            "role",
            "start_date",
            "end_date",
            "duration",
            "skills",
            "descriptions",
            "link_set",
        ]

    skills = serializers.SerializerMethodField()
    link_set = LinkSerializer(many=True)
    duration = serializers.SerializerMethodField()
    start_date = serializers.SerializerMethodField()
    end_date = serializers.SerializerMethodField()
    descriptions = DescriptionSerializer(many=True)

    def get_skills(self, obj):
        skills = obj.skills.all()
        titles = []
        for skill in skills:
            titles.append(skill.name)
        return ", ".join(titles)

    def get_start_date(self, obj):
        return obj.start_date.strftime("%b %Y")

    def get_end_date(self, obj):
        if obj.end_date:
            return obj.end_date.strftime("%b %Y")
        else:
            return "Present"

    def get_duration(self, obj):
        duration = obj.duration
        days = duration.days
        years = int(days / 365)
        months = int((days - (365 * years)) / 28)
        y = None
        if years == 1:
            y = "1 year"
        if years > 1:
            y = f"{years} years"
        m = None
        if months == 1:
            m = "1 month"
        if months > 1:
            m = f"{months} months"
        if y and m:
            return f"{y} and {m}"
        if y:
            return y
        if m:
            return m


class SkillFullSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = ["name", "duration"]

    duration = serializers.SerializerMethodField()

    def get_duration(self, obj):
        from datetime import timedelta

        experiences = Experience.objects.filter(skills=obj)
        duration = timedelta(0)
        for experience in experiences:
            if experience.id != 10:
                duration += experience.duration
            else:
                duration += timedelta(days=366)
        years = max(int(duration.days / 365), 1)
        return years


def resume_view(request):
    experiences = ExperienceSerialzier(Experience.objects.exclude(id=10), many=True).data
    educations = ExperienceSerialzier(Experience.objects.filter(id=10), many=True).data
    skills = SkillFullSerializer(Skill.objects.all(), many=True).data
    return render(
        request, "resume.html", {"experiences": experiences,"educations":educations, "skills": skills}
    )


def resume_md(request):
    experiences = ExperienceSerialzier(
        Experience.objects.exclude(id=10), many=True
    ).data
    educations = ExperienceSerialzier(Experience.objects.filter(id=10), many=True).data
    skills = SkillFullSerializer(Skill.objects.all(), many=True).data
    links = LinkSerializer(Link.objects.all(), many=True).data
    return render(
        request,
        "resume_md.html",
        {
            "experiences": experiences,
            "educations": educations,
            "links": links,
            "skills": skills,
        },
    )
