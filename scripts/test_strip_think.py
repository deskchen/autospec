#!/usr/bin/env python3
from scripts.gen_specs import strip_think_wrappers, extract_corrected_code


def test_strip_think_plain():
    raw = "<think>\nfoo\n</think>\nint main() {return 0;}\n"
    cleaned = strip_think_wrappers(raw)
    assert cleaned.startswith("int main"), cleaned


def test_strip_think_with_code_block():
    raw = "<think>\nblah\n</think>\n```c\nint main(){return 0;}\n```\n"
    extracted = extract_corrected_code(raw)
    assert extracted.strip().startswith("<think>"), extracted  # extract_corrected_code returns inside fence
    cleaned = strip_think_wrappers(extracted)
    assert cleaned.startswith("int main"), cleaned


if __name__ == "__main__":
    # test_strip_think_plain()
    test_strip_think_with_code_block()
    print("OK")

