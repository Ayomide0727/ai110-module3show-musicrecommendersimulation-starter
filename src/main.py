"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

from recommender import load_songs, recommend_songs


def main() -> None:
    songs = load_songs("data/songs.csv")
    print(f"Loaded songs: {len(songs)}")

    # Starter example profile
    user_prefs = {"genre": "pop", "mood": "happy", "energy": 0.8}

    recommendations = recommend_songs(user_prefs, songs, k=5)

    line = "=" * 60
    print(f"\n{line}")
    print(f"  TOP {len(recommendations)} RECOMMENDATIONS")
    print(f"  Profile: {user_prefs}")
    print(line)
    for rank, rec in enumerate(recommendations, start=1):
        # You decide the structure of each returned item.
        # A common pattern is: (song, score, explanation)
        song, score, explanation = rec
        print(f"\n{rank}. {song['title']} by {song['artist']}")
        print(f"   Score: {score:.2f} / 6.00")
        print("   Reasons:")
        for reason in explanation.split(", "):
            print(f"     - {reason}")
    print(f"\n{line}")


if __name__ == "__main__":
    main()
