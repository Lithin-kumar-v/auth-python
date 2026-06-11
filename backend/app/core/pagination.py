"""
=========================================================
Pageless Gradient
Enterprise Pagination System
=========================================================

Features
--------
✓ Pagination Parameters
✓ Offset Calculation
✓ Sorting
✓ Search
✓ Filtering Support
✓ Metadata
✓ Frontend Friendly
✓ API Consistency

=========================================================
"""

from __future__ import annotations

from math import ceil
from typing import Any
from typing import Generic
from typing import TypeVar

from pydantic import BaseModel
from pydantic import ConfigDict
from pydantic import Field

T = TypeVar("T")

# =========================================================
# Request Parameters
# =========================================================

class PaginationParams(BaseModel):
    """
    Standard pagination query params.
    """

    page: int = Field(
        default=1,
        ge=1,
        description="Page number",
    )

    limit: int = Field(
        default=20,
        ge=1,
        le=100,
        description="Items per page",
    )

    search: str | None = Field(
        default=None,
        description="Search term",
    )

    sort_by: str | None = Field(
        default=None,
        description="Sort field",
    )

    sort_order: str = Field(
        default="desc",
        pattern="^(asc|desc)$",
    )

    @property
    def offset(self) -> int:
        return (
            self.page - 1
        ) * self.limit

    @property
    def is_first_page(self) -> bool:
        return self.page == 1


# =========================================================
# Pagination Metadata
# =========================================================

class PaginationMeta(BaseModel):

    page: int
    limit: int

    total: int
    pages: int

    has_next: bool
    has_previous: bool

    next_page: int | None = None
    previous_page: int | None = None


# =========================================================
# Paginated Response
# =========================================================

class PaginatedResponse(
    BaseModel,
    Generic[T],
):
    """
    Standard paginated API response.
    """

    model_config = ConfigDict(
        arbitrary_types_allowed=True
    )

    success: bool = True

    data: list[T]

    pagination: PaginationMeta

    timestamp: str | None = None


# =========================================================
# Builder
# =========================================================

def build_paginated_response(
    *,
    items: list[Any],
    total: int,
    page: int,
    limit: int,
) -> dict:

    pages = max(
        ceil(total / limit),
        1,
    )

    return {
        "success": True,
        "data": items,
        "pagination": {
            "page": page,
            "limit": limit,
            "total": total,
            "pages": pages,
            "has_next": page < pages,
            "has_previous": page > 1,
            "next_page": (
                page + 1
                if page < pages
                else None
            ),
            "previous_page": (
                page - 1
                if page > 1
                else None
            ),
        },
    }


# =========================================================
# Helpers
# =========================================================

def calculate_offset(
    page: int,
    limit: int,
) -> int:

    return (
        page - 1
    ) * limit


def calculate_pages(
    total: int,
    limit: int,
) -> int:

    return max(
        ceil(total / limit),
        1,
    )