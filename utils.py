def digits_to_num(arr, bits_in_digit):
    """
    Little endian
    """
    num = 0
    for i in range(len(arr)):
        weight = 2 ** (i * bits_in_digit)
        num += arr[i] * weight
    return num


def num_to_digits(num, bits_in_digit, num_digits):
    """
    Little endian
    """
    temp_num = num
    words = [0] * num_digits
    mask = int('1' * bits_in_digit, base=2)
    for i in range(num_digits):
        words[i] = temp_num & mask
        temp_num = temp_num >> bits_in_digit
    return words
