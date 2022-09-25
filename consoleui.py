"""
This module provides functions that are useful for interacting with a user on a console.
"""


def input_integer(prompt_msg):
    """
        Prompt for integer input and return the integer value entered by the user
    Args:
        prompt_msg: a string value displayed as a prompt

    Returns:
        the int value entered by the user in response to the prompt
    """
    response = input(prompt_msg).strip()
    while not response.isdigit():
        print('  *** Enter an integer value. ***')
        response = input(prompt_msg).strip()

    return int(response)


def input_integer_between(prompt_msg, lo, hi):
    """
    Prompt for integer input between tow int values and return the integer value
    meeting those constraints entered by the user
    Args:
        prompt_msg: a string value displayed as a prompt
        lo:         the lowest int value that is acceptable
        hi:         the highest int value that is acceptable, lo < hi

    Returns:
        the int value between lo and hi, inclusive, entered by the user in response
        to the prompt
    """
    response = input_integer(prompt_msg)
    while response < lo or response > hi:
        print(f'  *** Enter an integer value between {lo} and {hi}. ***')
        response = input_integer(prompt_msg)

    return int(response)


def input_menu_selection(options, prompt_msg):
    """
    Present a list of menu options to the user and return the index of the option selected
    Args:
        options:    a non-empty list of menu options
        prompt_msg: a prompt message displayed to ask for an option number

    Returns:
        the index of the option selected by a user
    """
    # Display the list of menu choices, numbered 1, 2, 3, ...
    for option_number, option in enumerate(options, 1):
        print(f'{option_number:2}: {option}')

    # Get a choice from the user
    response = input_integer_between(prompt_msg, 1, len(options))

    return response - 1


if __name__ == '__main__':
    # Call each function and display the value returned
    n = input_integer('Enter a number: ')
    print(f'Return value is {repr(n)}')

    m = input_integer_between('Enter a number between 1 and 10: ', 1, 10)
    print(f'Return value is {repr(m)}')

    colors = ['red', 'blue', 'yellow', 'green', 'other']
    i = input_menu_selection(colors, 'Select your favorite color: ')
    print(f'Return value is {repr(i)}: {repr(colors[i])}')
