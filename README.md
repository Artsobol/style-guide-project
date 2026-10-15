# Стайлгайд REST API на Java и Spring Boot

Лабораторная работа № 3: полный учебный проект Docs as Code.
Руководство охватывает язык, структуру, Markdown, описание REST API и сопровождение документации.
Ответы по пунктам 1–5 находятся в `docs/lab/`, два примерных документа — в `docs/examples/`.
Репозиторий содержит учебный контракт Task API, но не запускаемый сервер.

## Быстрый запуск

Требуются Python 3.12, Node.js 22+ и npm. Команды выполняйте из корня проекта.

```bash
python -m venv .venv
```

Активируйте окружение в Bash: `source .venv/bin/activate`.
В Windows PowerShell: `.venv\Scripts\Activate.ps1`.

```bash
python -m pip install -r requirements.txt
npm ci
npm run lint:md
python scripts/check_examples.py
mkdocs build --strict
mkdocs serve
```

Откройте [локальный сайт](http://127.0.0.1:8000/).
Закреплены версии MkDocs, темы и линтера; `package-lock.json` фиксирует дерево Node-зависимостей.

## Структура

```text
docs/
  guide/           правила стиля
  examples/        инструкция и справочник операции
  lab/             ответы, оценка, порядок сдачи
  assets/          OpenAPI и JSON-примеры
scripts/           проверка учебного контракта
.github/workflows/ проверки и публикация
```

## CI/CD и Pages

Workflow `Docs CI and Pages` запускает линтер, проверку примеров и строгую сборку на push и PR.
Только push в `main` или ручной запуск из `main` публикует проверенный сайт через GitHub Pages.
В Settings → Pages выберите Source → GitHub Actions до первой публикации.
Если публикация не запустилась автоматически после настройки Pages, запустите workflow вручную из `main`.
Планируемый адрес: [сайт проекта](https://artsobol.github.io/style-guide-project/).
Наличие этой ссылки не означает, что сайт уже опубликован: смотрите `STATUS.md` и GitHub Actions.

## Ветка доступности

Раздел доступности добавляется веткой `docs/accessibility` поверх основной работы.
Изменение включает страницу и пункт навигации. Оно готово к настоящему ревью другого студента.
Слияние выполняется после замечаний, исправлений и одобрения.

См. [правила участия](CONTRIBUTING.md), [статус](STATUS.md),
[инструкции публикации](UPLOAD.md) и [журнал изменений](CHANGELOG.md).
