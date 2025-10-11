from sqlalchemy.orm import Session
import string
from datetime import datetime
from models.SquadPlayer import SquadPlayer
from models.Squad import Squad
from .stats_service import StatsService


class ScoringService:
    @staticmethod
    def calculate_squad_round_score(db: Session, squad_id: int, round_id: int):
        # Get all players in the squad for the round
        squad_starters = db.query(SquadPlayer).filter(
            SquadPlayer.squad_id == squad_id,
            SquadPlayer.is_starter == True
        ).all()

        squad_bench = db.query(SquadPlayer).filter(
            SquadPlayer.squad_id == squad_id,
            SquadPlayer.is_starter == False
        ).all()

        # Get stats for each player (filter out None results)
        starter_stats = []
        for player in squad_starters:
            if player.player_id:  # Only get stats if player exists
                stats = StatsService.get_player_stats_for_round(db, player.player_id, round_id)
                if stats:
                    starter_stats.append((player, stats))

        bench_stats = []
        for player in squad_bench:
            if player.player_id:  # Only get stats if player exists
                stats = StatsService.get_player_stats_for_round(db, player.player_id, round_id)
                if stats:
                    bench_stats.append((player, stats))

        # Apply substitutions and calculate score
        playing_squad, substitutions = ScoringService._apply_substitutions(starter_stats, bench_stats)

        # Calculate base points from playing squad
        base_points = sum(stats.fantasy_points for _, stats in playing_squad)

        # Get squad for captain/kicker info
        squad = db.query(Squad).filter(Squad.id == squad_id).first()
        if not squad:
            raise ValueError("Squad not found")

        # Calculate bonuses
        captain_bonus = ScoringService._calculate_captain_bonus(squad, playing_squad)
        kicker_bonus = ScoringService._calculate_kicker_bonus(squad, playing_squad)

        total_points = base_points + captain_bonus + kicker_bonus

        # Update league member points
        ScoringService._update_league_member_points(db, squad.league_member_id, total_points)

        return {
            "squad_id": squad_id,
            "round_id": round_id,
            "total_points": total_points,
            "base_points": base_points,
            "captain_bonus": captain_bonus,
            "kicker_bonus": kicker_bonus,
            "substitutions": substitutions,
            "playing_squad": [{"player_id": player.player_id, "fantasy_points": stats.fantasy_points} for player, stats in playing_squad]
        }

    @staticmethod
    def _apply_substitutions(starter_stats, bench_stats):
        """
        Apply substitutions for non-playing starters.
        Returns: (playing_squad, substitutions_made)
        """
        playing_squad = []
        substitutions = []

        # Create a dictionary of available bench players by position
        available_subs = {}
        for bench_player, bench_stat in bench_stats:
            position = bench_player.squad_position.split("-")[0]  # Extract position (e.g., "PR" from "PR-B-1")
            if position not in available_subs:
                available_subs[position] = []
            available_subs[position].append((bench_player, bench_stat))

        # Sort bench players by fantasy points (highest first) for each position
        for position in available_subs:
            available_subs[position].sort(key=lambda x: x[1].fantasy_points, reverse=True)

        # Process each starter
        for starter_player, starter_stats in starter_stats:
            starter_position = starter_player.squad_position.split("-")[0]

            # Check if starter played (minutes > 0)
            if starter_stats.minutes_played > 0:
                # Starter played, use their score
                playing_squad.append((starter_player, starter_stats))
            else:
                # Starter didn't play, try to substitute
                if starter_position in available_subs and available_subs[starter_position]:
                    # Get the best available substitute for this position
                    sub_player, sub_stats = available_subs[starter_position].pop(0)
                    playing_squad.append((sub_player, sub_stats))
                    substitutions.append({
                        "starter_out": starter_player.player_id,
                        "substitute_in": sub_player.player_id,
                        "position": starter_position
                    })
                else:
                    # No substitute available, starter gets 0 points
                    playing_squad.append((starter_player, starter_stats))

        return playing_squad, substitutions

    @staticmethod
    def _calculate_captain_bonus(squad: Squad, playing_squad) -> int:
        """Calculate captain bonus (2x points for captain, or vice-captain if captain didn't play)"""
        captain_bonus = 0

        # Find captain and vice-captain in playing squad
        captain_stats = None
        vice_captain_stats = None

        for player, stats in playing_squad:
            if player.player_id == squad.captain_id and stats.minutes_played > 0:
                captain_stats = stats
            elif player.player_id == squad.vice_captain_id and stats.minutes_played > 0:
                vice_captain_stats = stats

        # Apply captain bonus
        if captain_stats:
            captain_bonus = captain_stats.fantasy_points  # 2x total - original = bonus
        elif vice_captain_stats:
            captain_bonus = vice_captain_stats.fantasy_points  # Vice-captain gets the bonus

        return captain_bonus

    @staticmethod
    def _calculate_kicker_bonus(squad: Squad, playing_squad) -> int:
        """Calculate kicker bonus (extra points for conversions, penalties, drop goals)"""
        kicker_bonus = 0

        # Find kicker and backup kicker in playing squad
        kicker_stats = None
        backup_kicker_stats = None

        for player, stats in playing_squad:
            if player.player_id == squad.kicker_id and stats.minutes_played > 0:
                kicker_stats = stats
            elif player.player_id == squad.backup_kicker_id and stats.minutes_played > 0:
                backup_kicker_stats = stats

        # Apply kicker bonus
        if kicker_stats:
            # Primary kicker gets bonus: 1 point per conversion/penalty, 3 per drop goal
            kicker_bonus = (kicker_stats.conversions + kicker_stats.penalties) * 2 + kicker_stats.drop_goals * 3
        elif backup_kicker_stats:
            # Backup kicker gets bonus only if primary didn't play
            kicker_bonus = (backup_kicker_stats.conversions + backup_kicker_stats.penalties) * 2 + backup_kicker_stats.drop_goals * 3

        return kicker_bonus

    @staticmethod
    def _update_league_member_points(db: Session, league_member_id: int, points: int):
        """Update the league member's total points"""
        from models.LeagueMember import LeagueMember

        league_member = db.query(LeagueMember).filter(LeagueMember.id == league_member_id).first()
        if league_member:
            league_member.points += points  # Add this round's points to total
            db.commit()
            return True
        return False