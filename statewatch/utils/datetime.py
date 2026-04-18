from itertools import groupby
from datetime import timedelta, datetime


def group_consecutive_dates(dates: list[datetime]):
    """
    Group consecutive datetime values into continuous date ranges.

    This function takes a list of datetime objects, removes duplicates,
    sorts them in ascending order, and groups consecutive dates into
    (start, end) tuples. Dates are considered consecutive if they differ
    by exactly one day.

    Parameters
    ----------
    dates : list of datetime
        A list of datetime objects. The list may be unsorted and contain duplicates.

    Returns
    -------
    list of tuple of datetime
        A list of tuples where each tuple represents a consecutive date range:
        (start_date, end_date). For single isolated dates, start and end will be the same.

    Notes
    -----
    - Time components of the datetime objects are preserved but ignored for
      grouping logic (only day differences are considered).
    - Duplicate dates are automatically removed.
    - The function assumes daily granularity (i.e., 1-day intervals).

    Examples
    --------
    Basic usage with consecutive and non-consecutive dates:

    >>> from datetime import datetime
    >>> dates = [
    ...     datetime(2026, 1, 1),
    ...     datetime(2026, 1, 2),
    ...     datetime(2026, 1, 3),
    ...     datetime(2026, 1, 5),
    ...     datetime(2026, 1, 6),
    ... ]
    >>> group_consecutive_dates(dates)
    [(datetime(2026, 1, 1, 0, 0), datetime(2026, 1, 3, 0, 0)),
     (datetime(2026, 1, 5, 0, 0), datetime(2026, 1, 6, 0, 0))]

    Example with unsorted input and duplicates:

    >>> dates = [
    ...     datetime(2026, 1, 3),
    ...     datetime(2026, 1, 1),
    ...     datetime(2026, 1, 2),
    ...     datetime(2026, 1, 2),  # duplicate
    ... ]
    >>> group_consecutive_dates(dates)
    [(datetime(2026, 1, 1, 0, 0), datetime(2026, 1, 3, 0, 0))]

    Example with isolated dates:

    >>> dates = [
    ...     datetime(2026, 1, 1),
    ...     datetime(2026, 1, 3),
    ...     datetime(2026, 1, 5),
    ... ]
    >>> group_consecutive_dates(dates)
    [(datetime(2026, 1, 1, 0, 0), datetime(2026, 1, 1, 0, 0)),
     (datetime(2026, 1, 3, 0, 0), datetime(2026, 1, 3, 0, 0)),
     (datetime(2026, 1, 5, 0, 0), datetime(2026, 1, 5, 0, 0))]

    """
    dates = sorted(set(dates))

    groups = []
    for _, group in groupby(
        enumerate(dates), key=lambda x: x[1] - timedelta(days=x[0])
    ):
        group = [g[1] for g in group]
        groups.append((group[0], group[-1]))

    return groups
