# SauceDemo Playwright + Pytest Automation Framework

A maintainable UI automation framework for [SauceDemo](https://www.saucedemo.com) using Python, Playwright, Pytest, the Page Object Model, JSON test data, failure screenshots and traces, pytest-html reporting, and GitHub Actions CI across Chromium, Firefox and WebKit.

## Structure

```text
config/
  urls.json             # base_url
  credentials.json      # users, incl. negative-login cases
  test_data.json        # checkout customer, products used in tests
pages/
  base_page.py          # BasePage, AppPage (post-login), Header component
  login_page.py
  inventory_page.py
  cart_page.py
  checkout_page.py      # info, overview and complete steps
utils/
  data_loader.py        # cached JSON loading, env-var credential overrides
  screenshot_helper.py
tests/
  conftest.py           # data and page-object fixtures
  test_login.py
  test_inventory.py
  test_cart.py
  test_checkout.py
.github/workflows/
  playwright-tests.yml
conftest.py             # framework hooks: paths, base_url, test-id attribute, screenshots
pytest.ini
requirements.txt
```

## Conventions

- **Page objects expose locators and actions, never assertions.** Tests assert with Playwright's `expect(...)`, which retries automatically. Plain `assert` is only used for computed values (e.g. order totals).
- **Locators use `data-test` attributes** through `page.get_by_test_id(...)`; the root `conftest.py` sets `data-test` as the test-id attribute.
- **URLs are relative.** Each page object declares a `PATH`, `open()` navigates to it, and `url_pattern` is used with `expect(page).to_have_url(...)`. The host comes from `base_url`.
- **Fixtures** in `tests/conftest.py` provide test data (`credentials`, `customer`, `products`) and page objects. `login_page` is already opened; `inventory_page` is already logged in as the valid user.
- **Markers:** every test is `regression`; critical paths are also `smoke`. Markers are strict: use only those declared in `pytest.ini`.

## Setup

Requires **Python 3.13** (the version CI uses). Dependencies are pinned in `requirements.txt`.

```bash
python -m venv .venv

# Windows
.venv\Scripts\activate
# macOS / Linux
source .venv/bin/activate

pip install -r requirements.txt
playwright install chromium          # add firefox / webkit as needed
```

## Run

```bash
pytest                                # full suite, Chromium, headless
pytest -m smoke                       # critical paths only
pytest -n auto                        # in parallel (pytest-xdist)
pytest --headed --slowmo 500          # watch the browser
pytest --browser firefox              # another browser
pytest --browser chromium --browser webkit
```

### Configuration

| Setting | Default | Override |
|---|---|---|
| Application URL | `base_url` in `config/urls.json` | `pytest --base-url https://...` |
| Credentials | `config/credentials.json` | `SAUCEDEMO_<USER_KEY>_USERNAME` / `SAUCEDEMO_<USER_KEY>_PASSWORD`, e.g. `SAUCEDEMO_VALID_USER_PASSWORD` |

## Output

All paths are anchored to the project root, regardless of where pytest is launched from:

| Output | Location |
|---|---|
| HTML report (self-contained, failure screenshots embedded) | `reports/report.html` |
| Failure screenshots | `screenshots/` |
| Playwright traces (and videos with `--video=retain-on-failure`) for failed tests | `test-results/` |

Open a trace with `playwright show-trace test-results/<test>/trace.zip`.

## Important QA behavior

The negative-login tests verify that invalid credentials are rejected. They PASS when the expected login error is displayed: an invalid login is application behavior, not an automated-test failure.

The framework captures a full-page screenshot when an actual test assertion fails and embeds it in the HTML report.

## CI/CD

GitHub Actions (`.github/workflows/playwright-tests.yml`) runs the full suite in parallel on Chromium, Firefox and WebKit as separate matrix jobs, with pip caching, a 20-minute timeout, and cancellation of superseded runs. Each job uploads its HTML report; failed jobs also upload screenshots, traces and videos.
