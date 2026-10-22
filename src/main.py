"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

import argparse

from tabulate import tabulate

from recommender import SCORING_MODES, load_songs, max_score, recommend_songs

# Distinct user taste profiles for testing the recommender.
PROFILES = {
    "High-Energy Pop": {
        "genre": "pop",
        "mood": "happy",
        "energy": 0.9,
        "valence": 0.8,
        "acousticness": 0.1,
    },
    "Chill Lofi": {
        "genre": "lofi",
        "mood": "chill",
        "energy": 0.38,
        "valence": 0.58,
        "acousticness": 0.8,
    },
    "Deep Intense Rock": {
        "genre": "rock",
        "mood": "intense",
        "energy": 0.92,
        "valence": 0.45,
        "acousticness": 0.1,
    },
    # Uses the advanced song features (mood tag, decade, popularity, ...).
    "Nostalgic Throwback": {
        "genre": "synthwave",
        "mood": "moody",
        "mood_tag": "nostalgic",
        "energy": 0.7,
        "popularity": 60,
        "release_decade": 1980,
        "instrumentalness": 0.7,
    },
    # Edge case: the labels and the numbers pull in opposite directions.
    "Conflicted Listener": {
        "genre": "classical",
        "mood": "angry",
        "energy": 0.95,
        "valence": 0.25,
        "acousticness": 0.9,
    },
}


# Adversarial profiles: try to trick the scoring logic or hit silent failures.
ADVERSARIAL_PROFILES = {
    "Sad but high-energy":   {"genre": "pop", "mood": "sad", "energy": 0.9},
    "Metal wants peaceful":  {"genre": "metal", "mood": "peaceful", "energy": 0.95},
    "Wrong case":            {"genre": "Pop", "mood": "Happy", "energy": 0.8},
    "Unknown categories":    {"genre": "k-pop", "mood": "bittersweet", "energy": 0.7},
    "Energy out of range":   {"genre": "pop", "mood": "happy", "energy": 5.0},
    "Energy as percent":     {"genre": "pop", "mood": "happy", "energy": 90},
    "Empty profile":         {},
    "Wrong key names":       {"favorite_genre": "pop", "target_energy": 0.8},
    "Dead-center numerics":  {"energy": 0.5, "valence": 0.5, "acousticness": 0.5, "danceability": 0.5},
    "Loud but acoustic":     {"genre": "folk", "mood": "chill", "energy": 0.95, "acousticness": 1.0},
    "Sad but danceable":     {"mood": "sad", "valence": 0.0, "danceability": 1.0},
    "Energy as string":      {"genre": "pop", "mood": "happy", "energy": "0.9"},
}


def main() -> None:
    parser = argparse.ArgumentParser(description="Music Recommender Simulation")
    parser.add_argument("--mode", choices=SCORING_MODES, default="balanced",
                        help="scoring mode (default: balanced)")
    mode = parser.parse_args().mode
    weights = SCORING_MODES[mode]

    songs = load_songs("data/songs.csv")
    print(f"Loaded songs: {len(songs)}")
    print(f"Scoring mode: {mode}")

    line = "=" * 60
    for group, profiles in (("STANDARD", PROFILES), ("ADVERSARIAL", ADVERSARIAL_PROFILES)):
        print(f"\n\n##### {group} PROFILES #####")
        for name, user_prefs in profiles.items():
            print(f"\n{line}")
            print(f"  {name}")
            print(f"  Profile: {user_prefs}")
            print(line)
            try:
                recommendations = recommend_songs(user_prefs, songs, k=5, weights=weights)
            except Exception as exc:  # adversarial input may crash the scorer
                print(f"  CRASHED: {type(exc).__name__}: {exc}")
                continue
            top = max_score(user_prefs, weights)
            rows = [
                [rank, song["title"], song["artist"], f"{score:.2f} / {top:.2f}",
                 explanation or "no matching features"]
                for rank, (song, score, explanation) in enumerate(recommendations, start=1)
            ]
            print(tabulate(
                rows,
                headers=["#", "Title", "Artist", "Score", "Reasons"],
                tablefmt="grid",
                maxcolwidths=[None, 22, 16, None, 60],
            ))


if __name__ == "__main__":
    main()
