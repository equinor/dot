"""
Module defining low level markdown basic elements
"""
from collections.abc import Iterable
from typing import Any


one_newline = "\n"
two_newlines = one_newline + one_newline
double_blank_end = "  \n"
ordered_symbol ="1. "
unordered_symbol = "- "

def _header_tag(level: int)->str:
    """Create a markdown section tag

    Args:
        level (int): The level of the section

    Returns:
        str: the markdwon tag for the section. This a `#` per level.
    """
    return f"{'#'*(level)}"


def header(level: int, prefix: str, data: str = None) -> str:
    """create a section header

    Args:
        level (int): Level of section (1 begin the document title)
        prefix (str): A prefix to the header
        data (str, optional): Data to eventually disaply after the prefix.
        Defaults to None.

    Returns:
        str: A markdown section header finishing by 2 new lines
    """
    hdr =  f"{_header_tag(level)} {prefix}"
    if data:
        hdr += f": {data.strip()} "
    hdr += two_newlines
    return hdr


def text_line(data: str) -> str:
    """Create some text finishing by a new line

    Args:
        data (str): Some text

    Returns:
        str: Input text with an addiciotnal new line
    """
    return f"{data.strip()} {one_newline}"


def _list_symbol(mode: str) -> str:
    """Select bullet symbol for list

    Args:
        mode (str): "unordered" or "ordered" list

    Returns:
        str: "-" for unordered lists, "1." for ordered ones
    """
    if mode == "unordered":
        symbol = unordered_symbol
    if mode == "ordered":
        symbol = ordered_symbol
    return symbol


def _parse_simple_type(
        data: str | int | float | complex | bool,
        indent: int,
        level: int,
        rank: int,
        parent
) -> str:
    """parse data for single line item of a list

    Args:
        data (str | int | float | complex | bool): line content
        indent (int): indentation level (2 blanks per level)
        level (int): level of sub-list (0 being the main list)
        rank (int): rank of the item within the list or sub-list
        parent: type of the object where the item lies

    Returns:
        str: the parsed data content
    """
    text = f"{data} {one_newline}"
    if parent is dict:
        return text
    prefix = _item_prefix(indent, level, rank, parent)
    return f"{prefix}{text}"


def _parse_sequence(
        data: tuple | list,
        indent: int,
        level: int,
        rank: int,
        parent
) -> str:
    """parse sequence data

    Args:
        data (list | tuple): line content
        indent (int): indentation level (2 blanks per level)
        level (int): level of sub-list (0 being the main list)
        rank (int): rank of the item within the list or sub-list
        parent: type of the object where the item lies

    Returns:
        str: the parsed data content
    """
    return "".join(
        _parse_multitype_item(
            subitem,
            indent,
            level+1,
            rank=count,
            parent=list
            )
            for count, subitem in enumerate(data)
            )


def _parse_single_item_dict(
        data: dict,
        indent: int,
        level: int,
        rank: int,
        parent
) -> str:
    """parse single element dictionary data

    Args:
        data (dict): line content
        indent (int): indentation level (2 blanks per level)
        level (int): level of sub-list (0 being the main list)
        rank (int): rank of the item within the list or sub-list
        parent: type of the object where the item lies

    Returns:
        str: the parsed data content
    """
    md = ""
    key = list(data.keys())[0]
    value = list(data.values())[0]
    if isinstance(value, str | int | float | complex | bool):
        value_str = _parse_multitype_item(value, indent, level, rank, dict)
        value_str = f"{value_str}"
    else:
        value_str = _parse_multitype_item(value, indent, level+1, rank, parent)
        value_str = f"{one_newline}{value_str}"
    prefix = _item_prefix(indent, level, rank, dict)
    md += f"{prefix}{key}: {value_str}"
    # if level <= 1:
    #     md += f"{blanks}{ordered_symbol}{unordered_symbol}{key}: {value_str}"
    # else:
    #     # md += f"{blanks}{' '*len(symbol)}{unordered_symbol}{key}: {value_str}"
    #     md += f"{blanks}{unordered_symbol}{key}: {value_str}"
    return md


def _parse_dict(
        data: dict,
        indent: int,
        level: int,
        rank: int,
        parent
) -> str:
    """parse dictionary data

    Args:
        data (dict): line content
        indent (int): indentation level (2 blanks per level)
        level (int): level of sub-list (0 being the main list)
        rank (int): rank of the item within the list or sub-list
        parent: type of the object where the item lies

    Returns:
        str: the parsed data content
    """
    return "".join(
        _parse_multitype_item(
            {item[0]: item[1]},
            indent,
            level+1,
            rank=count,
            parent=parent
            )
            for count, item in enumerate(data.items())
            )


def _item_prefix(indent: int, level: int, rank: int, parent) -> str:
    """Make the prefix of the list item

    Args:
        indent (int): indentation level (2 blanks per level)
        level (int): level of sub-list (0 being the main list)
        rank (int): rank of the item within the list or sub-list
        parent: type of the object where the item lies

    Returns:
        str: the prefix of the markdown line
    """
    prefix = ' '*(indent*2)
    if level == 0:
        prefix += ordered_symbol
        if parent is dict:
            prefix += unordered_symbol
    if level == 1:
        if rank == 0 and parent is not list:
            prefix += ordered_symbol+unordered_symbol
        else:
            prefix += ' '*(level*2)+' '+unordered_symbol
    if level > 1:
        prefix += ' '*(level*2)+' '+unordered_symbol
    return prefix


def _parse_multitype_item(item, indent: int, level: int, rank: int, parent) -> str:

    if isinstance(item, str | int | float | complex | bool):
        return _parse_simple_type(item, indent, level, rank, parent)
    
    if isinstance(item, list):
        return _parse_sequence(item, indent, level, rank, parent)
    
    if isinstance(item, dict) and len(item) <= 1:
        return _parse_single_item_dict(item, indent, level, rank, parent)

    if isinstance(item, dict) and len(item) > 1:
        return _parse_dict(item, indent, level, rank, parent)
    

def multitype_list(data: list, indent=1) -> str:
    return "".join(
        _parse_multitype_item(
            item,
            indent,
            level=0,
            rank=count,
            parent=list
            )
            for count, item in enumerate(data)
            )


def item_line(data: str, indent=1, mode="unordered") -> str:
    """Add some an item line

    The item can be for unorderd or ordered lists or for 

    Args:
        data (str): Text of list item.
        indent (int, optional): Indent of the item. Defaults to 1.
        mode (str, optional): Unordered or ordered (list). Defaults to "unordered".

    Returns:
        str: An item text finishing by a new line.
        The indent value is multiplied by two. This means the default value is 2 spaces.

    """
    symbol = _list_symbol(mode)
    text = f"{data}".strip()
    return f"{' '*(indent*2)}{symbol}{text} {one_newline}"


def unordered_list(items: list | tuple, indent=1) -> str:
    """Make an unordered list

    Args:
        items (list | tuple): Items to list
        indent (int, optional): Indent of the item. Defaults to 1.
        Use for example 2 for sublists

    Returns:
        str: A markdown representation of an unordered list
    """
    unordered_list = "".join(
        [item_line(k, indent=indent, mode="unordered") for k in items]
        )
    unordered_list += one_newline
    return unordered_list


def ordered_list(items: list | tuple, indent=1) -> str:
    """Make an ordered list

    Args:
        items (list | tuple): Items to list
        indent (int, optional): Indent of the item. Defaults to 1.
        Use for example 2 for sublists

    Returns:
        str: A markdown representation of an ordered list
    """
    ordered_list = "".join(
        [item_line(k, indent=indent, mode="ordered") for k in items]
        )
    ordered_list += one_newline
    return ordered_list


def two_columns_table_row(key: str, value: Any) -> str:
    """Create a row in a 2-columns table 

    Args:
        key (str): Text in first column
        value (Any): Value in the second column

    Returns:
        str: a markdown description of a 2-columns table row
    """
    if isinstance(value, Iterable) and not isinstance(value, str):
        if not value:
            value_str = " - "
        elif len(value) == 1:
            if not value[0]:
                value_str = " - "
            else:
                value_str = str(value[0])
        else:
            value_str = "; ".join([str(v) for v in value])
    elif value == "" or value is None:
        value_str = " - "
    else:
        value_str = str(value)
    key_without_blanks = key.replace('_', ' ')
    key_without_blanks = key_without_blanks.strip()
    value_str = value_str.strip()
    return f"| {key_without_blanks} | {value_str} |{one_newline}"


def two_columns_table(data: dict, filter_keys: list = None) -> str:
    """Create a 2-columns table based on key/value pairs

    Args:
        data (dict): Key/Value pairs
        filter_keys (list, optional): List of keys from data to include. 
        Defaults to None, meaning all keys are taken.

    Returns:
        str: A markdown representation of a 2-columns table
    """
    md = one_newline
    md += f"|||{one_newline}"
    md += f"|:---|---:|{one_newline}"
    if filter_keys is None:
        md += "".join(
            [two_columns_table_row(key, value) for key, value in data.items()]
            )
    else:
        md += "".join(
            [
                two_columns_table_row(key, value)
                for key, value in data.items()
                if key in filter_keys
            ]
        )
    md += one_newline
    return md


def table_section(
        level: int,
        header_data: list | tuple,
        data: dict,
        text: str = None,
        filter_keys: list = None
        ) -> str:
    """Create a section containing some text and a 2-columns table

    Args:
        level (int): Level of section (1 begin the document title)
        header_data(list | tuple): data to use for the header. 2-element list or
        tuple, the first being the prefix, the second one some extra data. If the
        second element is None, it is not used.
        data (dict): Key/Value pairs to set in the table
        text (str, optional): Some text before the table
        filter_keys (list, optional): List of keys from data to include. 
        Defaults to None, meaning all keys are taken.

    Returns:
        str: A markdown representation of a section with text and table.
    """
    md = ""
    md += header(level, header_data[0], header_data[1])
    if text:
        md += text_line(text)
    md += two_columns_table(data, filter_keys=filter_keys)
    md += one_newline
    return md
