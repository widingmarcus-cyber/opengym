"""Main script that uses utilities."""

from utils import reverse_string, capitalize_words, clamp, average


def run():
    print(reverse_string("hello"))
    print(capitalize_words("hello world foo"))
    print(clamp(15, 0, 10))
    print(average([1, 2, 3, 4, 5]))


if __name__ == "__main__":
    run()
