"""
File: bobs_librarian.py
Author: Dan Weidenaar
Title: Bob's Burgers Archive CLI
Menu:
  1) List Episodes
        (paged, 10 per page)
  2) Episode Details
        (by Season + Episode #)
  3) Episode Gags
        (Store Next Door + Burger of the Day + Pest Control Truck) (by Season + Episode #)
  4) Quit
"""

import sys
from typing import Any
import requests

BASE_URL = "https://bobsburgers-api.herokuapp.com"
PAGE_SIZE = 10


# ----------------------------
# HTTP helper
# ----------------------------
def api_get(path: str, params: dict[str, Any] | None = None) -> Any | None:
    """Sends GET to BASE_URL + path; returns parsed JSON on success, None on failure."""
    url = f"{BASE_URL.rstrip('/')}/{path.lstrip('/')}"
    try:
        r = requests.get(url, params=params, timeout=15)
        r.raise_for_status()
        return r.json()
    except requests.RequestException as e:
        print(f"[API error] {e}")
        return None


# -------------------------------------------------------------------------
# Input tools
# -------------------------------------------------------------------------
def prompt_int(prompt: str, min_value: int = 1) -> int | None:
    s = input(prompt).strip()
    if not s.isdigit():
        return None
    n = int(s)
    return n if n >= min_value else None


def pause() -> None:
    input("\nPress Enter to continue...")

# ----------------------------
# normalize API list returns tool
# ----------------------------
def _extract_list(payload: Any) -> list[dict[str, Any]]:
    """Returns a flat list of dicts regardless of whether the API wraps the list in a key."""
    if isinstance(payload, list):
        return [x for x in payload if isinstance(x, dict)]
    if isinstance(payload, dict):
        for key in ("data", "results", "docs", "items", "episodes"):
            value = payload.get(key)
            if isinstance(value, list):
                return [x for x in value if isinstance(x, dict)]
    return []


# ----------------------------
# prompt for season + episode number tool
# ----------------------------
def prompt_season_episode() -> tuple[int, int] | None:
    season = prompt_int("S: ")
    if season is None:
        print("Invalid season number.")
        return None
    episode = prompt_int("E: ")
    if episode is None:
        print("Invalid episode number.")
        return None
    return season, episode


# ----------------------------
# fetch a single episode by season + episode number tool
# ----------------------------
def fetch_episode(season: int, epnum: int) -> dict[str, Any] | None:
    # API CALL: search episodes by season and episode number
    results = _extract_list(api_get("/episodes", params={"season": season, "episode": epnum, "limit": 1}))
    # confirm the result matches — some APIs ignore unknown params
    for ep in results:
        if ep.get("season") == season and ep.get("episode") == epnum:
            return ep
    return None

# Menu Options (4 total)

# ----------------------------
# Option 1: list episodes (paged)
# ----------------------------
def list_episodes_paged() -> None:
    from datetime import datetime

    def fmt_date(raw):
        # reformat air date to DD_Mon_YY
        for fmt in ("%m/%d/%Y", "%Y-%m-%d", "%B %d, %Y", "%b %d, %Y"):
            try:
                return datetime.strptime((raw or "").strip(), fmt).strftime("%d_%b_%y")
            except ValueError:
                pass
        return (raw or "")[:9] # truncate to 9 chars if unknown format

    def row(se, name, date):
        name = str(name)
        if len(name) > 38:
            name = name[:37] + "…"
        return f"{str(se):<12}  {name:<38}  {date}"

    # API CALL: fetch all episodes, then page locally
    episodes = _extract_list(api_get("/episodes"))

    if not episodes:
        print("No episodes returned from API.")
        pause()
        return

    episodes.sort(key=lambda ep: (int(ep.get("season", 0)), int(ep.get("episode", 0))))

    total = len(episodes)
    total_pages = (total + PAGE_SIZE - 1) // PAGE_SIZE
    page = 0

    # print header once, outside the loop so it stays visible
    print()
    print(row("S/E", "Episode Name", "Air Date"))
    print(row("-"*12, "-"*38, "-"*8))

    while True:
        start = page * PAGE_SIZE
        end   = min(start + PAGE_SIZE, total)

        print(f"\n  Page {page + 1}/{total_pages}  (episodes {start + 1}-{end} of {total})")
        for ep in episodes[start:end]:
            s  = ep.get("season",  "?")
            e  = ep.get("episode", "?")
            se = f"S:{s:<3} E:{e}"
            print(row(
                se,
                ep.get("name",    "N/A"),
                fmt_date(str(ep.get("airDate") or "")),
            ))

        cmd = input("\n[N]ext  [P]rev  [M]enu :").strip().lower()
        if cmd == "n":
            if page < total_pages - 1:
                page += 1
            else:
                print("Already at last page.")
        elif cmd == "p":
            if page > 0:
                page -= 1
            else:
                print("Already at first page.")
        elif cmd == "m":
            return
        else:
            print("Invalid choice.")


# ----------------------------
# Option 2: episode details by season + episode #
# ----------------------------
def episode_details() -> None:
    se = prompt_season_episode()
    if se is None:
        pause()
        return
    season, epnum = se

    ep = fetch_episode(season, epnum)
    if ep is None:
        print("Episode not found.")
        pause()
        return

    name = str(ep.get("name") or "N/A")
    season_ep = f"S{ep.get('season')}E{ep.get('episode')}"
    air_date = str(ep.get("airDate") or "N/A")
    viewers = str(ep.get("totalViewers") or "N/A")
    wiki_url = str(ep.get("wikiUrl") or "N/A")
    desc = (ep.get("description") or "").strip()
    if len(desc) > 240:
        desc = desc[:240].rstrip() + "..."

    print("\n=== Episode Details ===")
    print(f"Name:        {name}")
    print(f"Season/Ep:   {season_ep}")
    print(f"Air date:    {air_date}")
    print(f"Description: {desc}")
    print(f"Viewers:     {viewers}")
    print(f"Wiki URL:    {wiki_url}")
    pause()


# ----------------------------
# Option 3: gags by season + episode #
# ----------------------------
def episode_gags() -> None:
    se = prompt_season_episode() 
    if se is None:
        pause()
        return
    season, epnum = se

    # confirm episode exists before making three more API calls
    ep = fetch_episode(season, epnum)
    if ep is None:
        print("Episode not found.")
        pause()
        return

    print("\n=== Episode Gags ===")
    print(f"Episode: {ep.get('name', 'N/A')} (S{season}E{epnum})")

    # API CALL #2: Store Next Door
    store = api_get("/storeNextDoor", params={"season": season, "episode": epnum, "limit": 1})
    store_name = store[0].get("name") if isinstance(store, list) and store else None

    # API CALL #3: Burger of the Day
    burger = api_get("/burgerOfTheDay", params={"season": season, "episode": epnum, "limit": 1})
    burger_name  = burger[0].get("name")  if isinstance(burger, list) and burger else None
    burger_price = burger[0].get("price") if isinstance(burger, list) and burger else None

    # API CALL #4: Pest Control Truck
    truck = api_get("/pestControlTruck", params={"season": season, "episode": epnum, "limit": 1})
    truck_name = truck[0].get("name") if isinstance(truck, list) and truck else None

    print("\nStore Next Door:")
    print(f"  {store_name or '(none found)'}")

    print("\nBurger of the Day:")
    if burger_name and burger_price:
        print(f"  {burger_name} — {burger_price}")
    elif burger_name:
        print(f"  {burger_name}")
    else:
        print("  (none found)")

    print("\nPest Control Truck:")
    print(f"  {truck_name or '(none found)'}")

    pause()


# ----------------------------
# Main menu loop
# ----------------------------
def main() -> int:
    while True:
        print("\n=== Bob's Burgers Archive ===")
        print("1) List Episodes (paged, 10 per page)")
        print("2) Episode Details (by Season + Episode #)")
        print("3) Episode Gags (Store Next Door + Burger of the Day + Pest Control Truck) (by Season + Episode #)")
        print("4) Quit")

        choice = input("Select: ").strip()

        if choice == "1":
            list_episodes_paged()
        elif choice == "2":
            episode_details()
        elif choice == "3":
            episode_gags()
        elif choice == "4" or choice.lower() == "q":
            print("Goodbye.")
            return 0
        else:
            print("Invalid choice.")


if __name__ == "__main__":
    raise SystemExit(main())
