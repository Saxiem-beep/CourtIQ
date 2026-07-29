import bisect

class RealTimeLeaderboard:
    def __init__(self):
        self.athletes_db = {}  # O(1) lookup by ID
        self.ranking = []      # O(log n) inserts using bisect

    def add_or_update_athlete(self, athlete_id: str, name: str, team: str, score: float, risk_flag: str):
        # If athlete exists, remove their old score from the ranking list (O(n) worst case, but optimized)
        if athlete_id in self.athletes_db:
            old_score = self.athletes_db[athlete_id]["score"]
            old_entry = (-old_score, athlete_id)
            # Find and remove
            idx = bisect.bisect_left(self.ranking, old_entry)
            if idx < len(self.ranking) and self.ranking[idx] == old_entry:
                self.ranking.pop(idx)
        
        # Update DB
        self.athletes_db[athlete_id] = {
            "name": name,
            "team": team,
            "score": score,
            "risk_flag": risk_flag
        }
        
        # Insert new score into sorted list in O(log n)
        # We store negative score so the list is sorted descending
        new_entry = (-score, athlete_id)
        bisect.insort(self.ranking, new_entry)
        
    def get_top_n(self, n: int = 10, team_filter: str = "All"):
        results = []
        for neg_score, ath_id in self.ranking:
            data = self.athletes_db[ath_id]
            if team_filter == "All" or data["team"] == team_filter:
                results.append({
                    "ID": ath_id,
                    "Name": data["name"],
                    "Team": data["team"],
                    "Score": -neg_score,
                    "Status": data["risk_flag"]
                })
                if len(results) >= n:
                    break
        return results
