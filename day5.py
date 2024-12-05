from collections import defaultdict
from dataclasses import dataclass

PageOrderingRule = tuple[int, int]
PageDependencies = dict[int, set[int]]
PageUpdates = list[int]


@dataclass
class Input:
    page_ordering_rules: list[PageOrderingRule]
    page_dependencies: PageDependencies
    page_updates: list[PageUpdates]


def parse_input() -> Input:
    input = Input(
        page_ordering_rules=[],
        page_dependencies=defaultdict(lambda: set()),
        page_updates=[],
    )
    with open("inputs/day5.txt") as f:
        for line in f.readlines():
            line = line.strip()
            if "|" in line:
                a, b = line.split("|")
                input.page_ordering_rules.append((int(a), int(b)))
                input.page_dependencies[int(b)].add(int(a))
            elif line:
                updates = line.split(",")
                input.page_updates.append(list(map(int, updates)))

    return input


def verify_order(
    page_dependencies: PageDependencies,
    page_updates: PageUpdates,
) -> bool:
    for i, page_number in enumerate(page_updates):
        for other_page_number in page_updates[i + 1 :]:
            if other_page_number in page_dependencies[page_number]:
                return False

    return True


def sort_pages(
    page_dependencies: PageDependencies,
    page_updates: PageUpdates,
) -> PageUpdates:
    sorted_page_updates: PageUpdates = []
    required_page_numbers: set[int] = set(page_updates)
    visited_page_numbers: set[int] = set()

    def _insert_with_dependencies(page_number: int) -> None:
        for dependency in page_dependencies[page_number]:
            if (
                dependency in required_page_numbers
                and dependency not in visited_page_numbers
            ):
                _insert_with_dependencies(dependency)

        if page_number not in visited_page_numbers:
            sorted_page_updates.append(page_number)
            visited_page_numbers.add(page_number)

    for page_number in page_updates:
        _insert_with_dependencies(page_number)

    return sorted_page_updates


def get_middle_page(page_updates: PageUpdates) -> int:
    return page_updates[len(page_updates) // 2]


def solve() -> None:
    input = parse_input()

    correctly_ordered: list[PageUpdates] = []
    incorrectly_ordered: list[PageUpdates] = []
    for page_update in input.page_updates:
        if verify_order(input.page_dependencies, page_update):
            correctly_ordered.append(page_update)
        else:
            incorrectly_ordered.append(page_update)

    part_1 = sum(get_middle_page(page_update) for page_update in correctly_ordered)
    part_2 = sum(
        get_middle_page(sort_pages(input.page_dependencies, page_update))
        for page_update in incorrectly_ordered
    )
    print("Part 1:", part_1)
    print("Part 2:", part_2)


if __name__ == "__main__":
    solve()
