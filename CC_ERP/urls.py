"""
CC_ERPP URL Configuration
"""

from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from auth_access_admin.admin import admin_site
from frontpage.admin import advanced_admin

urlpatterns = [
    path('stucture_admin/',
         admin_site.urls,
         ),
    path('2233ddffaq6e85rg46ern/', advanced_admin.urls),
    path("", include("frontpage.urls", namespace="frontpage")),
    path("auth/", include("auth_access_admin.urls", namespace="auth")),
    path("day-to-day/", include("day_to_day.urls", namespace="d_to_d"))
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


handler404 = "frontpage.views.page_not_found_view"
handler500 = "frontpage.views.error_view"
handler403 = "frontpage.views.permission_denied_view"

if settings.DEBUG:
    import debug_toolbar

    urlpatterns = [
        path(
            "__debug__/",
            include(
                debug_toolbar.urls)),
    ] + urlpatterns
