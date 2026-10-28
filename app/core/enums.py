"""Enumeraciones del dominio, compartidas por modelos, schemas y servicios."""

from enum import StrEnum


class TournamentFormat(StrEnum):
    SINGLE_ELIMINATION = "single_elimination"
    SWISS = "swiss"
    ROUND_ROBIN = "round_robin"


class TournamentStatus(StrEnum):
    DRAFT = "draft"
    REGISTRATION = "registration"
    IN_PROGRESS = "in_progress"
    FINISHED = "finished"
    CANCELLED = "cancelled"
