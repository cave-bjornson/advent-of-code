import math
from collections import deque, namedtuple
from dataclasses import dataclass, field
from functools import singledispatch, singledispatchmethod, total_ordering
from itertools import batched
from typing import NamedTuple

import aocd

from utils.fixture import Solution

PartitionTuple = namedtuple("PartitionTuple", ["point", "left_offset"], defaults=(0, 0))


@dataclass
@total_ordering
class Range:
    start: int
    end: int

    def __post_init__(self):
        if self.end < self.start:
            raise ValueError("End cannot be before start")

    def __contains__(self, item: int):
        return self.start <= item <= self.end

    def __eq__(self, other):
        return self.start == other.start and self.end == other.end

    def __lt__(self, other):
        return self.end < other.start


@dataclass
@total_ordering
class SeedFilter:
    start: int
    end: int
    offset: int

    def __contains__(self, item):
        if isinstance(item, int):
            return self.start <= item <= self.end
        if isinstance(item, Range):
            return (self.start <= item.start <= self.end) and (
                self.start <= item.end <= self.end
            )

    def __eq__(self, other):
        return self.start == other.start and self.end == other.end

    def __lt__(self, other):
        return self.end < other.start


def filter_seed_bag(bag: Range, seed_filter: SeedFilter) -> list[Range]:
    if bag in seed_filter:
        return [
            Range(
                start=bag.start + seed_filter.offset, end=bag.end + seed_filter.offset
            )
        ]

    if bag.end < seed_filter.start:
        return [bag]

    l_splitter = seed_filter.start - 1
    r_splitter = seed_filter.end + 1
    slices = []
    if seed_filter.start in bag and seed_filter.start != bag.start:
        slices.append(Range(start=bag.start, end=l_splitter))
        r_end = (
            seed_filter.end + seed_filter.offset
            if seed_filter.end in bag
            else bag.end + seed_filter.offset
        )
        slices.append(Range(seed_filter.start + seed_filter.offset, r_end))

    if seed_filter.end in bag and seed_filter.end != bag.end:
        if len(slices) == 0:
            slices.append(
                Range(
                    start=bag.start + seed_filter.offset,
                    end=seed_filter.end + seed_filter.offset,
                )
            )
        slices.append(Range(start=r_splitter, end=bag.end))

    return slices


def filter_seed(seed: int, seed_filter: SeedFilter) -> int:
    if seed in seed_filter:
        return seed + seed_filter.offset

    return seed


def generate_almanac_list(map_data) -> dict[str, [deque[SeedFilter]]]:
    almanac_list = dict[str, [deque[SeedFilter]]]()
    for maps in map_data[1:]:
        filters = [
            SeedFilter(
                start=source, end=source + length - 1, offset=destination - source
            )
            for destination, source, length in [
                [int(item) for item in sublist]
                for sublist in [m.split() for m in maps[1:]]
            ]
        ]

        filters.sort()
        filter_q = deque(filters)
        almanac_list[maps[0]] = filter_q

    return almanac_list


class Day5(Solution):
    def __init__(self):
        day, year = aocd.get_day_and_year()
        super().__init__(
            year,
            day,
            input_transform=lambda x: list(map(str.splitlines, x.split("\n\n"))),
        )

    def solution_a(self) -> int:
        almanac = self.input_data
        seeds = [int(s) for s in almanac[0][0].split()[1:]]
        seeds.sort()
        source_q = deque[int](seeds)
        destination_q = deque[int]()
        almanac_list = generate_almanac_list(almanac)

        for category, filter_q in almanac_list.items():
            destination_q.clear()
            while source_q and filter_q:
                if filter_q[0].end < source_q[0]:
                    filter_q.popleft()
                    continue
                else:
                    destination = filter_seed(source_q.popleft(), filter_q[0])
                    destination_q.append(destination)

            destination_q.extend(source_q)
            source_q.clear()
            source_q.extend(sorted(destination_q))

        return source_q[0]

    def solution_b(self) -> int:
        almanac = self.input_data
        seeds = [int(s) for s in almanac[0][0].split()[1:]]
        almanac_list = generate_almanac_list(almanac)

        batched_seeds = [
            c for b in [[a[0], sum(a) - 1] for a in batched(seeds, 2)] for c in b
        ]
        print(batched_seeds)
        paired = [Range(b[0], sum(b) - 1) for b in batched(seeds, 2)]
        paired.sort()
        print(paired)
        # paired = [RangeTuple(0, 51)]

        destination_q = deque[Range]()
        source_q = deque[Range]()
        # source_q = deque[RangeTuple](paired)
        lowest_location = math.inf
        used_q = list[SeedFilter]()
        for seed_bag in paired:
            source_q.clear()
            source_q.append(seed_bag)
            for category, filter_q in almanac_list.items():
                destination_q.clear()
                used_q.clear()
                while filter_q and source_q:
                    if filter_q[0].end < source_q[0].start:
                        used_q.append(filter_q.popleft())
                        continue
                    else:
                        bag = source_q.popleft()
                        bag_slices = filter_seed_bag(bag, filter_q[0])
                        if len(bag_slices) == 1:
                            destination_q.append(bag_slices[0])
                            continue
                        if len(bag_slices) > 1:
                            destination_q.extend(bag_slices[:-1])
                            source_q.appendleft(bag_slices[-1])

                destination_q.extend(source_q)
                source_q.clear()
                source_q.extend(sorted(destination_q))
                used_q.extend(filter_q)
                filter_q.clear()
                filter_q.extend(sorted(used_q))

            if source_q[0].start < lowest_location:
                lowest_location = source_q[0].start

        return lowest_location


if __name__ == "__main__":
    sol = Day5()
    sol.solve_examples(p1=False)
    sol.solve_real(p1=False)
    # sol.solve_performance(p2=False)
