def is_data_contains_element(self: list, element):
    for i in range(len(self)):
        if self[i] == element:
            return True
    return False
