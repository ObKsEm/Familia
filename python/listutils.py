# -*- coding: utf-8 -*-


def is_empty(items):
    return items is None or len(items) == 0


def cycle(iterable):
    saved = []
    for element in iterable:
        yield element
        saved.append(element)
    while saved:
        for element in saved:
            yield element


def remove_from_list(target_list: list, removal_list: list):
    if target_list is None or len(target_list) == 0 or removal_list is None or len(removal_list) == 0:
        return target_list
    return list(set(target_list) - set(removal_list))
