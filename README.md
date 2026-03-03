# Bob’s Burgers Library — README

## Basic Plan (Lab 3)

### Menu
1. **List Episodes** (paged, 10 per page)
2. **Episode Details** (by Season + Episode #)
3. **Episode Gags** (Store Next Door + Burger of the Day + Pest Control Truck) (by Season + Episode #)
4. **Quit**

### App Flow
- App displays the menu in a loop until the user quits.
- Options **2** and **3** prompt for **Season** and **Episode #** (episode number within season).
- Option **3** verifies the episode exists before requesting gag endpoints.

### API Calls

#### Option 1 — List Episodes
- `GET /episodes` (fetch all episodes once; then page locally)

#### Option 2 — Episode Details
- `GET /episodes?season=X&episode=Y&limit=1` (filtered lookup)

#### Option 3 — Episode Gags (all gags)
- `GET /episodes?season=X&episode=Y&limit=1` (confirm episode exists)
- `GET /storeNextDoor?season=X&episode=Y&limit=1`
- `GET /burgerOfTheDay?season=X&episode=Y&limit=1`
- `GET /pestControlTruck?season=X&episode=Y&limit=1`

---

## API Endpoints Used

All requests are **HTTPS GET only**.

- `GET /episodes`
- `GET /episodes?season={season}&episode={ep_num}&limit=1`
- `GET /storeNextDoor?season={season}&episode={ep_num}&limit=1`
- `GET /burgerOfTheDay?season={season}&episode={ep_num}&limit=1`
- `GET /pestControlTruck?season={season}&episode={ep_num}&limit=1`

---

## Progression / History

1. Selected the Bob’s Burgers API and confirmed it was public and authentication-free.
2. Updated the interaction model to **Season + Episode #** input to match how endpoints are queried.
3. Implemented:
   - Episode listing with local paging (10 per page)
   - Episode details lookup by Season/Episode
   - Episode gag lookup for Store Next Door, Burger of the Day, and Pest Control Truck
4. **GitHub note:** I started implementing my plan before I finished reading the Lab 4 instructions, and I started the GitHub portion of Lab 4 after I got the program running well. The repo now contains a baseline commit, and going forward I will make more frequent commits per feature and per bug fix as required.

---

## Issues (Log + Fixes)

- **GitHub setup done after most coding**
  - **Issue:** I forgot the GitHub portion of the lab until after most implementation work was completed.
  - **Fix:** Uploaded the current baseline; will now commit incrementally (feature-by-feature / bugfix-by-bugfix) and update this log as changes are made.

- **Episode ID input replaced with Season/Episode**
  - **Issue:** A numeric “Episode ID” is not the natural input for gag endpoints, which are indexed by season + episode number. Converting added complexity for no benefit.
  - **Fix:** Options **2** and **3** prompt for **Season #** and **Episode #** directly.

- **API response shape differences**
  - **Issue:** Some endpoints may return a list directly, while others can be wrapped in an object.
  - **Fix:** Added `_extract_list()` to normalize list responses; should be applied consistently across all endpoints.

- **Air date formatting**
  - **Issue:** Dates are returned as ISO strings, and formatting/parsing can fail if records differ.
  - **Fix:** Added a small `fmt_date()` helper with multiple parse patterns and a safe fallback.

- **Terminal output complexity**
  - **Issue:** Columns can get unwieldy or not fit correctly in a small terminal, making output unreadable. A two-adjacent-table layout introduced significant extra complexity with no real benefit, and there were unnecessary additional columns.
  - **Fix:** Standardized the format, kept output to a single table, and reduced columns to essential ones used by other menu functions.

---

## Lab 4 Credit Expectations (Self-Check)

- Frequent commits (**not completed**) — will commit per feature / per bug fix in future. 
- Issues logged in README and updated with solutions.
- Completed implementation of the Lab 3 plan.

---

## Reference

Bob’s Burgers API documentation: https://www.bobsburgersapi.com/documentation
