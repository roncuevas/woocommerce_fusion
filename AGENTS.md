# Repository Guidelines

## Project Structure & Module Organization

This repository is an ERPNext/Frappe app for synchronizing ERPNext with one or more WooCommerce sites. Core Python code is under `woocommerce_fusion/`: synchronization jobs live in `tasks/`, the WooCommerce API client in `woocommerce/`, setup and patches in `setup/` and `patches/`, and browser assets in `public/`. Unit and integration tests are colocated with the implementation, primarily in `woocommerce_fusion/tasks/` and `woocommerce_fusion/woocommerce/`. Cypress UI tests are in `cypress/`. User and developer documentation is in `docs/`, with images in `docs/images/`.

## Architecture & Integration Notes

Preserve support for ERPNext v15 and v16 and for multiple WooCommerce servers. Batch API mode is opt-in per **WooCommerce Server** and queues operations visible at `/app/woocommerce-sync-status`; changes to synchronization must preserve queued, flushed, and failed operation handling. Use the existing WooCommerce client and task boundaries rather than embedding remote API calls in unrelated ERPNext code.

## Build, Test, and Development Commands

Run commands from the app directory inside a Frappe bench unless noted:

- `bench --site test_site_woocommerce run-tests --app woocommerce_fusion --coverage` runs Python tests and coverage.
- `bench --site test_site_woocommerce run-ui-tests woocommerce_fusion --headless --browser chromium` runs Cypress UI tests through Frappe.
- `pre-commit run --all-files` runs repository formatting and lint checks.
- `yarn docs:dev` previews VitePress documentation; `yarn build` builds docs and prepares help files.

Integration tests require the local WordPress Playground and Caddy setup described in `README.md`. Start them with `npx @wp-playground/cli server --blueprint wp_woo_blueprint.json --site-url=https://woo-test.localhost` and `caddy run --config wp_woo_caddy --adapter caddyfile`; map `woo-test.localhost` to `127.0.0.1` in hosts. Use only test credentials and the documented `WOO_INTEGRATION_TESTS_WEBSERVER`, `WOO_API_CONSUMER_KEY`, `WOO_API_CONSUMER_SECRET`, and `DEV_SERVER` variables.

## Coding Style & Naming Conventions

Use tabs for Python indentation and double quotes, following `pyproject.toml` and Ruff. Keep Python modules and functions `snake_case`, classes `PascalCase`, and JavaScript variables/functions `camelCase`. Run pre-commit before submitting changes; it applies Ruff, Prettier, ESLint, and basic repository checks. Keep synchronization behavior platform-consistent and isolate WooCommerce-specific API work in the WooCommerce client or task modules.

## Testing Guidelines

Add focused tests beside the affected Python module, using the existing `test_*.py` naming pattern. Add Cypress scenarios under `cypress/integration/` for UI behavior. Cover both success and failure paths for sync, mapping, queue, and API changes; use the real integration setup only when the change needs external WooCommerce behavior.

## Commit & Pull Request Guidelines

Make multiple atomic commits when a change contains independent concerns; each commit must be focused, self-contained, and easy to review or revert. Use lowercase Conventional Commits such as `feat:`, `fix:`, `test:`, `docs:`, `chore:`, or `refactor:` with a concise imperative subject. Pull requests should explain the user-visible or synchronization impact, include tests and validation commands, link related issues, and include screenshots for UI or documentation changes. Keep unrelated changes out of the PR and ensure CI, linters, and semantic-commit checks pass.

## Security & Configuration

Never commit WooCommerce keys, secrets, site credentials, or generated coverage/build output. Use environment variables for integration credentials and review patches and sync changes for unintended writes before running them against a non-test ERPNext site.

## CI & Documentation Checks

Before opening a pull request, run the relevant tests and `pre-commit`. CI also runs Frappe Semgrep rules and `pip-audit`; install or run those checks when changing Python or integration code. Documentation changes should be previewed with `yarn docs:dev` and verified with `yarn build`.
