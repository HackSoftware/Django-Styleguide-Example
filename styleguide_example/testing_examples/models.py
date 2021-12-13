from uuid import uuid4

from django.db import models
from django.db.models.query import F, Q


class School(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True)

    def __str__(self):
        return self.name


class Student(models.Model):
    email = models.EmailField(max_length=255)
    identifier = models.UUIDField(default=uuid4)
    school = models.ForeignKey(School, related_name='students', on_delete=models.CASCADE)

    class Meta:
        unique_together = (
            ('email', 'school'),
            ('identifier', 'school'),
        )

    def __str__(self):
        return f'Student {self.email} ({self.identifier})'


class SchoolCourse(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255)
    school = models.ForeignKey(School, related_name='school_courses', on_delete=models.CASCADE)

    start_date = models.DateField()
    end_date = models.DateField()

    class Meta:
        constraints = [
            models.CheckConstraint(
                name="school_course_start_before_end",
                check=Q(start_date__lt=F("end_date"))
            )
        ]

        unique_together = (
            ('name', 'slug', 'start_date', 'end_date', ),
        )

    def __str__(self):
        return f'{self.name} in {self.school}'


class Roster(models.Model):
    student = models.ForeignKey(Student, related_name='rosters', on_delete=models.CASCADE)
    school_course = models.ForeignKey(SchoolCourse, related_name='rosters', on_delete=models.CASCADE)

    start_date = models.DateField()
    end_date = models.DateField()

    active = models.BooleanField(default=True)
    deactivated_at = models.DateField(null=True, blank=True)

    class Meta:
        constraints = [
            models.CheckConstraint(
                name="roster_start_before_end",
                check=Q(start_date__lt=F("end_date"))
            )
        ]
