find _build/html/notebooks -name "*.html" | xargs -I {} python addPlaceholder.py {}
