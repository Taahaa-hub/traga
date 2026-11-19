from django.urls import path

from . import views

app_name = "pages"

urlpatterns = [
    path("", views.accueil, name="accueil"),
    path("a-propos/", views.a_propos, name="a_propos"),
    path("gants/", views.categorie, {"categorie_slug": "gants"}, name="gants"),
    path("protections/", views.categorie, {"categorie_slug": "protections"}, name="protections"),
    path("accessoires/", views.categorie, {"categorie_slug": "accessoires"}, name="accessoires"),
    path("pack-complet/", views.categorie, {"categorie_slug": "pack-complet"}, name="pack_complet"),
    path(
        "<slug:category_slug>/<slug:product_slug>/",
        views.product_detail,
        name="product_detail",
    ),
]
