# AI Interactions Log

> **Stretch features only.** Only fill in the sections that apply to stretch features you attempted. If you did not attempt a stretch feature, leave its section blank or delete it. This file is not required for the core project.

---

## Agentic Workflow (SF8)

> Document your experience using an AI agent (e.g., Cursor Agent, Claude, Copilot) to make multi-step changes autonomously.

### Challenge 1: Advanced Song Features

**What task did you give the agent?**

Add 5+ new song attributes to the dataset and make the scoring use them.

**Prompts used:**

> "Introduce 5 or more complex attributes to your dataset that are not currently present, such as Song Popularity (0-100), Release Decade, or Detailed Mood Tags. Update both data/songs.csv and the scoring logic in src/recommender.py so scoring accounts for the new attributes."

**What did the agent generate or change?**

- `data/songs.csv`: added 5 columns to all 18 songs: `popularity` (0-100), `release_decade`, `mood_tag` (e.g. nostalgic, euphoric), `instrumentalness`, `speechiness`.
- `src/recommender.py`: new weights (mood_tag 1.0, popularity 0.5, release_decade 0.5, instrumentalness 0.25, speechiness 0.25), a `NUMERIC_RANGE` table so each numeric gap is scaled to 0-1, and a `max_score()` helper. `score_song` now loops over these tables. New features are optional, so existing profiles score as before.
- `src/main.py`: added a "Nostalgic Throwback" profile that uses the new features, and the score line now shows `max_score()` instead of a fixed 6.00.

**What did you verify or fix manually?**

- Ran `python src/main.py`: "Nostalgic Throwback" ranks Night Drive Loop first (6.65 / 6.75), and the reasons list shows every new feature.
- `pytest` still passes (the new `Song` fields have defaults).
- The agent first wrote `release_decade` 1800 for the classical song, which made the decade scale look odd. I changed it to 2000.
- The "Energy as string" adversarial profile still crashes. That was already the case before this change.

---

## Design Pattern (SF10)

> Document how AI helped you choose or implement a design pattern.

### Challenge 2: Multiple Scoring Modes

**Which design pattern did you use?**

Strategy pattern. A scoring mode is just a weight table, and the scoring code takes the table as a parameter.

**How did AI help you brainstorm or implement it?**

Prompt: *"Here is recommender.py. I want users to switch between ranking modes (Genre-First, Mood-First, Energy-Focused) in main.py. Suggest a simple design pattern that keeps the code modular."*

The AI suggested three options: a class per mode, a function per mode, or a dict of weight tables. It recommended the dict, because `score_song` already reads from `WEIGHTS`. A class per mode would repeat the same scoring loop four times. I accepted that suggestion.

**How does the pattern appear in your final code?**

- `SCORING_MODES` in `src/recommender.py` maps a mode name to a weight table: balanced, genre-first, mood-first, energy-focused.
- `score_song`, `recommend_songs` and `max_score` take an optional `weights` argument. It defaults to the balanced weights.
- `src/main.py` has a `--mode` flag, e.g. `python src/main.py --mode mood-first`.
- To add a mode, add one line to `SCORING_MODES`.

**Verification:** I ran all four modes. "Conflicted Listener" gets Rainfall Sonata first under genre-first (classical) and Iron Verdict first under mood-first and energy-focused. The tests still pass.

---

### Challenge 3: Diversity and Fairness Logic

**Prompt used:**

> "In recommend_songs, add a diversity penalty: when choosing the top k songs one at a time, subtract a single fixed penalty from a candidate's score if its artist or genre is already in the picks so far. Apply it once, not per repeat, and show it in the song's reasons."

**What the AI generated:**

- `DIVERSITY_PENALTY = 1.0` in `src/recommender.py`.
- `recommend_songs` now picks greedily: each round it re-scores the remaining songs against the artist and genre already chosen. Repeats lose 1.0 point and get a `repeat artist/genre (-1.0)` reason. Passing `diversity_penalty=0` turns it off.

**Verification:**

- "High-Energy Pop": Gym Hero (pop, already picked) drops from 3.66 to 2.66 and shows the penalty in its reasons, so the lower-scoring edm and rock songs sit close behind it.
- The tests still pass.
- With 18 songs, a 1.0 penalty only reorders close scores. It does not remove a song that is a much better match.

---

### Challenge 4: Visual Summary Table

**Prompt used:**

> "Suggest a way to use the tabulate library to display my top recommendations in the terminal. The table must include the reasons for each score."

**What the AI generated:**

- `src/main.py` prints each profile's results with `tabulate` in `grid` format. The columns are rank, title, artist, score out of the profile's maximum, and reasons.
- `maxcolwidths` wraps the long reasons text so the table stays readable in a normal terminal.
- `tabulate` is added to `requirements.txt`.

**Verification:** I ran `python src/main.py`. The table renders, every row shows its reasons (including the diversity penalty), and the tests still pass. The "Energy as string" adversarial profile still prints CRASHED, as before.
