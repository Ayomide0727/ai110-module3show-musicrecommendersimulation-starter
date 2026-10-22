import csv
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass

@dataclass
class Song:
    """
    Represents a song and its attributes.
    Required by tests/test_recommender.py
    """
    id: int
    title: str
    artist: str
    genre: str
    mood: str
    energy: float
    tempo_bpm: float
    valence: float
    danceability: float
    acousticness: float
    popularity: int = 50
    release_decade: int = 2000
    mood_tag: str = ""
    instrumentalness: float = 0.0
    speechiness: float = 0.0

@dataclass
class UserProfile:
    """
    Represents a user's taste preferences.
    Required by tests/test_recommender.py
    """
    favorite_genre: str
    favorite_mood: str
    target_energy: float
    likes_acoustic: bool

# Point weights from the README's Algorithm Recipe (core maximum is 6.0).
# Categorical features are all-or-nothing; numeric features earn up to their
# weight based on how close the song is to the user's target.
# The last five entries are the advanced song features; like valence,
# acousticness and danceability they are skipped when the user gives no target.
WEIGHTS = {
    "mood": 2.0,
    "genre": 1.0,
    "energy": 1.5,
    "valence": 0.75,
    "acousticness": 0.5,
    "danceability": 0.25,
    "mood_tag": 1.0,
    "popularity": 0.5,
    "release_decade": 0.5,
    "instrumentalness": 0.25,
    "speechiness": 0.25,
}

# Scoring modes (Strategy pattern): each mode is just a weight table, so the
# scoring code never changes -- switching modes means passing a different table.
# Modes only re-weight the features; each one starts from the balanced weights.
SCORING_MODES = {
    "balanced": WEIGHTS,
    "genre-first": {**WEIGHTS, "genre": 4.0},
    "mood-first": {**WEIGHTS, "mood": 4.0, "mood_tag": 2.0},
    "energy-focused": {**WEIGHTS, "energy": 4.0},
}

# Size of each numeric feature's scale, used to turn a gap into a 0-1 closeness.
NUMERIC_RANGE = {
    "energy": 1.0,
    "valence": 1.0,
    "acousticness": 1.0,
    "danceability": 1.0,
    "popularity": 100.0,
    "release_decade": 60.0,
    "instrumentalness": 1.0,
    "speechiness": 1.0,
}

# Points removed from a song whose artist or genre is already in the top picks.
DIVERSITY_PENALTY = 1.0

CATEGORICAL_FEATURES = {"mood": "mood", "genre": "genre", "mood_tag": "mood_tag"}


def max_score(user_prefs: Dict, weights: Dict = WEIGHTS) -> float:
    """Highest score possible for the features this profile actually sets."""
    return sum(
        weight for feature, weight in weights.items()
        if user_prefs.get(feature) is not None
    )

class Recommender:
    """
    OOP implementation of the recommendation logic.
    Required by tests/test_recommender.py
    """
    def __init__(self, songs: List[Song]):
        self.songs = songs

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        # TODO: Implement recommendation logic
        return self.songs[:k]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        # TODO: Implement explanation logic
        return "Explanation placeholder"

def load_songs(csv_path: str) -> List[Dict]:
    """
    Loads songs from a CSV file.
    Required by src/main.py
    """
    # TODO: Implement CSV loading logic
    print(f"Loading songs from {csv_path}...")
    int_fields =("id", "popularity", "release_decade")
    float_fields = (
        "energy", "tempo_bpm", "valence", "danceability", "acousticness",
        "instrumentalness", "speechiness",
    )

    songs: List[Dict] = []
    with open(csv_path, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            for field in int_fields:
                row[field] = int(row[field])
            for field in float_fields:
                row[field] = float(row[field])
            songs.append(row)
    return songs

def score_song(user_prefs: Dict, song: Dict, weights: Dict = WEIGHTS) -> Tuple[float, List[str]]:
    """
    Scores a single song against user preferences.
    Required by recommend_songs() and src/main.py
    """
    # TODO: Implement scoring logic using your Algorithm Recipe from Phase 2.
    # Expected return format: (score, reasons)
    # user_prefs keys: genre, mood, energy; valence, acousticness and
    # danceability are optional and skipped when absent.
    score = 0.0
    reasons: List[str] = []

    for feature, song_key in CATEGORICAL_FEATURES.items():
        if user_prefs.get(feature) == song[song_key]:
            score += weights[feature]
            reasons.append(f"{feature.replace('_', ' ')} match (+{weights[feature]:.1f})")

    for feature, scale in NUMERIC_RANGE.items():
        target = user_prefs.get(feature)
        if target is None:
            continue
        points = weights[feature] * (1 - abs(float(song[feature]) - target) / scale)
        score += points
        reasons.append(
            f"{feature} close to target ({song[feature]} vs {target}) (+{points:.2f})"
        )

    return score, reasons

def recommend_songs(
    user_prefs: Dict,
    songs: List[Dict],
    k: int = 5,
    weights: Dict = WEIGHTS,
    diversity_penalty: float = DIVERSITY_PENALTY,
) -> List[Tuple[Dict, float, str]]:
    """
    Functional implementation of the recommendation logic.
    Required by src/main.py

    Picks the top k one at a time. A candidate whose artist or genre is already
    in the picks loses `diversity_penalty` points (once, not per repeat).
    """
    # Expected return format: (song_dict, score, explanation)
    remaining = [
        (song, score, reasons)
        for song in songs
        for score, reasons in [score_song(user_prefs, song, weights)]
    ]
    picks: List[Tuple[Dict, float, str]] = []
    while remaining and len(picks) < k:
        artists = {song["artist"] for song, _, _ in picks}
        genres = {song["genre"] for song, _, _ in picks}
        best = None
        for song, score, reasons in remaining:
            repeated = song["artist"] in artists or song["genre"] in genres
            adjusted = score - diversity_penalty if repeated else score
            if best is None or adjusted > best[1]:
                best = ((song, score, reasons), adjusted, repeated)
        (song, score, reasons), adjusted, repeated = best
        if repeated and diversity_penalty:
            reasons = reasons + [f"repeat artist/genre (-{diversity_penalty:.1f})"]
        picks.append((song, adjusted, ", ".join(reasons)))
        remaining = [r for r in remaining if r[0] is not song]
    return picks
