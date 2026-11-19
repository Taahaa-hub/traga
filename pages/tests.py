import re

from django.test import TestCase


class CategoryPageTests(TestCase):
    def test_each_category_has_a_product_page(self):
        categories = (
            ("gants", "Gants de boxe", "category-gants-hero.jfif"),
            ("protections", "Protections", "protections-hero.jfif"),
            ("accessoires", "Accessoires", "accessoires-hero.jfif"),
            ("pack-complet", "Pack complet", "hero-warrior.jfif"),
        )

        for url_name, title, image in categories:
            with self.subTest(category=url_name):
                response = self.client.get(f"/{url_name}/")

                self.assertEqual(response.status_code, 200)
                self.assertContains(response, title)
                self.assertContains(response, "data-image-viewer")
                self.assertContains(response, "Voir la fiche produit")
                self.assertContains(response, "Commander sur WhatsApp")
                self.assertContains(response, "wa.me/212723368026?text=")
                self.assertContains(response, image)
                self.assertContains(
                    response,
                    'class="product-showcase product-showcase--dark"'
                    if url_name in ("gants", "protections", "accessoires", "pack-complet")
                    else 'class="product-showcase"',
                )

    def test_home_category_cards_link_to_their_pages(self):
        response = self.client.get("/")

        self.assertEqual(response.status_code, 200)
        self.assertLess(
            response.content.index(b'class="hero"'),
            response.content.index(b'class="categories"'),
        )
        self.assertLess(
            response.content.index(b'class="categories"'),
            response.content.index(b'class="featured-products"'),
        )
        self.assertLess(
            response.content.index(b'class="featured-products"'),
            response.content.index(b'class="product-finder"'),
        )
        for url_name in ("gants", "protections", "accessoires", "pack-complet"):
            with self.subTest(category=url_name):
                self.assertContains(response, f'href="/{url_name}/"')
        self.assertNotContains(response, "Bandes de boxe")
        self.assertEqual(len(response.context["featured_products"]), 4)
        self.assertContains(response, "Une sélection pour votre entraînement")
        self.assertContains(response, "Comment commander")
        self.assertContains(response, "Les détails à vérifier ensemble")
        self.assertContains(response, "Frais et délais à confirmer selon votre ville.")
        self.assertContains(response, "Demandez les conditions de retour avant votre achat.")
        self.assertContains(response, "class=\"header-cta\"")
        self.assertContains(response, "Nous contacter sur WhatsApp")
        for href in ("/gants/", "/protections/", "/accessoires/", "/pack-complet/"):
            self.assertContains(response, f'href="{href}"')

    def test_product_detail_shows_confirmed_product_info_and_order_link(self):
        listing = self.client.get("/gants/")
        product = listing.context["products"][0]

        response = self.client.get(product["detail_url"])

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["product"]["name"], product["name"])
        self.assertContains(response, product["variant"])
        self.assertContains(response, "220 DH")
        self.assertContains(response, "Disponibilité")
        self.assertContains(response, "Modalités à confirmer avant commande")
        self.assertContains(response, "Commander sur WhatsApp")
        self.assertContains(response, "Dans la même catégorie")
        self.assertContains(response, 'class="product-detail__image-button"')
        self.assertContains(response, 'class="image-viewer"')

    def test_all_catalogue_products_have_unique_working_detail_pages(self):
        for category_path in (
            "/gants/",
            "/protections/",
            "/accessoires/",
            "/pack-complet/",
        ):
            listing = self.client.get(category_path)
            detail_urls = [
                product["detail_url"]
                for product in listing.context["products"]
            ]
            self.assertEqual(len(detail_urls), len(set(detail_urls)))

            for detail_url in detail_urls:
                with self.subTest(detail_url=detail_url):
                    self.assertEqual(self.client.get(detail_url).status_code, 200)

    def test_unknown_product_detail_returns_not_found(self):
        response = self.client.get("/gants/produit-introuvable/")

        self.assertEqual(response.status_code, 404)

    def test_about_page_has_clear_heading_and_contact_action(self):
        response = self.client.get("/a-propos/")

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "<h1")
        self.assertContains(response, "Notre objectif")
        self.assertContains(response, "Nous contacter sur WhatsApp")

    def test_category_filters_by_type_brand_and_search(self):
        response = self.client.get(
            "/accessoires/",
            {"type": "t-shirts", "brand": "VENUM"},
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            [product["name"] for product in response.context["products"]],
            [
                "T-shirt Venum UFC Fight - blanc et noir",
                "T-shirt Venum UFC Fight - noir et rouge",
            ],
        )

        response = self.client.get("/accessoires/", {"query": "noir"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            [product["name"] for product in response.context["products"]],
            [
                "Protège-cheville PAKKA - noir",
                "T-shirt Venum UFC Fight - blanc et noir",
                "T-shirt Venum UFC Fight - noir et rouge",
                "Short de boxe thaï Wiked - vert noir",
                "Fairtex BS1947 Muaythai Short - noir et jaune",
            ],
        )

        response = self.client.get("/protections/", {"type": "casque"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            [product["name"] for product in response.context["products"]],
            [
                "Casque de boxe ouvert - noir et rouge",
                "Casque de boxe ouvert - noir et blanc",
            ],
        )

        response = self.client.get("/accessoires/", {"color": "Vert noir"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            [product["name"] for product in response.context["products"]],
            ["Short de boxe thaï Wiked - vert noir"],
        )

        response = self.client.get("/protections/", {"color": "Jaune"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            [product["name"] for product in response.context["products"]],
            ["Protège-dents FAFA SPORT - jaune"],
        )

    def test_category_filter_reports_unavailable_choice(self):
        response = self.client.get("/accessoires/", {"type": "not-a-category"})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["products"], [])
        self.assertContains(response, "Un filtre sélectionné n’est pas disponible")

    def test_complete_pack_catalog_is_listed_on_request(self):
        response = self.client.get("/pack-complet/")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            [
                (product["name"], product["image"])
                for product in response.context["products"]
            ],
            [
                ("Pack complet 1", "pages/products/pack-complet-01.jfif"),
                ("Pack complet 2", "pages/products/pack-complet-02.jfif"),
                ("Pack complet 3", "pages/products/pack-complet-03.jfif"),
            ],
        )
        self.assertContains(response, "Pack complet 1")
        self.assertContains(response, "Pack complet 2")
        self.assertContains(response, "Pack complet 3")
        self.assertContains(response, "Prix sur demande", count=3)
        self.assertNotContains(response, "Photo bientôt disponible")

    def test_home_filters_gloves_by_brand_and_price(self):
        response = self.client.get(
            "/",
            {
                "filter": "1",
                "product_type": "gants",
                "brand": "VENUM",
                "price_min": "220",
                "price_max": "220",
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["filter_results"]), 8)
        self.assertContains(response, "8 produit(s) trouvé(s)")
        self.assertNotContains(response, "Gants de kick-boxing Fairtex")

    def test_home_filters_by_protector_and_pack_type(self):
        filters = (
            (
                "protege-dents",
                (
                    "Protège-dents Venum Predator Competition Series - orange et noir",
                    "Protège-dents Venum Predator Competition Series - bleu et noir",
                    "Protège-dents Venum Predator Competition Series - blanc et noir",
                    "Protège-dents Venum Predator Competition Series - noir et blanc",
                    "Protège-dents Venum Predator Competition Series - noir et rouge",
                    "Protège-dents FAFA SPORT - bleu",
                    "Protège-dents FAFA SPORT - jaune",
                ),
            ),
            (
                "protege-tibias",
                (
                    "Protège-tibia ZTT - noir",
                    "Protège-tibia FAFA - doré et noir",
                ),
            ),
            (
                "casque",
                (
                    "Casque de boxe ouvert - noir et rouge",
                    "Casque de boxe ouvert - noir et blanc",
                ),
            ),
            (
                "accessoires",
                (
                    "Bandages de boxe et de MMA PAKKA",
                    "Corde à sauter réglable PAKKA - fitness, boxe et CrossFit",
                    "Protège-cheville PAKKA - noir",
                    "Protège-cheville PAKKA - bleu",
                    "Protège-cheville FAFA - rouge",
                    "T-shirt Venum UFC Fight - blanc et noir",
                    "T-shirt Venum UFC Fight - noir et rouge",
                    "Short de boxe thaï Venum - gris et blanc",
                    "Short de boxe thaï Wiked - vert noir",
                    "Fairtex BS1947 Muaythai Short - noir et jaune",
                    "BSG3 Fairtex Official GLORY Short - blanc",
                ),
            ),
            ("pack-complet", ("Pack complet 1", "Pack complet 2", "Pack complet 3")),
        )
        for product_type, expected_products in filters:
            with self.subTest(product_type=product_type):
                response = self.client.get(
                    "/",
                    {"filter": "1", "product_type": product_type},
                )

                self.assertEqual(response.status_code, 200)
                self.assertEqual(
                    [product["name"] for product in response.context["filter_results"]],
                    list(expected_products),
                )

    def test_protection_catalog_lists_all_new_products(self):
        response = self.client.get("/protections/")
        expected_products = (
            "Protège-tibia ZTT - noir",
            "Protège-tibia FAFA - doré et noir",
            "Protège-dents Venum Predator Competition Series - orange et noir",
            "Protège-dents Venum Predator Competition Series - bleu et noir",
            "Protège-dents Venum Predator Competition Series - blanc et noir",
            "Protège-dents Venum Predator Competition Series - noir et blanc",
            "Protège-dents Venum Predator Competition Series - noir et rouge",
            "Protège-dents FAFA SPORT - bleu",
            "Protège-dents FAFA SPORT - jaune",
            "Casque de boxe ouvert - noir et rouge",
            "Casque de boxe ouvert - noir et blanc",
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["products"]), 11)
        for product_name in expected_products:
            with self.subTest(product=product_name):
                self.assertContains(response, product_name)
        self.assertContains(response, "Prix sur demande", count=11)
        image_paths = re.findall(
            rb'<img class="product-card__image" src="/static/pages/products/([^"]+)"',
            response.content,
        )
        expected_image_numbers = (1, 2, 5, 6, 7, 8, 9, 13, 14, 15, 16)
        self.assertEqual(
            image_paths,
            [f"{number:02}.jpg".encode() for number in expected_image_numbers],
        )
        self.assertNotContains(response, "Bandages de boxe et de MMA PAKKA")
        self.assertNotContains(response, "Protège-cheville FAFA - rouge")
        open_helmet = next(
            product
            for product in response.context["products"]
            if product["name"] == "Casque de boxe ouvert - noir et rouge"
        )
        self.assertEqual(open_helmet["filter_brand"], "VENUM")

    def test_accessories_catalog_lists_transferred_products_with_photos(self):
        response = self.client.get("/accessoires/")
        expected_products = (
            ("Bandages de boxe et de MMA PAKKA", "pages/products/03.jpg"),
            ("Corde à sauter réglable PAKKA - fitness, boxe et CrossFit", "pages/products/04.jpg"),
            ("Protège-cheville PAKKA - noir", "pages/products/10.jpg"),
            ("Protège-cheville PAKKA - bleu", "pages/products/11.jpg"),
            ("Protège-cheville FAFA - rouge", "pages/products/12.jpg"),
            (
                "T-shirt Venum UFC Fight - blanc et noir",
                "pages/products/accessoires-01.jfif",
            ),
            (
                "T-shirt Venum UFC Fight - noir et rouge",
                "pages/products/accessoires-02.jfif",
            ),
            (
                "Short de boxe thaï Venum - gris et blanc",
                "pages/products/accessoires-03.jfif",
            ),
            (
                "Short de boxe thaï Wiked - vert noir",
                "pages/products/accessoires-04.jfif",
            ),
            (
                "Fairtex BS1947 Muaythai Short - noir et jaune",
                "pages/products/accessoires-05.jfif",
            ),
            (
                "BSG3 Fairtex Official GLORY Short - blanc",
                "pages/products/accessoires-06.jfif",
            ),
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["products"]), len(expected_products))
        self.assertEqual(
            [
                (product["name"], product["image"])
                for product in response.context["products"]
            ],
            list(expected_products),
        )
        for product_name, _ in expected_products:
            with self.subTest(product=product_name):
                self.assertContains(response, product_name)
        self.assertContains(response, "Prix sur demande", count=len(expected_products))

    def test_home_filter_reports_invalid_price_range(self):
        response = self.client.get(
            "/",
            {"filter": "1", "price_min": "300", "price_max": "200"},
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Le prix maximum doit être supérieur au prix minimum.")

    def test_glove_catalog_has_twelve_products_with_ordered_photos_and_prices(self):
        response = self.client.get("/gants/")
        product_names = (
            "Gants Venum Contender 2.0",
            "Gants Venum Contender 2.0",
            "Gants Venum Stone",
            "Gants Venum Elite",
            "Gants Venum Challenger 3.0",
            "Gants Venum Impact",
            "Gants Venum roses",
            "Gants de kick-boxing Fairtex × GLORY",
            "Gants de kick-boxing Fairtex × GLORY",
            "Gants de kick-boxing Fairtex × GLORY",
            "Gants de compétition de kick-boxing Fairtex × GLORY",
            "Gants Venum Impact",
        )
        variants = (
            "Noir et blanc",
            "Blanc, gris et noir",
            "Vert minéral",
            "Noir et rouge",
            "Noir",
            "Camouflage sombre et sable",
            "Rose et blanc",
            "Noir",
            "Blanc et noir",
            "BGVG1 - Fermeture auto-agrippante",
            "Blanc et noir",
            "Noir et or",
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '<article class="product-card product-card--illustrated">', count=12)
        self.assertContains(response, '<del class="product-card__original-price">300 DH</del>', count=12)
        self.assertContains(response, '<span class="product-card__sale-price">220 DH</span>', count=12)
        self.assertNotContains(response, "Photo bientôt disponible")
        self.assertContains(response, "Prix+%3A+220+DH")
        self.assertContains(response, "Merci+de+confirmer+la+disponibilit")

        for name, variant in zip(product_names, variants):
            with self.subTest(product=name, variant=variant):
                self.assertContains(response, name)
                self.assertContains(response, variant)
        expected_images = (
            "gants-11.jpg",
            "gants-04.jpg",
            "gants-08.jpg",
            "gants-05.jpg",
            "gants-10.jpg",
            "gants-01.jpg",
            "gants-12.jpg",
            "gants-09.jpg",
            "gants-02.jpg",
            "gants-06.jpg",
            "gants-07.jpg",
            "gants-03.jpg",
        )
        image_paths = re.findall(
            rb'<img class="product-card__image" src="/static/pages/products/([^"]+)"',
            response.content,
        )
        self.assertEqual(image_paths, [image.encode() for image in expected_images])
