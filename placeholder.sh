find _build/html/notebooks -name "*.html" | xargs -I {} python addPlaceholder.py {}
find _build/html/notebooks -name "*.html" | xargs -I {} sed -i  "/vnd.jupyter.widget-state+json/,$ d" {}
