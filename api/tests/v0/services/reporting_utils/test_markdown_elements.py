from src.v0.services.reporting_utils import markdown_elements


def test_header_tag():
    assert markdown_elements._header_tag(3) == "###"


def test_list_symbol():
    assert markdown_elements._list_symbol("unordered") == "- "
    assert markdown_elements._list_symbol("ordered") == "1. "


def test_header_prefix_only():
    assert markdown_elements.header(2, "Title") == "## Title\n\n"


def test_header_prefix_and_data():
    assert (
        markdown_elements.header(2, "Title", "Once upon a time")
        == "## Title: Once upon a time \n\n"
    )


def test_text_line():
    assert (
        markdown_elements.text_line("A text to be written") == "A text to be written \n"
    )


def test_item_line_unordered():
    assert (
        markdown_elements.item_line("A text to be written", 2)
        == "    - A text to be written \n"
    )


def test_item_prefix():
    assert markdown_elements._item_prefix(1, 0, 0, str) == "  1. "
    assert markdown_elements._item_prefix(1, 1, 0, str) == "     - "
    assert markdown_elements._item_prefix(1, 0, 0, dict) == "  1. - "
    assert markdown_elements._item_prefix(1, 0, 1, dict) == "     - "
    assert markdown_elements._item_prefix(1, 1, 1, dict) == "     - "


def test_multitype_list_and_sublist():
    assert markdown_elements.multitype_list(
        ["item1", "item2", ["item3", "item4"], [[1, 2, 3], [4, 5]]]
    ) == (
        "  1. item1 \n"
        "  1. item2 \n"
        "     - item3 \n"
        "     - item4 \n"
        "       - 1 \n"
        "       - 2 \n"
        "       - 3 \n"
        "       - 4 \n"
        "       - 5 \n\n"
    )


def test_multitype_dict_single_item():
    assert markdown_elements.multitype_list([{"k": "v"}]) == ("  1. - k: v \n\n")


def test_multitype_dict_simple_items():
    assert markdown_elements.multitype_list([{"a": 1, "b": True}]) == (
        "  1. - a: 1 \n" "     - b: True \n\n"
    )


def test_multitype_dict_of_simple_dict_items_1():
    assert markdown_elements.multitype_list([{"c": {"q": "q"}}]) == (
        "  1. - c: \n" "       - q: q \n\n"
    )


def test_multitype_dict_of_simple_dict_items_2():
    assert markdown_elements.multitype_list([{"d": {"w": "w", "x": "x"}}]) == (
        "  1. - d: \n" "       - w: w \n" "       - x: x \n\n"
    )


def test_multitype_dict_of_dict_of_simple_dict_items():
    assert markdown_elements.multitype_list([{"d": {"w": {"z": "z"}, "x": "x"}}]) == (
        "  1. - d: \n" "       - w: \n" "         - z: z \n" "       - x: x \n\n"
    )


def test_multitype_dict_of_dict_of_list():
    assert markdown_elements.multitype_list(
        [{"e": ["e1", "e2", {"e3": [1, 2, 3]}, "e4"]}]
    ) == (
        "  1. - e: \n"
        "       - e1 \n"
        "       - e2 \n"
        "       - e3: \n"
        "         - 1 \n"
        "         - 2 \n"
        "         - 3 \n"
        "       - e4 \n\n"
    )


def test_multitype_dict_multiple_items():
    assert markdown_elements.multitype_list(
        [
            {
                "a": 1,
                "b": True,
                "c": {"q": "q"},
                "d": {"w": "w", "x": "x"},
                "e": ["e1", "e2", {"e3": [1, 2, {"z": 3}]}, "e4"],
            }
        ]
    ) == (
        "  1. - a: 1 \n"
        "     - b: True \n"
        "     - c: \n"
        "       - q: q \n"
        "     - d: \n"
        "       - w: w \n"
        "       - x: x \n"
        "     - e: \n"
        "       - e1 \n"
        "       - e2 \n"
        "       - e3: \n"
        "         - 1 \n"
        "         - 2 \n"
        "         - z: 3 \n"
        "       - e4 \n\n"
    )


def test_multitype_list():
    assert markdown_elements.multitype_list(
        [
            "item1",
            "item2",
            ["item3", "item4"],
            {"k": "v"},
            {
                "a": 1,
                "b": True,
                "c": {"q": "q"},
                "d": {"w": "w", "x": "x"},
                "e": ["e1", "e2", {"e3": [1, 2, 3]}, "e4"],
            },
        ]
    ) == (
        "  1. item1 \n"
        "  1. item2 \n"
        "     - item3 \n"
        "     - item4 \n"
        "  1. - k: v \n"
        "  1. - a: 1 \n"
        "     - b: True \n"
        "     - c: \n"
        "       - q: q \n"
        "     - d: \n"
        "       - w: w \n"
        "       - x: x \n"
        "     - e: \n"
        "       - e1 \n"
        "       - e2 \n"
        "       - e3: \n"
        "         - 1 \n"
        "         - 2 \n"
        "         - 3 \n"
        "       - e4 \n\n"
    )


def test_item_line_ordered():
    assert (
        markdown_elements.item_line("A text to be written", 2, mode="ordered")
        == "    1. A text to be written \n"
    )


def test_unordered_list():
    assert (
        markdown_elements.unordered_list(
            ["A text to be written", "And a second item"],
        )
        == "  - A text to be written \n  - And a second item \n\n"
    )


def test_ordered_list():
    assert (
        markdown_elements.ordered_list(
            ["A text to be written", "And a second item"],
        )
        == "  1. A text to be written \n  1. And a second item \n\n"
    )


def test_two_columns_table_row():
    assert (
        markdown_elements.two_columns_table_row("First", "Second")
        == "| First | Second |\n"
    )
    assert (
        markdown_elements.two_columns_table_row("First", ["Second", "Third"])
        == "| First | Second; Third |\n"
    )
    assert (
        markdown_elements.two_columns_table_row("First", ["Second"])
        == "| First | Second |\n"
    )
    assert markdown_elements.two_columns_table_row("First", []) == "| First | - |\n"
    assert markdown_elements.two_columns_table_row("First", [None]) == "| First | - |\n"
    assert markdown_elements.two_columns_table_row("First", None) == "| First | - |\n"
    assert markdown_elements.two_columns_table_row("First", "") == "| First | - |\n"


def test_two_columns_table_no_filter():
    data = {"a": 1, "b": 2, "c": 3}
    assert markdown_elements.two_columns_table(data) == (
        "\n" "|||\n" "|:---|---:|\n" "| a | 1 |\n" "| b | 2 |\n" "| c | 3 |\n" "\n"
    )


def test_two_columns_table_with_filter():
    data = {"a": 1, "b": 2, "c": 3}
    assert markdown_elements.two_columns_table(data, ["b"]) == (
        "\n" "|||\n" "|:---|---:|\n" "| b | 2 |\n" "\n"
    )


def test_table_section():
    assert markdown_elements.table_section(
        2, ("Title", None), {"a": 1, "b": 2, "c": 3}, "The table below is nice"
    ) == (
        "## Title\n\n"
        "The table below is nice \n"
        "\n"
        "|||\n"
        "|:---|---:|\n"
        "| a | 1 |\n"
        "| b | 2 |\n"
        "| c | 3 |\n"
        "\n"
        "\n"
    )


def test_table_section_no_text():
    assert markdown_elements.table_section(
        2,
        ("Title", "None"),
        {"a": 1, "b": 2, "c": 3},
    ) == (
        "## Title: None \n\n"
        "\n"
        "|||\n"
        "|:---|---:|\n"
        "| a | 1 |\n"
        "| b | 2 |\n"
        "| c | 3 |\n"
        "\n"
        "\n"
    )
