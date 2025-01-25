import random


def count_1010_occurrences(binary_string):
    count = 0
    for i in range(len(binary_string) - 3):
        if binary_string[i : i + 4] == "1010":
            count += 1
    return count


def generate_binary_string(n):
    # 生成1个长度为n的随机二进制字符串，且包含1010的次数大于等于3
    # binary_string = "".join(random.choice(["0", "1"]) for _ in range(n))
    while True:
        binary_string = "".join(random.choice(["0", "1"]) for _ in range(n))
        if count_1010_occurrences(binary_string) >= 3:
            return binary_string


def generate_binary_string_with_n_1010(n):
    # 生成1个随机二进制字符串
    # 字符串中包含1010的次数为n
    binary_string = ""
    while True:
        binary_string += random.choice(["0", "1"])
        if count_1010_occurrences(binary_string) == n:
            return binary_string


def generate_non_random_binary_string_with_n_1010(n):
    # 生成1个非随机二进制字符串
    # 字符串中包含1010的次数为n
    binary_string = "10" * (n + 1)
    return binary_string


def check_final_state(binary_string):
    # 检查二进制字符串在FSM中的最终状态
    state = 0
    for i in range(len(binary_string)):
        if state == 0:
            if binary_string[i] == "0":
                state = 0
            elif binary_string[i] == "1":
                state = 1
        elif state == 1:
            if binary_string[i] == "0":
                state = 2
            elif binary_string[i] == "1":
                state = 1
        elif state == 2:
            if binary_string[i] == "0":
                state = 0
            elif binary_string[i] == "1":
                state = 3
        elif state == 3:
            if binary_string[i] == "0":
                state = 4
            elif binary_string[i] == "1":
                state = 1
        elif state == 4:
            if binary_string[i] == "0":
                state = 0
            elif binary_string[i] == "1":
                state = 3
    return state


def generate_binary_string_with_final_state(final_state, n):
    # 生成1个长度为n的二进制字符串，且在FSM中的最终状态为final_state
    while True:
        binary_string = generate_binary_string(n)
        if check_final_state(binary_string) == final_state:
            return binary_string


def main():
    # for n in [10, 20, 50, 100000]:
    #     binary_string = generate_binary_string(n)
    #     print(f'std::string input_{n} = "{binary_string}";')

    # for n in [12, 123]:
    #     binary_strings = generate_binary_strings_with_n_1010(n)
    #     print(f"std::vector<std::string> input_with_{n}_1010 = {{")
    #     for i, binary_string in enumerate(binary_strings):
    #         print(f'    "{binary_string}"', end="")
    #         if i < len(binary_strings) - 1:
    #             print(",")
    #         else:
    #             print()
    #     print("};")

    # for n in [1234, 12345]:
    #     binary_strings = generate_non_random_binary_strings_with_n_1010(n)
    #     print(f"std::vector<std::string> non_random_input_with_{n}_1010 = {{")
    #     for i, binary_string in enumerate(binary_strings):
    #         print(f'    "{binary_string}"', end="")
    #         if i < len(binary_strings) - 1:
    #             print(",")
    #         else:
    #             print()
    #     print("};")

    for final_state in range(5):
        binary_string = generate_binary_string_with_final_state(final_state, 50)
        print(count_1010_occurrences(binary_string))
        print(f'std::string input_with_final_state_{final_state} = "{binary_string}";')


if __name__ == "__main__":
    main()
