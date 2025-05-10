from task5 import run_unsafe_increment, run_safe_increment


def test_race_condition():
    unsafe = run_unsafe_increment()
    safe = run_safe_increment()

    assert unsafe < safe
    print(f"\nРазница: {safe - unsafe} потерянных инкрементов")


def test_consistent_failure():
    failures = 0
    test_runs = 3

    for _ in range(test_runs):
        unsafe = run_unsafe_increment()
        safe = run_safe_increment()

        if unsafe < safe:
            failures += 1

    assert failures >= test_runs - 1
    print(f"Гонка обнаружена в {failures} из {test_runs} запусков")