# Публикация проекта в GitHub

## Восстановление истории из комплекта

В архиве проекта находятся исходные файлы и отдельный Git bundle с ветками `main` и `docs/accessibility`.
Bundle сохраняет коммиты и различие веток. Для его использования нужны Git и права записи в репозиторий.
Команды выполняйте в каталоге, где лежит `style-guide-project.bundle`:

```bash
git clone style-guide-project.bundle style-guide-project
cd style-guide-project
git remote rename origin archive
git remote add origin https://github.com/Artsobol/style-guide-project.git
git switch main
git push -u origin main
git switch -c docs/accessibility archive/docs/accessibility
git push -u origin docs/accessibility
```

Если имя ветки уже существует локально, используйте `git switch docs/accessibility`.
Если на GitHub уже появилась независимая история, сначала согласуйте её с локальной без `--force`.
Не заменяйте работу других авторов принудительной отправкой.
Если ветки уже опубликованы этим запуском, повторно заливать их не требуется.

## Открытие PR

Откройте сравнение веток:
[main и docs/accessibility](https://github.com/Artsobol/style-guide-project/compare/main...docs/accessibility).
Укажите заголовок «docs: add text accessibility guidelines».
Описание возьмите из `ACCESSIBILITY_PR.md`. Откройте PR для настоящего ревью.
Если установлен и авторизован GitHub CLI, можно выполнить:

```bash
gh pr create --base main --head docs/accessibility \
  --title "docs: add text accessibility guidelines" \
  --body-file ACCESSIBILITY_PR.md
```

## Настройка Pages

1. Откройте Settings → Pages в репозитории.
2. Выберите Build and deployment → Source → GitHub Actions.
3. Разрешите запуск Actions, если политика аккаунта его ограничивает.
4. В Actions запустите `Docs CI and Pages` через Run workflow из ветки `main`.
5. Проверьте jobs `validate` и `deploy` и откройте адрес из окружения `github-pages`.

Ожидаемый адрес: [сайт проекта](https://artsobol.github.io/style-guide-project/).
Workflow PR только проверяет документы; ветка доступности публикуется после merge в `main`.
Права `pages: write` и `id-token: write` заданы только заданию публикации.

Порядок основан на [официальной документации GitHub Pages](https://docs.github.com/en/pages/getting-started-with-github-pages/using-custom-workflows-with-github-pages).

## Завершение взаимного ревью

Обменяйтесь PR с другим студентом, оставьте три содержательных комментария в его PR,
получите замечания к своему и исправьте их новым коммитом. После одобрения выполните merge.
Проверьте повторный запуск workflow и появление раздела доступности на сайте.
Сохраните ссылки для преподавателя. Фиктивные одобрения и комментарии не заменяют эти действия.
