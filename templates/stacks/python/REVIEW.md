## Python review

- Check syntax and dependency changes against the minimum supported Python version.
- Verify imports and packaging from the installed entry point. Check that tests exercise the changed behavior using the project's test runner.
- For filesystem and CLI changes, check encoding, platform-specific paths, exit codes and temporary file cleanup.
