from django.contrib import admin

from styleguide_example.test_examples.models import (
    School,
    SchoolClass,
    Student,
    Roster
)


@admin.register(School)
class SchoolAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', )


@admin.register(Roster)
class RosterAdmin(admin.ModelAdmin):
    list_display = ('student', 'school_class', 'start_date', 'end_date', 'active', )
    list_filter = ('student', 'school_class')


class RosterStudentInline(admin.TabularInline):
    model = Roster
    fields = ('school_class', 'start_date', 'end_date', 'active', 'deactivated_at', )
    extra = 1


class RosterSchoolClassInline(admin.TabularInline):
    model = Roster
    fields = ('student', 'start_date', 'end_date', 'active', 'deactivated_at', )
    extra = 1


@admin.register(SchoolClass)
class SchoolClassAdmin(admin.ModelAdmin):
    list_display = ('name', 'short_name', 'slug', 'school', 'start_date', 'end_date', )
    list_filter = ('school', )
    inlines = (RosterSchoolClassInline, )


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('email', 'identifier', 'school', )
    list_filter = ('school', )
    inlines = (RosterStudentInline, )
