from __future__ import annotations
from dataclasses import dataclass
import python.f1fast.exceptions.analysis_exceptions as e


@dataclass(frozen=True, eq=False)  # eq=False para definir el nuestro
class DriverId:
    abbreviation: str
    full_name: str

    def __post_init__(self):
        if not self.abbreviation or len(self.abbreviation.strip()) != 3:
            raise e.ConfigurationError(
                f"DriverId: abbreviation inválida: '{self.abbreviation}'"
            )
        object.__setattr__(self, 'abbreviation', self.abbreviation.upper().strip())
        object.__setattr__(self, 'full_name', self.full_name.strip())

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, DriverId):
            return NotImplemented
        return self.abbreviation == other.abbreviation

    def __hash__(self) -> int:
        return hash(self.abbreviation)

    def __str__(self) -> str:
        return self.abbreviation

    def __repr__(self) -> str:
        return f"DriverId({self.abbreviation})"

    @classmethod
    def from_result_row(cls, row) -> "DriverId":
        return cls(
            abbreviation=row["Abbreviation"],
            full_name=row["FullName"]
        )