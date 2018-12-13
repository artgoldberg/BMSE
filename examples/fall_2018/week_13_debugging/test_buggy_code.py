example_data =  dict(
    first = [1],
    third = [3],
    second_n_fourth = [2, 4]
)

import buggy_code

expected = [(1, 'first'), (2, 'second_n_fourth'), (3, 'third'), (4, 'second_n_fourth')]
print(buggy_code.by_year_fn(buggy_code.president_elections))
print(buggy_code.by_year_fn(example_data))

assert buggy_code.by_year_fn(example_data) == expected