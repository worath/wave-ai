from pydantic import BaseModel
from typing import Literal
import re

from pydantic import BaseModel
from typing import Literal


class ProjectAnalysis(BaseModel):
    project_type: Literal[
        "ecommerce",
        "corporate",
        "portfolio",
        "unknown"
    ]

    features: list[str]

    estimated_complexity: Literal[
        "low",
        "medium",
        "high"
    ]

    product_count: int | None = None