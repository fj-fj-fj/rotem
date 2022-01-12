from werkzeug.datastructures import ImmutableMultiDict

from app import app
from tests.conftest import captured_templates


client = app.test_client()


def test_index_view():
    with captured_templates(app) as templates:
        r = client.get('/')
        assert r.status_code == 200
        assert len(templates) == 1
        template, context = templates[0]
        assert template.name == 'index.html'
        assert context['g'].title == 'Новости'
        assert isinstance(context['articles'], list)
        assert len(context['articles']) == 20


def test_about_view():
    with captured_templates(app) as templates:
        r = client.get('/about')
        assert r.status_code == 200
        assert len(templates) == 1
        template, context = templates[0]
        assert template.name == 'menu/about.html'
        assert context['g'].title == 'Информация о rotem'
        assert '<h1>Тромбоэластометр ROTEM delta</h1>' in r.data.decode('utf-8')


def test_tests_view():
    with captured_templates(app) as templates:
        r = client.get('/tests')
        assert r.status_code == 200
        assert len(templates) == 1
        template, context = templates[0]
        assert template.name == 'menu/tests.html'
        assert context['g'].title == 'Тесты rotem'
        assert '<h1>Тесты ROTEM® delta</h1>' in r.data.decode('utf-8')


def test_historical_data_view():
    with captured_templates(app) as templates:
        r = client.get('/historical-data')
        assert r.status_code == 200
        assert len(templates) == 1
        template, context = templates[0]
        assert template.name == 'menu/historical_data.html'
        assert context['g'].title == 'Историческая справка'
        assert '<h1>РОТАЦИОННАЯ ТРОМБОЭЛАСТОМЕТРИЯ (ROTEM)</h1>' in r.data.decode('utf-8')


def test_video_instructions_view():
    with captured_templates(app) as templates:
        r = client.get('/video-instructions')
        assert r.status_code == 200
        assert len(templates) == 1
        template, context = templates[0]
        assert template.name == 'menu/video_instructions.html'
        assert context['g'].title == 'Видео инструкции'


def test_results_interpretation_view_get():
    with captured_templates(app) as templates:
        r = client.get('/interpretation-of-results')
        assert r.status_code == 200
        assert len(templates) == 1
        template, context = templates[0]
        assert template.name == 'menu/results_interpretation.html'
        assert context['g'].title == 'Интерпретация результатов'
        assert '<h1>Интерпретация результатов</h1>' in r.data.decode('utf-8')


def test_results_interpretation_view_post_and_flash_message_error():
    with captured_templates(app) as templates:
        r = client.post('/interpretation-of-results', data=ImmutableMultiDict([('data_extem_ct', 1)]))
        assert r.status_code == 200
        assert len(templates) == 1
        template, context = templates[0]
        assert template.name == 'menu/results_interpretation.html'
        assert context['g'].title == 'Интерпретация результатов'
        assert '<div class="flash error">' in r.data.decode('utf-8')


def test_results_interpretation_view_post_and_flash_message_success():
    with captured_templates(app) as templates:
        r = client.post(
            '/interpretation-of-results',
            data=ImmutableMultiDict([
                ('data_extem_ct', 40),
                ('data_extem_a5', 37),
                ('data_intem_ct', 100),
                ('data_fibtem_a5', 8),
            ]),
        )
        assert r.status_code == 200
        assert len(templates) == 1
        template, context = templates[0]
        assert template.name == 'menu/results_interpretation.html'
        assert context['g'].title == 'Интерпретация результатов'
        assert '<div class="flash success">' in r.data.decode('utf-8')


def test_help_view():
    with captured_templates(app) as templates:
        r = client.get('/help')
        assert r.status_code == 200
        assert len(templates) == 1
        template, context = templates[0]
        assert template.name == 'menu/help.html'
        assert context['g'].title == 'Поддержка'


def test_historical_data_view():
    with captured_templates(app) as templates:
        r = client.get('/useful-links')
        assert r.status_code == 200
        assert len(templates) == 1
        template, context = templates[0]
        assert template.name == 'menu/useful_links.html'
        assert context['g'].title == 'Полезные ссылки'
