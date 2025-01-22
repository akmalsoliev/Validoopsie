import narwhals
from narwhals.typing import DTypes

KwargsType = dict[str, object]
"""
KwargsType is an internal use case type alias for a dictionary.
It is a dictionary with string keys and object values. Object can be any type.
"""


class ValidationType(DTypes):
    """ValidoopsieType represents a valid type.

    It can be one of the following:

    - ArrayType: Array type
    - BooleanType: Boolean type
    - CategoryType: Categorical type
    - DateTimeType: Datetime type
    - DateType: Date type
    - DurationType: Duration type
    - EnumType: Enumeration type
    - FloatType: Floating-point type
    - IntegerType: Integer type
    - ObjectType: Object type
    - StringType: String type
    - UIntType: Unsigned integer type
    """


class FloatType(ValidationType, narwhals.Float32, narwhals.Float64, narwhals.Decimal):
    """FloatType represents a floating-point type.

    It can be one of the following:

    - Float32: 32-bit floating-point number
    - Float64: 64-bit floating-point number
    - Decimal: Arbitrary-precision decimal number
    """


class IntType(
    ValidationType,
    narwhals.Int8,
    narwhals.Int16,
    narwhals.Int32,
    narwhals.Int64,
    narwhals.Int128,
):
    """IntType represents an integer type.

    It can be one of the following:

    - Int8: 8-bit signed integer
    - Int16: 16-bit signed integer
    - Int32: 32-bit signed integer
    - Int64: 64-bit signed integer
    - Int128: 128-bit signed integer
    """


class UIntType(
    ValidationType,
    narwhals.UInt8,
    narwhals.UInt16,
    narwhals.UInt32,
    narwhals.UInt64,
    narwhals.UInt128,
):
    """UIntType represents an unsigned integer type.

    It can be one of the following:

    - UInt8: 8-bit unsigned integer
    - UInt16: 16-bit unsigned integer
    - UInt32: 32-bit unsigned integer
    - UInt64: 64-bit unsigned integer
    - UInt128: 128-bit unsigned integer
    """
