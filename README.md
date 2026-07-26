# Second-Hand Price Intelligence

Scrapes eBay's sold/completed listings, scores each listing's condition from its
title using a keyword heuristic, and estimates a fair price range by comparing
a listing against past sales in the same condition grade. There's a small
Streamlit demo on top so you can try it without running a scrape.

**Status: v0.1.** The scraper, scoring, and demo work end-to-end. The parts
below marked "not built yet" are real gaps, not modesty.

## What actually works right now

- **Scraper** (`scraper/`) — `requests` + BeautifulSoup against eBay's sold
  listings search. `fetch.py` warms up a session against the eBay homepage
  first to pick up cookies, then paginates with randomized 5–10s delays and
  stops early after two consecutive empty pages. `parser.py` pulls title,
  price, and URL out of each listing card and filters out sponsored/dummy
  cards. `save.py` writes the results to a timestamped CSV in `data/`.
- **CI Score** (`scoring/ci_score.py`) — every listing starts at 50 and moves
  up or down based on ~20 hardcoded keywords in the title ("sealed" +25,
  "for parts" −30, etc.), clamped to 0–100 and bucketed into grades A–D.
- **Streamlit demo** (`frontend/app.py`) — type in a listing title, get a CI
  score and grade, and a price range (25th/50th/75th percentile) pulled from
  past listings with the same grade. Falls back to the bundled sample CSV if
  you haven't scraped anything yet.
- **Sample data** (`sample_data/sample_listings.csv`) — ~600 real scraped
  Sony WH-1000XM4 listings, included so the demo has something to show out
  of the box.

## About the "NLP-powered" part

The repo description and topics say NLP/ML. As of v0.1, the scoring is a
plain keyword-matching dictionary — no trained model, no embeddings, no
image analysis. `scoring/ci_score.py` says as much in its own header
comment. It's a reasonable baseline (it's readable, debuggable, and gives
sensible grades on the sample data), but it isn't NLP yet. That's the
actual next milestone, not a finished feature.

## What's scaffolded but not built

These folders exist with an empty placeholder `README.md` and nothing else:

- `backend/` — no API yet. `starlette`/`uvicorn`/`python-multipart` are in
  `requirements.txt` ahead of this being built.
- `docker/` — no containerization yet.
- `models/` — no trained models yet (this is where a future ML scorer's
  weights would live).
- `notebooks/` — no EDA or experiments committed yet.

Also worth knowing:
- `test_scoring.py` is not a test suite despite the name — it's a one-off
  script that prints the grade distribution over a scraped CSV. There's no
  `pytest`/assertion-based testing in this repo yet.
- `playwright` is in `requirements.txt` but unused — the scraper is plain
  `requests`, not a headless browser.
- The parser depends on eBay's current CSS class names
  (`s-card__title`, `s-card__price`, `su-card-container__content`, etc.).
  If eBay changes their markup, `parser.py` will start returning zero
  results until those selectors are updated.

## Running it

```bash
pip install -r requirements.txt

# Scrape (edit SEARCH_QUERY at the top of main.py to change the product)
python main.py

# Demo — works even without scraping, using the bundled sample data
streamlit run frontend/app.py
```

Run it through `main.py`, not the individual scraper modules directly — the
`if __name__ == "__main__"` blocks in `scraper/fetch.py`, `parser.py`, and
`save.py` predate the session-based refactor and call
`fetch_ebay_sold_listings` with the wrong number of arguments, so they'll
throw a `TypeError` if run standalone.

## Roadmap

- v0.2 — replace keyword scoring with a real NLP model trained on labeled
  condition data
- v0.3 — FastAPI backend to serve scores and price estimates
- v0.4 — Docker packaging
- v1.0 — image-based condition analysis
