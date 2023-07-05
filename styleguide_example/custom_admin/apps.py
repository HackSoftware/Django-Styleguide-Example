from django.contrib.admin.apps import AdminConfig as BaseAdminConfig


class CustomAdminConfig(BaseAdminConfig):
    default_site = "styleguide_example.custom_admin.sites.AdminSite"
