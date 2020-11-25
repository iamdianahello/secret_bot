import re


# print (u'\u0441\u2064\u2063\u0441\u0438\u044f')
# strrr = 'с⁤⁣сия'
# print(list('Hello World!'.encode('utf8')))


def decimal_to_binary(decimal_int):
    return(bin(int(decimal_int))[2::])


def binary_to_decimal(binary_int):
    return(int(binary_int, 2))


def encode_string_to_int(input_string):
    mybytes = input_string.encode('utf-8')
    myint = int.from_bytes(mybytes, 'little')
    return(myint)


def decode_int_to_string(input_int):
    recoveredbytes = input_int.to_bytes((input_int.bit_length() + 7) // 8, 'little')
    recoveredstring = recoveredbytes.decode('utf-8')
    return(recoveredstring)


def create_message_with_hidden_part(cover_message, really_secret_message):
    decimal_secret_symbols = encode_string_to_int(really_secret_message)
    binary_secret_symbols = decimal_to_binary(decimal_secret_symbols)
    hidden_part = binary_secret_symbols.replace('0', u'\u2063').replace('1', u'\u2064') 
    if len(cover_message) > 1:
        combo_message = cover_message[:1] + hidden_part + cover_message[1:]
    else:
        combo_message = '=' + hidden_part + ')'
    return(combo_message)


def get_secret_message(cover_message):
    secret_symbols = (u'\u2064\u2063')
    reg = re.compile('[^' + secret_symbols + ']')
    secret_symbols_from_cover_message = reg.sub('', cover_message)
    if len(secret_symbols_from_cover_message) == 0:
        return('')
    else:
        binary_secret_symbols = secret_symbols_from_cover_message.replace(u'\u2063', '0').replace(u'\u2064', '1')
        decimal_secret_symbols = binary_to_decimal(binary_secret_symbols)
        final_secret_message = decode_int_to_string(decimal_secret_symbols)
        return(final_secret_message)


# visible_message = create_message_with_hidden_part('nice day', 'hahahah lol')
# print(visible_message)
# secret = get_secret_message(visible_message)
# print(secret)


if __name__ == "__main__":
    print(create_message_with_hidden_part('mmm', 'jjjjj'))
