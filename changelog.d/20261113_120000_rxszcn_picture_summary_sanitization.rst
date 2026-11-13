Fixed
-----

*   Preserve the ``<summary>`` element instead of stripping its tags
    while keeping its text, so the disclosure semantics of
    ``<details><summary>`` markup survive HTML sanitization.
*   Preserve the ``<picture>`` element and the responsive-image
    ``srcset`` and ``sizes`` attributes, so ``<picture><source>``
    markup keeps its structure and responsive image selection.
