"""Fetch recent AI papers from OpenAlex and save them as timestamped JSON."""

from __future__ import annotations

import json
import os
from datetime import date, datetime, timedelta, timezone
from pathlib import Path

from pyalex import Concepts, Works, config

CONCEPT_QUERY = "artificial intelligence"
LOOKBACK_DAYS = 3
TEMP_DIR = Path(__file__).resolve().parent / "temp"


def _short_openalex_id(entity_id: str) -> str:
    return entity_id.rstrip("/").rsplit("/", 1)[-1]


def find_concept(query: str) -> dict:
    matches = Concepts().search(query).get(per_page=25)
    if not matches:
        raise SystemExit(f"No OpenAlex concepts found for {query!r}.")

    query_lower = query.casefold()
    for concept in matches:
        if (concept.get("display_name") or "").casefold() == query_lower:
            return dict(concept)
    return dict(matches[0])


def fetch_recent_works(concept_id: str, since: date) -> list[dict]:
    query = Works().filter(
        concepts={"id": concept_id},
        from_publication_date=since.isoformat(),
    )
    count = query.count()
    print(f"Found {count} works tagged with {concept_id} since {since.isoformat()}.")

    papers: list[dict] = []
    for page in query.paginate(per_page=200, n_max=None):
        papers.extend(dict(work) for work in page)
        print(f"  downloaded {len(papers)} / {count}")
    return papers


def main() -> None:
    email = os.environ.get("OPENALEX_EMAIL")
    if email:
        config.email = email

    print(f"Searching OpenAlex concepts for {CONCEPT_QUERY!r}...")
    concept = find_concept(CONCEPT_QUERY)
    concept_id = _short_openalex_id(concept["id"])
    print(f"Using concept {concept.get('display_name')} ({concept_id})")

    since = date.today() - timedelta(days=LOOKBACK_DAYS)
    papers = fetch_recent_works(concept_id, since)

    TEMP_DIR.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
    out_path = TEMP_DIR / f"ai_papers_{stamp}.json"
    out_path.write_text(json.dumps(papers, indent=2, default=str), encoding="utf-8")
    print(f"Saved {len(papers)} papers to {out_path}")


if __name__ == "__main__":
    main()
