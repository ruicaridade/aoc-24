MIN_DELTA = 1
MAX_DELTA = 3


def parse_reports() -> list[list[int]]:
    reports: list[list[int]] = []
    with open("inputs/day2.txt") as f:
        for line in f.read().splitlines():
            reports.append([int(x) for x in line.split(" ") if x])

    return reports


def is_report_safe(report: list[int]) -> bool:
    for i in range(len(report)):
        if i == 0:
            continue

        prev, curr = report[i - 1], report[i]
        curr_delta = curr - prev
        if abs(curr_delta) < MIN_DELTA or abs(curr_delta) > MAX_DELTA:
            return False

        if i - 2 >= 0:
            prev_delta = prev - report[i - 2]
            if curr_delta > 0 and prev_delta < 0 or curr_delta < 0 and prev_delta > 0:
                return False

    return True


def part_1() -> None:
    reports = parse_reports()

    safe_count: int = 0
    for report in reports:
        if is_report_safe(report):
            safe_count += 1

    print(safe_count)


def part_2() -> None:
    reports = parse_reports()

    safe_count: int = 0
    for report in reports:
        if is_report_safe(report):
            safe_count += 1
            continue

        for i in range(len(report)):
            dampened_report = list(report)
            dampened_report.pop(i)
            if is_report_safe(dampened_report):
                safe_count += 1
                break

    print(safe_count)


if __name__ == "__main__":
    part_1()
    part_2()
