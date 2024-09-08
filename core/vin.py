from typing import Annotated

from loguru import logger
from pydantic import AfterValidator

ALLOWED_VIN_LETTERS: str = "ABCDEFGHJKLMNPRSTUVWXYZ"


def translitering_vin_character_to_number(vin_char: str) -> int:
    vin_translate_chars_tuple: tuple = (
        ("AJ", 1),
        ("BKS", 2),
        ("CLT", 3),
        ("DMU", 4),
        ("ENV", 5),
        ("FW", 6),
        ("GPX", 7),
        ("HY", 8),
        ("RZ", 9),
    )
    if vin_char.isdigit():
        return int(vin_char)
    elif vin_char.isalpha():
        for chars, number in vin_translate_chars_tuple:
            if vin_char.upper() in chars:
                return number
    return 0


def vin_checksum_calc(vin_code: str) -> str:
    weights_tuple: tuple = (8, 7, 6, 5, 4, 3, 2, 10, 0, 9, 8, 7, 6, 5, 4, 3, 2)
    transliterated_list: list = [
        translitering_vin_character_to_number(char) for char in vin_code
    ]
    result_numbers_list = [
        translated_number * weight_number
        for translated_number, weight_number in zip(
            transliterated_list, weights_tuple
        )
    ]
    remainder = sum(result_numbers_list) % 11
    if remainder == 10:
        return "X"
    return str(remainder).upper()


def vin_format_checking(vin_code: str) -> bool:
    assert len(vin_code) == 17, f"VIN length must be 17 characters."
    assert all(
        vin_char.isdigit() or vin_char.upper() in ALLOWED_VIN_LETTERS
        for vin_char in vin_code
    ), f"VIN code contains incorrect characters."
    return True


def vin_code_validator(
    vin_code: str, checksum_verification: bool = True
) -> str:
    """Check VIN code format and calculation checksum."""
    assert vin_format_checking(vin_code)
    logger.debug(f"{vin_code}: format is correct.")
    if checksum_verification:
        assert (
            vin_checksum_calc(vin_code) == vin_code[8]
        ), f"VIN checksum is incorrect!"
        logger.debug(f"VIN {vin_code} checksum is correct.")
    return vin_code


VIN_Type = Annotated[str, AfterValidator(vin_code_validator)]
