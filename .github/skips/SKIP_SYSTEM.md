# Skip System Documentation

The skip system allows you to temporarily disable specific GitHub Actions workflows.

## How it works

Create a skip file in `.github/skips/` to disable a workflow:

- `.skip.all` - Disables ALL workflows
- `.skip.update-readme` - Disables only the update-readme workflow

## Skip file content

Each skip file must contain the exact text:

- `.skip.all` → `SKIP_ALL`
- `.skip.update-readme` → `SKIP_README`

## Example

To skip the readme update workflow:

```bash
echo "SKIP_README" > .github/skips/.skip.update-readme
git add .github/skips/.skip.update-readme
git commit -m "ci: skip readme updates"
git push
```

To re-enable:

```bash
rm .github/skips/.skip.update-readme
git add .github/skips/.skip.update-readme
git commit -m "ci: re-enable readme updates"
git push
```

## Security

The skip system validates file content to prevent accidental or malicious workflow disabling.
