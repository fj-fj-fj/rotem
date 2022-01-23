"""Menu as key/value pairs: name/url."""

# `menu_name_url_map` exports to app.interpretation.views.routes for `common_data()`
# `menu_name_url_map` used in app.templates.includes.menu
menu_name_url_map = [
    {
        "name": "информация о Rotem",
        "url": "about",
    },
    {
        "name": "Rotem тесты",
        "url": "tests",
    },
    {
        "name": "исторические данные",
        "url": "historical_data",
    },
    {
        "name": "видео инструкции",
        "url": "video_instructions",
    },
    {
        "name": "интерпретация результатов",
        "url": "results_interpretation",
    },
    {
        "name": "Поддержка",
        "url": "help",
    },
    {
        "name": "Полезные ссылки",
        "url": "useful_links",
    },
]
