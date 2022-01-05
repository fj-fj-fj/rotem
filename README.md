# Rotem

> Сайт про технологию Rotem и агрегатор новостей о медицине.

#
### Главная страница
 - новости
### Меню 
 - информация о rotem
 - rotem тесты
 - исторические данные
 - видео инструкции
 - интерпретация результатов
 - поддержка
 - полезные ссылки

#

## Установка
```sh
mkdir -p rotem && cd rotem && git clone https://github.com/fj-fj-fj/rotem.git src

# Управляйте версиями Python с помощью pyenv:
curl -L https://pyenv.run | bash
echo 'export PATH="~/.pyenv/bin:$PATH"' >> ~/.bashrc
echo 'eval "$(pyenv init -)"' >> ~/.bashrc
source ~/.bashrc

# Управляйте зависимостями с помощью Poetry:
curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python - --version 1.1.11
source $HOME/.poetry/env
poetry install
# Если с Poetry что-то пошло не так:
python3 -m venv .venv
.venv/bin/pip install -r src/requirements.txt

# Управляйте переменными окружения с помощью direnv:
pip install -U pip && pip install -r src/requirements.txt
sudo apt-get update && sudo apt-get install direnv
echo 'eval "$(direnv hook bash)"' >> ~/.bashrc
source ~/.bashrc
mv .envrc.sample .envrc
direnv allow .
# Если с direnv что-то пошло не так, установите переменные вручную из .envrc.sample
```

## Использование
```sh
make run
# Откройте в браузере http://127.0.0.1:5000
```
## :)
