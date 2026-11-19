from urllib.parse import urlencode

from django.http import Http404
from django.shortcuts import render
from django.urls import reverse
from django.utils.text import slugify

from .forms import CategoryFilterForm, ProductFilterForm


WHATSAPP_NUMBER = "212723368026"

CATEGORY_TYPE_LABELS = {
    "protege-tibias": "Protège-tibias",
    "protege-dents": "Protège-dents",
    "casque": "Casques",
    "bandages": "Bandages",
    "corde-a-sauter": "Cordes à sauter",
    "protege-chevilles": "Protège-chevilles",
    "t-shirts": "T-shirts",
    "shorts": "Shorts",
}

CATALOGUE = {
    "gants": {
        "name": "Gants de boxe",
        "eyebrow": "FRAPPE & ENTRAÎNEMENT",
        "description": "Choisissez des gants adaptés à vos séances, au sac comme lors des combats d’entraînement.",
        "image": "pages/category-gants-hero.jfif",
        "price_note": "Prix habituel : 300 DH · prix promotionnel : 220 DH.",
        "original_price": 300,
        "products": [
            {
                "name": "Gants Venum Contender 2.0",
                "variant": "Noir et blanc",
                "color": "Noir et blanc",
                "brand": "VENUM",
                "price": 220,
                "image": "pages/products/gants-11.jpg",
            },
            {
                "name": "Gants Venum Contender 2.0",
                "variant": "Blanc, gris et noir",
                "color": "Blanc, gris et noir",
                "brand": "VENUM",
                "price": 220,
                "image": "pages/products/gants-04.jpg",
            },
            {
                "name": "Gants Venum Stone",
                "variant": "Vert minéral",
                "color": "Vert minéral",
                "brand": "VENUM",
                "price": 220,
                "image": "pages/products/gants-08.jpg",
            },
            {
                "name": "Gants Venum Elite",
                "variant": "Noir et rouge",
                "color": "Noir et rouge",
                "brand": "VENUM",
                "price": 220,
                "image": "pages/products/gants-05.jpg",
            },
            {
                "name": "Gants Venum Challenger 3.0",
                "variant": "Noir",
                "color": "Noir",
                "brand": "VENUM",
                "price": 220,
                "image": "pages/products/gants-10.jpg",
            },
            {
                "name": "Gants Venum Impact",
                "variant": "Camouflage sombre et sable",
                "color": "Camouflage sombre et sable",
                "brand": "VENUM",
                "price": 220,
                "image": "pages/products/gants-01.jpg",
            },
            {
                "name": "Gants Venum roses",
                "variant": "Rose et blanc",
                "color": "Rose et blanc",
                "brand": "VENUM",
                "price": 220,
                "image": "pages/products/gants-12.jpg",
            },
            {
                "name": "Gants de kick-boxing Fairtex × GLORY",
                "variant": "Noir",
                "color": "Noir",
                "brand": "FAIRTEX × GLORY",
                "price": 220,
                "image": "pages/products/gants-09.jpg",
            },
            {
                "name": "Gants de kick-boxing Fairtex × GLORY",
                "variant": "Blanc et noir",
                "color": "Blanc et noir",
                "brand": "FAIRTEX × GLORY",
                "price": 220,
                "image": "pages/products/gants-02.jpg",
            },
            {
                "name": "Gants de kick-boxing Fairtex × GLORY",
                "variant": "BGVG1 - Fermeture auto-agrippante",
                "brand": "FAIRTEX × GLORY",
                "price": 220,
                "image": "pages/products/gants-06.jpg",
            },
            {
                "name": "Gants de compétition de kick-boxing Fairtex × GLORY",
                "variant": "Blanc et noir",
                "color": "Blanc et noir",
                "brand": "FAIRTEX × GLORY",
                "price": 220,
                "image": "pages/products/gants-07.jpg",
            },
            {
                "name": "Gants Venum Impact",
                "variant": "Noir et or",
                "color": "Noir et or",
                "brand": "VENUM",
                "price": 220,
                "image": "pages/products/gants-03.jpg",
            },
        ],
    },
    "protections": {
        "name": "Protections",
        "eyebrow": "SÉCURITÉ & CONFORT",
        "description": "Les protections essentielles pour vous entraîner en toute confiance.",
        "image": "pages/protections-hero.jfif",
        "products": [
            {
                "name": "Protège-tibia ZTT - noir",
                "brand": "ZTT",
                "filter_type": "protege-tibias",
                "color": "Noir",
                "image": "pages/products/01.jpg",
            },
            {
                "name": "Protège-tibia FAFA - doré et noir",
                "brand": "FAFA SPORT",
                "filter_type": "protege-tibias",
                "color": "Doré et noir",
                "image": "pages/products/02.jpg",
            },
            {
                "name": "Protège-dents Venum Predator Competition Series - orange et noir",
                "brand": "VENUM",
                "filter_type": "protege-dents",
                "color": "Orange et noir",
                "image": "pages/products/05.jpg",
            },
            {
                "name": "Protège-dents Venum Predator Competition Series - bleu et noir",
                "brand": "VENUM",
                "filter_type": "protege-dents",
                "color": "Bleu et noir",
                "image": "pages/products/06.jpg",
            },
            {
                "name": "Protège-dents Venum Predator Competition Series - blanc et noir",
                "brand": "VENUM",
                "filter_type": "protege-dents",
                "color": "Blanc et noir",
                "image": "pages/products/07.jpg",
            },
            {
                "name": "Protège-dents Venum Predator Competition Series - noir et blanc",
                "brand": "VENUM",
                "filter_type": "protege-dents",
                "color": "Noir et blanc",
                "image": "pages/products/08.jpg",
            },
            {
                "name": "Protège-dents Venum Predator Competition Series - noir et rouge",
                "brand": "VENUM",
                "filter_type": "protege-dents",
                "color": "Noir et rouge",
                "image": "pages/products/09.jpg",
            },
            {
                "name": "Protège-dents FAFA SPORT - bleu",
                "brand": "FAFA SPORT",
                "filter_type": "protege-dents",
                "color": "Bleu",
                "image": "pages/products/13.jpg",
            },
            {
                "name": "Protège-dents FAFA SPORT - jaune",
                "brand": "FAFA SPORT",
                "filter_type": "protege-dents",
                "color": "Jaune",
                "image": "pages/products/14.jpg",
            },
            {
                "name": "Casque de boxe ouvert - noir et rouge",
                "brand": "VENUM",
                "filter_type": "casque",
                "color": "Noir et rouge",
                "image": "pages/products/15.jpg",
            },
            {
                "name": "Casque de boxe ouvert - noir et blanc",
                "brand": "VENUM",
                "filter_type": "casque",
                "color": "Noir et blanc",
                "image": "pages/products/16.jpg",
            },
        ],
    },
    "accessoires": {
        "name": "Accessoires",
        "eyebrow": "POUR VOTRE ENTRAÎNEMENT",
        "description": "Complétez votre équipement avec les indispensables de la salle.",
        "image": "pages/accessoires-hero.jfif",
        "products": [
            {
                "name": "Bandages de boxe et de MMA PAKKA",
                "brand": "PAKKA",
                "category_type": "bandages",
                "image": "pages/products/03.jpg",
            },
            {
                "name": "Corde à sauter réglable PAKKA - fitness, boxe et CrossFit",
                "brand": "PAKKA",
                "category_type": "corde-a-sauter",
                "image": "pages/products/04.jpg",
            },
            {
                "name": "Protège-cheville PAKKA - noir",
                "brand": "PAKKA",
                "category_type": "protege-chevilles",
                "color": "Noir",
                "image": "pages/products/10.jpg",
            },
            {
                "name": "Protège-cheville PAKKA - bleu",
                "brand": "PAKKA",
                "category_type": "protege-chevilles",
                "color": "Bleu",
                "image": "pages/products/11.jpg",
            },
            {
                "name": "Protège-cheville FAFA - rouge",
                "brand": "FAFA SPORT",
                "category_type": "protege-chevilles",
                "color": "Rouge",
                "image": "pages/products/12.jpg",
            },
            {
                "name": "T-shirt Venum UFC Fight - blanc et noir",
                "brand": "VENUM",
                "category_type": "t-shirts",
                "color": "Blanc et noir",
                "image": "pages/products/accessoires-01.jfif",
            },
            {
                "name": "T-shirt Venum UFC Fight - noir et rouge",
                "brand": "VENUM",
                "category_type": "t-shirts",
                "color": "Noir et rouge",
                "image": "pages/products/accessoires-02.jfif",
            },
            {
                "name": "Short de boxe thaï Venum - gris et blanc",
                "brand": "VENUM",
                "category_type": "shorts",
                "color": "Gris et blanc",
                "image": "pages/products/accessoires-03.jfif",
            },
            {
                "name": "Short de boxe thaï Wiked - vert noir",
                "brand": "WIKED",
                "category_type": "shorts",
                "color": "Vert noir",
                "image": "pages/products/accessoires-04.jfif",
            },
            {
                "name": "Fairtex BS1947 Muaythai Short - noir et jaune",
                "brand": "FAIRTEX",
                "category_type": "shorts",
                "color": "Noir et jaune",
                "image": "pages/products/accessoires-05.jfif",
            },
            {
                "name": "BSG3 Fairtex Official GLORY Short - blanc",
                "brand": "FAIRTEX × GLORY",
                "category_type": "shorts",
                "color": "Blanc",
                "image": "pages/products/accessoires-06.jfif",
            },
        ],
    },
    "pack-complet": {
        "name": "Pack complet",
        "eyebrow": "ÉQUIPEMENT DE BOXE",
        "description": "Choisissez le pack de boxe qui correspond à votre entraînement.",
        "image": "pages/hero-warrior.jfif",
        "price_note": "Contactez-nous pour connaître les tailles, les disponibilités et le prix de chaque pack.",
        "products": [
            {
                "name": "Pack complet 1",
                "image": "pages/products/pack-complet-01.jfif",
            },
            {
                "name": "Pack complet 2",
                "image": "pages/products/pack-complet-02.jfif",
            },
            {
                "name": "Pack complet 3",
                "image": "pages/products/pack-complet-03.jfif",
            },
        ],
    },
}


def _products_for_category(category, category_slug):
    products = []
    used_slugs = set()
    for product_index, product in enumerate(category["products"], start=1):
        product_slug = slugify(
            " ".join(
                value
                for value in (product["name"], product.get("variant", ""))
                if value
            )
        )
        if product_slug in used_slugs:
            product_slug = "{0}-{1}".format(product_slug, product_index)
        used_slugs.add(product_slug)
        order_message = (
            "Bonjour, je souhaite commander : {0}. Merci de confirmer la disponibilité, "
            "les tailles et les modalités avant commande."
        ).format(product["name"])
        if product.get("price") is not None:
            order_message += " Prix : {0} DH.".format(product["price"])
        products.append(
            {
                **product,
                "category_name": category["name"],
                "category_slug": category_slug,
                "slug": product_slug,
                "original_price": product.get("original_price", category.get("original_price")),
                "display_brand": product.get("brand") or category["name"],
                "filter_brand": product.get("brand") or "other",
                "filter_type": product.get("filter_type", category_slug),
                "category_type": product.get(
                    "category_type",
                    product.get("filter_type", category_slug),
                ),
                "filter_color": product.get("color", ""),
                "order_url": "https://wa.me/{0}?{1}".format(
                    WHATSAPP_NUMBER,
                    urlencode({"text": order_message}),
                ),
                "detail_url": reverse(
                    "pages:product_detail",
                    kwargs={
                        "category_slug": category_slug,
                        "product_slug": product_slug,
                    },
                ),
            }
        )
    return products


def accueil(request):
    filter_requested = request.GET.get("filter") == "1"
    product_filter_form = ProductFilterForm(request.GET if filter_requested else None)
    filter_results = []
    if filter_requested and product_filter_form.is_valid():
        filters = product_filter_form.cleaned_data
        for category_slug, category in CATALOGUE.items():
            for product in _products_for_category(category, category_slug):
                if filters["product_type"] and product["filter_type"] != filters["product_type"]:
                    continue
                if filters["brand"] and product["filter_brand"] != filters["brand"]:
                    continue
                price = product.get("price")
                if (
                    filters["price_min"] is not None
                    or filters["price_max"] is not None
                ) and price is None:
                    continue
                if filters["price_min"] is not None and price < filters["price_min"]:
                    continue
                if filters["price_max"] is not None and price > filters["price_max"]:
                    continue
                filter_results.append(product)

    featured_products = [
        _products_for_category(CATALOGUE[category_slug], category_slug)[0]
        for category_slug in ("gants", "protections", "accessoires", "pack-complet")
    ]
    contexte = {
        "nom_projet": "elfighter store",
        "product_filter_form": product_filter_form,
        "filter_requested": filter_requested,
        "filter_results": filter_results,
        "featured_products": featured_products,
    }
    return render(request, "pages/accueil.html", contexte)


def a_propos(request):
    contexte = {
        "version_projet": "1.0",
    }
    return render(request, "pages/a_propos.html", contexte)


def categorie(request, categorie_slug):
    category = CATALOGUE[categorie_slug]
    products = _products_for_category(category, categorie_slug)
    type_values = {product["category_type"] for product in products}
    type_choices = tuple(
        (value, CATEGORY_TYPE_LABELS.get(value, category["name"]))
        for value in sorted(type_values)
    )
    brand_values = {
        (product["filter_brand"], product["display_brand"])
        for product in products
    }
    brand_choices = tuple(sorted(brand_values, key=lambda choice: choice[1].casefold()))
    color_values = sorted(
        {product["filter_color"] for product in products if product["filter_color"]},
        key=str.casefold,
    )
    color_choices = tuple((color, color) for color in color_values)
    filter_form = CategoryFilterForm(
        request.GET if request.GET else None,
        type_choices=type_choices,
        brand_choices=brand_choices,
        color_choices=color_choices,
    )
    if filter_form.is_bound:
        if filter_form.is_valid():
            filters = filter_form.cleaned_data
            query = filters["query"].casefold().strip()
            products = [
                product
                for product in products
                if (not filters["type"] or product["category_type"] == filters["type"])
                and (not filters["brand"] or product["filter_brand"] == filters["brand"])
                and (not filters["color"] or product["filter_color"] == filters["color"])
                and (
                    not query
                    or query
                    in " ".join(
                        str(product.get(key, ""))
                        for key in ("name", "variant", "description", "brand")
                    ).casefold()
                )
            ]
        else:
            products = []
    return render(
        request,
        "pages/categorie.html",
        {
            "category": category,
            "category_slug": categorie_slug,
            "products": products,
            "category_filter_form": filter_form,
            "category_type_choices": type_choices,
            "category_brand_choices": brand_choices,
            "category_color_choices": color_choices,
            "category_path": "/{0}/".format(categorie_slug),
        },
    )


def product_detail(request, category_slug, product_slug):
    category = CATALOGUE.get(category_slug)
    if category is None:
        raise Http404("Produit introuvable")

    products = _products_for_category(category, category_slug)
    product = next(
        (item for item in products if item["slug"] == product_slug),
        None,
    )
    if product is None:
        raise Http404("Produit introuvable")

    related_products = [
        item for item in products if item["slug"] != product_slug
    ][:4]
    return render(
        request,
        "pages/product_detail.html",
        {
            "category": category,
            "product": product,
            "related_products": related_products,
        },
    )