from dataclasses import dataclass


@dataclass
class Config:
    qbit_host: str
    qbit_user: str
    qbit_password: str
    monitor_path: str
    free_space: int | None
    free_space_ratio: float | None
    delete_by_completed_on: bool
    min_delete_size: int | None
    allowed_categories: list[str]
