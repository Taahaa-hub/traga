from django import forms


class ProductFilterForm(forms.Form):
    PRODUCT_TYPE_CHOICES = (
        ("", "Tous les types"),
        ("gants", "Gants de boxe"),
        ("protege-dents", "Protège-dents"),
        ("protege-tibias", "Protège-tibias"),
        ("casque", "Casque de boxe"),
        ("accessoires", "Accessoires"),
        ("pack-complet", "Pack complet"),
    )
    BRAND_CHOICES = (
        ("", "Toutes les marques"),
        ("VENUM", "Venum"),
        ("FAIRTEX", "Fairtex"),
        ("FAIRTEX × GLORY", "Fairtex × GLORY"),
        ("WIKED", "Wiked"),
        ("FAFA SPORT", "FAFA SPORT"),
        ("PAKKA", "PAKKA"),
        ("ZTT", "ZTT"),
        ("other", "Sans marque"),
    )

    product_type = forms.ChoiceField(
        choices=PRODUCT_TYPE_CHOICES,
        required=False,
        label="Type de produit",
        widget=forms.Select(attrs={"class": "product-filter__control"}),
    )
    brand = forms.ChoiceField(
        choices=BRAND_CHOICES,
        required=False,
        label="Marque",
        widget=forms.Select(attrs={"class": "product-filter__control"}),
    )
    price_min = forms.IntegerField(
        required=False,
        min_value=0,
        label="Prix minimum (DH)",
        widget=forms.NumberInput(
            attrs={
                "class": "product-filter__control",
                "placeholder": "Ex. 100",
                "min": "0",
            }
        ),
    )
    price_max = forms.IntegerField(
        required=False,
        min_value=0,
        label="Prix maximum (DH)",
        widget=forms.NumberInput(
            attrs={
                "class": "product-filter__control",
                "placeholder": "Ex. 500",
                "min": "0",
            }
        ),
    )

    def clean(self):
        cleaned_data = super().clean()
        price_min = cleaned_data.get("price_min")
        price_max = cleaned_data.get("price_max")
        if price_min is not None and price_max is not None and price_min > price_max:
            self.add_error("price_max", "Le prix maximum doit être supérieur au prix minimum.")
        return cleaned_data


class CategoryFilterForm(forms.Form):
    def __init__(self, *args, type_choices=(), brand_choices=(), color_choices=(), **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["type"] = forms.ChoiceField(
            choices=(("", "Tous les types"), *type_choices),
            required=False,
            label="Type",
            widget=forms.Select(attrs={"class": "product-filter__control"}),
        )
        self.fields["brand"] = forms.ChoiceField(
            choices=(("", "Toutes les marques"), *brand_choices),
            required=False,
            label="Marque",
            widget=forms.Select(attrs={"class": "product-filter__control"}),
        )
        self.fields["color"] = forms.ChoiceField(
            choices=(("", "Toutes les couleurs"), *color_choices),
            required=False,
            label="Couleur",
            widget=forms.Select(attrs={"class": "product-filter__control"}),
        )
        self.fields["query"] = forms.CharField(
            required=False,
            label="Recherche",
            widget=forms.TextInput(
                attrs={
                    "class": "product-filter__control",
                    "placeholder": "Nom, modèle ou couleur",
                }
            ),
        )
