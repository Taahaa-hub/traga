(() => {
    const imageViewer = document.querySelector(".image-viewer");

    if (imageViewer) {
        const viewerImage = imageViewer.querySelector(".image-viewer__image");
        const viewerCaption = imageViewer.querySelector(".image-viewer__caption");
        const closeButton = imageViewer.querySelector(".image-viewer__close");

        document.addEventListener("click", (event) => {
            const trigger = event.target.closest("[data-image-viewer]");
            if (!trigger) {
                return;
            }

            const image = trigger.querySelector("img");
            if (!image) {
                return;
            }

            if (typeof imageViewer.showModal !== "function") {
                window.open(image.currentSrc || image.src, "_blank", "noopener,noreferrer");
                return;
            }

            event.preventDefault();
            const caption = trigger.dataset.imageCaption || image.alt;
            viewerImage.src = image.currentSrc || image.src;
            viewerImage.alt = caption;
            viewerCaption.textContent = caption;
            imageViewer.showModal();
        });

        closeButton.addEventListener("click", () => imageViewer.close());
        imageViewer.addEventListener("click", (event) => {
            if (event.target === imageViewer) {
                imageViewer.close();
            }
        });
        imageViewer.addEventListener("close", () => {
            viewerImage.removeAttribute("src");
            viewerImage.alt = "";
            viewerCaption.textContent = "";
        });
    }

    const prefersReducedMotion = window.matchMedia(
        "(prefers-reduced-motion: reduce)",
    ).matches;

    if (prefersReducedMotion || !("IntersectionObserver" in window)) {
        return;
    }

    const initializeScrollReveal = () => {
        const elements = document.querySelectorAll(
            [
            ".hero__content",
            ".hero__visual",
            ".product-finder",
            ".section-heading",
            ".category-card",
            ".product-card",
            ".assurance-card",
            ".closing-banner",
            ".order-steps__card",
            ".category-page__intro",
            ".category-filter-form",
            ".product-showcase",
            ".product-detail__layout",
            ".product-detail__related",
            ".about-page__intro",
            ".about-page__content",
            ".about-page__contact",
            ].join(", "),
        );

        if (!elements.length) {
            return;
        }

        document.documentElement.classList.add("has-scroll-reveal");

        const observer = new IntersectionObserver(
            (entries, currentObserver) => {
                entries.forEach((entry) => {
                    if (!entry.isIntersecting) {
                        return;
                    }

                    entry.target.classList.add("is-visible");
                    currentObserver.unobserve(entry.target);
                });
            },
            { threshold: 0.12, rootMargin: "0px 0px -40px 0px" },
        );

        const showContentWhenHidden = () => {
            if (!document.hidden) {
                return;
            }

            document.documentElement.classList.remove("has-scroll-reveal");
            observer.disconnect();
            document.removeEventListener(
                "visibilitychange",
                showContentWhenHidden,
            );
        };
        document.addEventListener("visibilitychange", showContentWhenHidden);

        elements.forEach((element) => {
            element.setAttribute("data-reveal", "");

            if (
                element.matches(".category-card, .product-card, .assurance-card")
            ) {
                const siblings = Array.from(
                    element.parentElement.children,
                ).filter((sibling) =>
                    sibling.matches(
                        ".category-card, .product-card, .assurance-card",
                    ),
                );
                const index = siblings.indexOf(element);
                element.style.setProperty(
                    "--reveal-delay",
                    `${Math.min(index, 4) * 80}ms`,
                );
            }

            observer.observe(element);
        });
    };

    if (document.hidden) {
        const initializeWhenVisible = () => {
            if (document.hidden) {
                return;
            }

            document.removeEventListener(
                "visibilitychange",
                initializeWhenVisible,
            );
            initializeScrollReveal();
        };
        document.addEventListener("visibilitychange", initializeWhenVisible);
        return;
    }

    initializeScrollReveal();
})();
