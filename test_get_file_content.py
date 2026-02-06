from functions.get_file_content import get_file_content


def main():
    # 1) lorem truncation check (don’t print full content)
    lorem = get_file_content("calculator", "lorem.txt")
    print("Result for lorem.txt:")
    print("Length:", len(lorem))
    print('Truncated?', 'truncated at 10000 characters]' in lorem)
    print()

    # 2) Print full contents for these (so stdout includes 'def main():')
    print("Result for main.py:")
    print(get_file_content("calculator", "main.py"))
    print()

    print("Result for pkg/calculator.py:")
    print(get_file_content("calculator", "pkg/calculator.py"))
    print()

    # 3) Error cases
    print('Result for "/bin/cat":')
    print(get_file_content("calculator", "/bin/cat"))
    print()

    print('Result for "pkg/does_not_exist.py":')
    print(get_file_content("calculator", "pkg/does_not_exist.py"))
    print()


if __name__ == "__main__":
    main()
