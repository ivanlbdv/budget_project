from budget.views import custom_400, custom_403, custom_404, custom_500
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('budget.urls')),
]

handler400 = custom_400
handler403 = custom_403
handler404 = custom_404
handler500 = custom_500
