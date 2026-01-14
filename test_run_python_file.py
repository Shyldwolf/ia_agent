from functions.run_python_file import run_python_file


def run_tests():
    print("TEST 1: run_python_file('calculator', 'main.py')")
    print(run_python_file("calculator", "main.py"))
    print("-" * 60)

    print("TEST 2: run_python_file('calculator', 'main.py', ['3 + 5'])")
    print(run_python_file("calculator", "main.py", ["3 + 5"]))
    print("-" * 60)

    print("TEST 3: run_python_file('calculator', 'tests.py')")
    print(run_python_file("calculator", "tests.py"))
    print("-" * 60)

    print("TEST 4: run_python_file('calculator', '../main.py')")
    print(run_python_file("calculator", "../main.py"))
    print("-" * 60)

    print("TEST 5: run_python_file('calculator', 'nonexistent.py')")
    print(run_python_file("calculator", "nonexistent.py"))
    print("-" * 60)

    print("TEST 6: run_python_file('calculator', 'lorem.txt')")
    print(run_python_file("calculator", "lorem.txt"))
    print("-" * 60)


if __name__ == "__main__":
    run_tests()
