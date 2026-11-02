## Python development

- Check `pyproject.toml`, lockfiles and CI for supported Python versions, package manager and test commands before changing dependencies.
- Use the project's configured test runner. For a standard-library unittest suite under `tests/`, run `python -m unittest discover tests` with the project interpreter.
- Run the formatter, linter and type checker already configured by the project. Keep runtime and development dependencies separate.
