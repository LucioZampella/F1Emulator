import python.f1fast.main.errors.Errors as e

class TeamValidator:

    @staticmethod
    def validate_team_exists(results, team_name: str) -> e:
        if team_name not in results["TeamName"].values:
            raise e.TeamNotFoundError(f"Team {team_name} was not found in this session")
