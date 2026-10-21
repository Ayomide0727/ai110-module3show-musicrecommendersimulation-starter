# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name  

Give your model a short, descriptive name.  
Example: **VibeFinder 1.0**  

**MyMusic Finder**

---

## 2. Intended Use  

Describe what your recommender is designed to do and who it is for. 

Prompts:  

- What kind of recommendations does it generate  
- What assumptions does it make about the user  
- Is this for real users or classroom exploration  

- It suggests the top 5 songs from a small catalog for one user profile.
- It gives each song a score and says why it got that score.
- It assumes the user knows their favorite genre, mood and energy level.
- It assumes those tastes stay the same.
- This is for classroom learning, and for a simple demo with friends.
- It is not ready for real users.

---

## 3. How the Model Works  

Explain your scoring approach in simple language.  

Prompts:  

- What features of each song are used (genre, energy, mood, etc.)  
- What user preferences are considered  
- How does the model turn those into a score  
- What changes did you make from the starter logic  

Avoid code here. Pretend you are explaining the idea to a friend who does not program.

- Each song has a genre, a mood, and numbers for energy, happiness, acoustic sound and danceability.
- The user picks a favorite genre, a favorite mood and a target energy.
- They can also add targets for happiness, acoustic sound and danceability.
- The model gives each song points, then shows the best five.
- A mood match is worth 2 points.
- A genre match is worth 1 point.
- Energy is worth up to 1.5 points. The closer the song is to the target, the more points it gets.
- Happiness is worth up to 0.75, acoustic sound up to 0.5, and danceability up to 0.25.
- The best possible score is 6.
- The starter code only had empty to-do spots. I wrote the song loading, the scoring and the ranking.
- I also added a reason for every point, so the output explains itself.

---

## 4. Data  

Describe the dataset the model uses.  

Prompts:  

- How many songs are in the catalog  
- What genres or moods are represented  
- Did you add or remove data  
- Are there parts of musical taste missing in the dataset  

- The catalog has 18 songs.
- It has 15 genres, like pop, lofi, rock, jazz, metal and reggae.
- It has 14 moods, like happy, chill, intense, sad and romantic.
- Lofi has 3 songs and pop has 2. Every other genre has just 1.
- I did not add or remove any songs.
- Energy is lopsided. 8 songs are below 0.5, 8 are 0.75 or higher, and only 2 are in the middle.
- Many tastes are missing, like language, lyrics, decade, artist fame and tempo preferences.

---

## 5. Strengths  

Where does your system seem to work well  

Prompts:  

- User types for which it gives reasonable results  
- Any patterns you think your scoring captures correctly  
- Cases where the recommendations matched your intuition  

- It works well for users with clear, matching tastes.
- High-Energy Pop, Chill Lofi and Deep Intense Rock all got a top song that fit every label (scores 5.56 to 5.71).
- Opposite users get opposite lists. Chill Lofi and Deep Intense Rock share no songs in their top 5.
- Every score comes with reasons, so it is easy to see why a song ranked high.
- The results matched my gut. Sunrise City, Library Rain and Storm Runner were the songs I expected to win.

---

## 6. Limitations and Bias 

Where the system struggles or behaves unfairly. 

Prompts:  

- Features it does not consider  
- Genres or moods that are underrepresented  
- Cases where the system overfits to one preference  
- Ways the scoring might unintentionally favor some users  

**Weakness found: labels override the energy gap.**

- Mood (2.0) and genre (1.0) together are worth 3.0 of the 6.0 points, which is half of the maximum score.
- They are all-or-nothing, so a song either gets the full points or nothing, with no credit for similar labels like "pop" and "indie pop".
- Energy is worth at most 1.5 points, and a 0.7 energy gap costs only about 1 point, which is less than a single mood match.
- A `lofi / chill` user who asks for energy 0.9 still gets Midnight Coding (energy 0.42) at 3.78 and Library Rain (energy 0.35) at 3.67 at the top.
- A `classical / melancholic` user who asks for energy 0.9 still gets Rainfall Sonata (energy 0.18) at 3.42 as the top result.
- When I turned off the mood check, those mood-matched songs lost exactly 2.0 points and the rankings changed for 5 of 8 test profiles.
- 13 of the 15 genres and 11 of the 14 moods have only one song in the 18-song catalog.
- Those users get one forced match at #1, then filler songs chosen only by energy closeness.

---

## 7. Evaluation  

How you checked whether the recommender behaved as expected. 

Prompts:  

- Which user profiles you tested  
- What you looked for in the recommendations  
- What surprised you  
- Any simple tests or comparisons you ran  

No need for numeric metrics unless you created some.

**Profiles tested**

- Four standard profiles: High-Energy Pop, Chill Lofi, Deep Intense Rock and Conflicted Listener (classical + angry + energy 0.95).
- Twelve adversarial profiles, such as sad but high-energy, wrong capitalization, unknown genre, energy out of range, empty profile and energy given as a string.
- One experiment: I turned off the mood check and compared the rankings.

**What surprised me**

- Mood mattered more than I expected. Without it, perfect matches fell from about 5.6 to 3.6 and the rankings changed for 5 of 8 profiles.
- A `lofi / chill` user at high energy still got quiet songs, because the labels beat the energy gap.
- Bad input fails silently. Wrong capitalization, an unknown genre and an empty profile all return confident-looking results. Only the string energy crashed.
- With out-of-range energy, scores went negative (-1.77 for energy 5.0), and the `/ 6.00` display makes that look valid.

**Pairwise comparisons**

- **High-Energy Pop vs Chill Lofi:** Pop gets bright, loud songs (Sunrise City, energy 0.82). Lofi gets quiet, acoustic ones (Library Rain, energy 0.35). This makes sense because the energy, valence and acousticness targets are almost opposite.
- **High-Energy Pop vs Deep Intense Rock:** Both want energy near 0.9, so Gym Hero shows up in both top 3 lists. They differ at #1: Sunrise City (pop/happy) vs Storm Runner (rock/intense). Mood and genre decide it, which is valid.
- **High-Energy Pop vs Conflicted Listener:** Pop's top 5 are mostly high-energy songs. Conflicted Listener's #1 is metal/angry (Iron Verdict), because only that song matches the angry mood and the high energy. It makes sense, but its 4.29 score is lower than the 5.5+ of the clean profiles.
- **Chill Lofi vs Deep Intense Rock:** These are the opposite ends of the catalog. Their top 5 lists share no songs, and their energy targets (0.38 vs 0.92) are far apart. This is the clearest sign that the energy and mood inputs steer the output.
- **Chill Lofi vs Conflicted Listener:** Lofi gets mood and genre matches and scores 5.66. Conflicted Listener has to choose between its labels and its numbers. Its genre is classical, but Rainfall Sonata (0.18 energy) clashes with the 0.95 target, so it ranks #2 behind the angry metal song.
- **Deep Intense Rock vs Conflicted Listener:** Both want energy 0.92 to 0.95, so loud songs fill both lists. Rock has a song that matches all its labels (Storm Runner, 5.71). Conflicted Listener has none, so its top score drops to 4.29. This shows the model rewards consistent profiles and spreads out for conflicting ones.

---

## 8. Future Work  

Ideas for how you would improve the model next.  

Prompts:  

- Additional features or preferences  
- Better ways to explain recommendations  
- Improving diversity among the top results  
- Handling more complex user tastes  

- Add more songs. Every genre and mood needs several, and the middle energy range needs more.
- Give partial credit for similar labels, like "pop" and "indie pop", or "chill" and "relaxed".
- Make energy count more, so a big mismatch costs more than a mood match.
- Keep the top 5 diverse. No repeat artists, and a mix of genres.
- Check the input. Fix capital letters, reject strings, and keep numbers between 0 and 1.
- Warn the user when no genre or mood matches.

---

## 9. Personal Reflection  

A few sentences about your experience.  

Prompts:  

- What you learned about recommender systems  
- Something unexpected or interesting you discovered  
- How this changed the way you think about music recommendation apps  

- A few simple point rules can give results that feel smart.
- Labels can trap users. A `lofi / chill` user who wanted high energy still got quiet songs.
- Edge cases taught me the most. Odd profiles found problems the normal ones hid.
- It surprised me that bad input did not crash. It just gave confident, wrong answers.
- Now I wonder how real music apps avoid putting people in a bubble.
- I also see that a good app needs lots of songs, not just a good formula.
