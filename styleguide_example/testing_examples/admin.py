from django.contrib import admin

from styleguide_example.testing_examples.models import (
    School,
    SchoolCourse,
    Student,
    Roster
)


@admin.register(School)
class SchoolAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', )


@admin.register(Roster)
class RosterAdmin(admin.ModelAdmin):
    list_display = ('student', 'school_course', 'start_date', 'end_date', 'active', )
    list_filter = ('student', 'school_course')


class RosterStudentInline(admin.TabularInline):
    model = Roster
    fields = ('school_course', 'start_date', 'end_date', 'active', 'deactivated_at', )
    extra = 1


class RosterSchoolCourseInline(admin.TabularInline):
    model = Roster
    fields = ('student', 'start_date', 'end_date', 'active', 'deactivated_at', )
    extra = 1


@admin.register(SchoolCourse)
class SchoolCourseAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'school', 'start_date', 'end_date', )
    list_filter = ('school', )
    inlines = (RosterSchoolCourseInline, )


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('email', 'identifier', 'school', )
    list_filter = ('school', )
    inlines = (RosterStudentInline, )
