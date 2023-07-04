from django.contrib.admin.apps import AdminConfig as BaseAdminConfig


class AdminConfig(BaseAdminConfig):
    default_site = "styleguide_example.admin.sites.AdminSite"
