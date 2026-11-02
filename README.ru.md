# AI templates

Установщик проектных правил для Claude, Codex и GitHub Copilot в VS Code.

Стеки: **C#**, **Unity** (подтягивает C#), **Python**, **Node.js**, **TypeScript**, **React** (подтягивает TypeScript).
Области: `backend-api`, `web-frontend`, `game`, `desktop-app`, `library-cli`.

## Использование

Нужен Python 3.9+ (только стандартная библиотека).

```bash
python setup.py                       # интерактивно
python setup.py --target ../MyGame --stacks unity --area game --extras all --forge both --yes
python setup.py --target . --stacks react,nodejs --dry-run
```

| Флаг | Значение |
|---|---|
| `--agent` | `claude,codex,copilot`, `all`, `both` (Claude + Codex), по умолчанию Claude |
| `--commit-lang` | Язык заголовка коммита (`ru` / `en`, по умолчанию `ru`) |
| `--pr-lang` | Язык заголовка и описания PR (`ru` / `en`, по умолчанию `ru`) |
| `--target` | папка проекта |
| `--stacks` | `csharp,unity,nodejs,typescript,react,python` |
| `--area` | одна область или `none` |
| `--extras` | `settings,pr,commitlint,editorconfig,gitignore` / `all` / `none` |
| `--forge` | `github`, `gitea`, `both` (папка для шаблона PR) |
| `--dry-run` | только показать изменения |
| `--yes` | без вопросов |
| `--force` | перезаписать уже существующие дополнительные файлы |

## Что записывается

- `CLAUDE.md` (Claude), `AGENTS.md` (Codex), `.github/copilot-instructions.md` (Copilot), `REVIEW.md`: правила помещаются между маркерами `claude-templates:begin/end`. Повторный запуск обновляет только этот блок, ваш текст сохраняется.
- `settings` (Claude): `.claude/settings.json` вливается в существующий (без соавторства и подписи Claude, запрет force-push и `reset --hard`).
- `pr`: `pull_request_template.md` в `.github/` и/или `.gitea/`.
- `commitlint`: для Node-стеков ставятся commitlint + husky, для остальных — обычные `.githooks/` (формат коммита, только заголовок, без соавторства, имя ветки).
- `editorconfig`, `gitignore`: под выбранные стеки (`gitignore` — блок между маркерами).

Скрипт не запускает `npm` и `git`, а выводит команды для ручного запуска.

## macOS Terminal

Из каталога этого репозитория запустите мастер или попробуйте установку в отдельный проект. Требуется Python 3.9+.

```bash
python3 setup.py
mkdir -p "../Demo Python"
python3 setup.py --target "../Demo Python" --stacks python --agent all --commit-lang ru --pr-lang en --extras all --yes --dry-run
python3 setup.py --target "../Demo Python" --stacks python --agent all --commit-lang ru --pr-lang en --extras all --yes
```

Однофайловый установщик можно собрать и запустить так. Для скачанного из релиза файла используйте ту же команду с путём к нему.

```bash
python3 build.py
python3 dist/claude-templates.py
```

Codex читает проектные инструкции от корня репозитория до рабочего каталога. В каждой папке непустой `AGENTS.override.md` имеет приоритет над `AGENTS.md`; более локальные правила имеют приоритет при конфликте. Общий бюджет проектных инструкций по умолчанию — 32 КиБ. [Codex](https://learn.chatgpt.com/docs/agent-configuration/agents-md)

CI проверяет PR на macOS, Linux и Windows. После слияния workflow на основную ветку в Actions → CI → Run workflow можно выбрать только `macos-latest`.

## Как добавить стек

Создайте `templates/stacks/<имя>/CLAUDE.md` и `REVIEW.md`, добавьте имя в `STACKS` (и в `IMPLIES`, если нужно) в `setup.py`. Один фрагмент держите в пределах ~60 строк.

## Тесты

```bash
python -m unittest discover tests
```

## Скачивание (клонировать не нужно)

Возьмите `claude-templates.py` из [последнего релиза](../../releases/latest) и запустите `python claude-templates.py`. Это один файл со всеми встроенными шаблонами. Собрать его самому: `python build.py` (результат: `dist/claude-templates.py`); пуш тега `v*` публикует релиз автоматически.
