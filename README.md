# 🎵 Music Recommender Simulation

## Project Summary

In this project you will build and explain a small music recommender system.

Your goal is to:

- Represent songs and a user "taste profile" as data
- Design a scoring rule that turns that data into recommendations
- Evaluate what your system gets right and wrong
- Reflect on how this mirrors real world AI recommenders

Replace this paragraph with your own summary of what your version does.

---

## How The System Works

Explain your design in plain language.

Some prompts to answer:

- What features does each `Song` use in your system
  - For example: genre, mood, energy, tempo
- What information does your `UserProfile` store
- How does your `Recommender` compute a score for each song
- How do you choose which songs to recommend

You can include a simple diagram or bullet list if helpful.

**My understanding and approach:** Real-world platforms like Spotify and YouTube combine collaborative filtering (learning from what similar users play, skip, and save) with content-based filtering (matching song attributes like energy, mood, and acousticness), then rank the results using many signals. My version is a simple content-based recommender. It scores each song by how *close* its features are to the user's targets, not by whether the values are high or low. It prioritizes mood and energy, then valence, with genre and acousticness as smaller bonuses. Songs are then ranked by score and the top results are returned.

# Song features used in scoring
mood (categorical): exact-match bonus, highest weight
energy (0–1): closeness to the user's target
valence (0–1): closeness to the user's target
genre (categorical): exact-match bonus
acousticness (0–1): closeness to the user's target, small weight

Identifiers: id, title and artist are for display only.

# UserProfile features
favorite_mood (str): compared with Song.mood
target_energy (float, 0–1): compared with Song.energy
target_valence (float, 0–1): compared with Song.valence
favorite_genre (str): compared with Song.genre
target_acousticness (float, 0–1): compared with Song.acousticnes

### Algorithm Recipe

Every song in `data/songs.csv` gets a score against the user's profile, then songs are ranked from highest to lowest and the top `k` are returned.

| Feature | Max points | How it is scored |
|---|---|---|
| Mood | 2.0 | +2.0 for an exact match, otherwise 0 |
| Genre | 1.0 | +1.0 for an exact match, otherwise 0 |
| Energy | 1.5 | `1.5 * (1 - abs(song.energy - target_energy))` |
| Valence | 0.75 | `0.75 * (1 - abs(song.valence - target_valence))` |
| Acousticness | 0.5 | `0.5 * (1 - abs(song.acousticness - target_acousticness))` |
| Danceability | 0.25 | `0.25 * (1 - abs(song.danceability - target_danceability))`, tie-breaker only |

- **Maximum score:** 6.0. Divide by 6 for a 0–1 score.
- **Numeric features** reward closeness to the target, not high or low values. A song at 0.4 energy scores well for a user targeting 0.4 and poorly for a user targeting 0.9.
- **Missing targets are skipped.** If the user profile has no target for a numeric feature, that feature adds no points for any song.
- **Explanations:** each recommendation lists the points every feature contributed, so a score can always be traced back to its reasons.
- **Why these weights:** mood is the listener's intent and carries across genres, so it is weighted highest. Genre is unique for 14 of the 18 songs in the dataset, so a large genre bonus would just pick a single song and leave the rest unranked. Energy varies the most (0.18 to 0.97), so it separates songs best.

### Expected Biases and Limitations

- **Mood can overpower everything else.** At +2.0, a song with the right mood but a poor energy, valence and acousticness fit can still outrank a song that is close on every numeric feature but has a different mood label. Great songs with a neighboring mood (for example "chill" vs "relaxed") get no mood credit at all.
- **Exact-match labels are brittle.** "indie pop" does not match "pop", and "relaxed" does not match "chill", even though a listener would treat them as close.
- **Genre can be under-served.** Because genre is only +1.0, a user who strongly cares about genre may see off-genre songs ranked above an on-genre song.
- **The dataset is tiny and uneven.** With 18 songs, most genres and moods have a single song. Users who prefer a common label (lofi, chill, pop) get more choice than everyone else, and some users have only one real match.
- **No personalization over time.** The profile is static: there is no listening history, skip data or similar-user signal, so the system cannot learn that a user's taste differs from what they stated.
- **Feature averaging hides contradictions.** A user who wants "angry" mood with very low energy gets a confusing mix, because the numeric closeness scores partly cancel the mood bonus.

---

## Getting Started

### Setup

1. Create a virtual environment (optional but recommended):

   ```bash
   python -m venv .venv
   source .venv/bin/activate      # Mac or Linux
   .venv\Scripts\activate         # Windows

2. Install dependencies

```bash
pip install -r requirements.txt
```

3. Run the app:

```bash
python -m src.main
```

### Running Tests

Run the starter tests with:

```bash
pytest
```

You can add more tests in `tests/test_recommender.py`.

---

## Sample Recommendation Output

Paste a sample of your recommender's output here as a text block so a reader can see what it produces:

Output of `python src/main.py` for the profile `genre=pop, mood=happy, energy=0.8`:

```
Loading songs from data/songs.csv...
Loaded songs: 18

============================================================
  TOP 5 RECOMMENDATIONS
  Profile: {'genre': 'pop', 'mood': 'happy', 'energy': 0.8}
============================================================

1. Sunrise City by Neon Echo
   Score: 4.47 / 6.00
   Reasons:
     - mood match (+2.0)
     - genre match (+1.0)
     - energy close to target (0.82 vs 0.8) (+1.47)

2. Rooftop Lights by Indigo Parade
   Score: 3.44 / 6.00
   Reasons:
     - mood match (+2.0)
     - energy close to target (0.76 vs 0.8) (+1.44)

3. Gym Hero by Max Pulse
   Score: 2.30 / 6.00
   Reasons:
     - genre match (+1.0)
     - energy close to target (0.93 vs 0.8) (+1.30)

4. Concrete Crown by Verse Valley
   Score: 1.47 / 6.00
   Reasons:
     - energy close to target (0.78 vs 0.8) (+1.47)

5. Night Drive Loop by Neon Echo
   Score: 1.42 / 6.00
   Reasons:
     - energy close to target (0.75 vs 0.8) (+1.42)

============================================================
```

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or demo video link here -->

## Recommendations by Profile

Condensed terminal output of `python src/main.py` (title, genre/mood, score out of 6.00).

### Standard profiles (top 5)

```
High-Energy Pop  {'genre': 'pop', 'mood': 'happy', 'energy': 0.9, 'valence': 0.8, 'acousticness': 0.1}
  1. Sunrise City (pop/happy) 5.56
  2. Rooftop Lights (indie pop/happy) 4.41
  3. Gym Hero (pop/intense) 3.66
  4. Neon Overdrive (edm/euphoric) 2.56
  5. Storm Runner (rock/intense) 2.50

Chill Lofi  {'genre': 'lofi', 'mood': 'chill', 'energy': 0.38, 'valence': 0.58, 'acousticness': 0.8}
  1. Library Rain (lofi/chill) 5.66
  2. Midnight Coding (lofi/chill) 5.63
  3. Spacewalk Thoughts (ambient/chill) 4.49
  4. Focus Flow (lofi/focused) 3.70
  5. Coffee Shop Stories (jazz/relaxed) 2.59

Deep Intense Rock  {'genre': 'rock', 'mood': 'intense', 'energy': 0.92, 'valence': 0.45, 'acousticness': 0.1}
  1. Storm Runner (rock/intense) 5.71
  2. Gym Hero (pop/intense) 4.47
  3. Iron Verdict (metal/angry) 2.50
  4. Night Drive Loop (synthwave/moody) 2.40
  5. Concrete Crown (hip hop/confident) 2.40

Conflicted Listener  {'genre': 'classical', 'mood': 'angry', 'energy': 0.95, 'valence': 0.25, 'acousticness': 0.9}
  1. Iron Verdict (metal/angry) 4.29
  2. Rainfall Sonata (classical/melancholic) 2.54
  3. Storm Runner (rock/intense) 2.12
  4. Night Drive Loop (synthwave/moody) 1.93
  5. Gym Hero (pop/intense) 1.91
```

### Selected adversarial profiles (top 3)

```
Sad but high-energy  {'genre': 'pop', 'mood': 'sad', 'energy': 0.9}
  1. Empty Chair Blues (blues/sad) 2.65
  2. Gym Hero (pop/intense) 2.46
  3. Sunrise City (pop/happy) 2.38

Wrong case  {'genre': 'Pop', 'mood': 'Happy', 'energy': 0.8}
  1. Sunrise City (pop/happy) 1.47
  2. Concrete Crown (hip hop/confident) 1.47
  3. Rooftop Lights (indie pop/happy) 1.44

Energy out of range  {'genre': 'pop', 'mood': 'happy', 'energy': 5.0}
  1. Sunrise City (pop/happy) -1.77
  2. Rooftop Lights (indie pop/happy) -2.86
  3. Gym Hero (pop/intense) -3.61

Empty profile  {}
  1. Sunrise City (pop/happy) 0.00
  2. Midnight Coding (lofi/chill) 0.00
  3. Storm Runner (rock/intense) 0.00

Energy as string  {'genre': 'pop', 'mood': 'happy', 'energy': '0.9'}
  CRASHED: TypeError: unsupported operand type(s) for -: 'float' and 'str'
```

Takeaways: mood (2.0) outweighs genre (1.0), unmatched labels silently drop out, out-of-range energy gives negative scores, and a string energy crashes the scorer.

---

## Experiments You Tried

Use this section to document the experiments you ran. For example:

- What happened when you changed the weight on genre from 2.0 to 0.5
- What happened when you added tempo or valence to the score
- How did your system behave for different types of users

---

## Limitations and Risks

Summarize some limitations of your recommender.

Examples:

- It only works on a tiny catalog
- It does not understand lyrics or language
- It might over favor one genre or mood

You will go deeper on this in your model card.

---

## Reflection

Read and complete `model_card.md`:

[**Model Card**](model_card.md)

Write 1 to 2 paragraphs here about what you learned:

- about how recommenders turn data into predictions
- about where bias or unfairness could show up in systems like this



