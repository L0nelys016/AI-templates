# AI templates

Установщик проектных правил для Claude, Codex и GitHub Copilot в VS Code.

## Скачать установщик

Требуется Python 3.9 или новее.

| Система | Русский | English | Как запустить |
|---|---|---|---|
| macOS | [macOS-ru.zip](https://github.com/L0nelys016/AI-templates/releases/latest/download/macOS-ru.zip) | [macOS-en.zip](https://github.com/L0nelys016/AI-templates/releases/latest/download/macOS-en.zip) | Распакуйте архив и дважды щёлкните `Install.command` в Finder. |
| Windows | [Windows-ru.zip](https://github.com/L0nelys016/AI-templates/releases/latest/download/Windows-ru.zip) | [Windows-en.zip](https://github.com/L0nelys016/AI-templates/releases/latest/download/Windows-en.zip) | Распакуйте архив и дважды щёлкните `Install.cmd`. |
| Linux | [Linux-ru.tar.gz](https://github.com/L0nelys016/AI-templates/releases/latest/download/Linux-ru.tar.gz) | [Linux-en.tar.gz](https://github.com/L0nelys016/AI-templates/releases/latest/download/Linux-en.tar.gz) | Распакуйте архив и запустите `./Install.sh` из распакованной папки. |

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

- В `CLAUDE.md` (Claude), `AGENTS.md` (Codex), `.github/copilot-instructions.md` (Copilot) и `REVIEW.md` правила находятся между маркерами `claude-templates:begin/end`. Каждый запуск обновляет общий чек-лист и все ранее установленные профили, сохраняя текст вне маркеров. Выбор агентов определяет, какие новые профили установить.
- `settings` (Claude): `.claude/settings.json` вливается в существующий (без соавторства и подписи Claude, запрет force-push и `reset --hard`).
- `pr`: `pull_request_template.md` в `.github/` и/или `.gitea/`.
- `commitlint`: для Node-стеков ставятся commitlint + husky, для остальных — обычные `.githooks/` (формат коммита, только заголовок, без соавторства, имя ветки).
- `editorconfig`, `gitignore`: под выбранные стеки (`gitignore` — блок между маркерами).

Скрипт не запускает `npm` и `git`, а выводит команды для ручного запуска.

## Запуск на Mac без команд

В Finder откройте `Install.command` двойным щелчком в папке шаблонов. Для установки из релиза скачайте и распакуйте `macOS-ru.zip`, затем откройте `Install.command` из распакованной папки. Выберите папку своего проекта в диалоге. Мастер объяснит варианты, покажет список файлов и попросит подтвердить запись. Потребуется Python 3.9 или новее.

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
python3 dist/claude-templates-ru.py
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

Распакуйте архив для своей системы. На macOS откройте `Install.command` из `macOS-ru.zip`. На Windows откройте `Install.cmd` из `Windows-ru.zip`. На Linux распакуйте `Linux-ru.tar.gz` и запустите `./Install.sh` из его каталога. В каждый архив включён установщик. Требуется Python 3.9 или новее.

Возьмите `claude-templates-ru.py` из [последнего релиза](../../releases/latest) и запустите `python claude-templates-ru.py`. Это один файл со всеми встроенными шаблонами. Собрать его самому: `python build.py` (результат: `dist/claude-templates-ru.py`); пуш тега `v*` публикует релиз автоматически.
