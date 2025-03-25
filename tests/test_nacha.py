import datetime
import pytest


from atnacha import ACHEntry, ACHBatch, NACHAFile


@pytest.fixture
def example_entry_0():
    return ACHEntry(
        transaction_code=32,
        receiving_dfi_identification="07200080",
        dfi_account_number="7548332",
        amount=5000,
        individual_id_number="",
        individual_name="Cox, Melissa",
        discretionary_data="",
        addenda_record_indicator=0,
    )


@pytest.fixture
def example_entry_1():
    return ACHEntry(
        transaction_code=22,
        receiving_dfi_identification="07200080",
        dfi_account_number="1254356",
        amount=26294,
        individual_id_number="",
        individual_name="Cox, Melissa",
        discretionary_data="",
        addenda_record_indicator=0,
    )


@pytest.fixture
def example_entry_2():
    return ACHEntry(
        transaction_code=32,
        receiving_dfi_identification="07200091",
        dfi_account_number="45876523",
        amount=10000,
        individual_id_number="",
        individual_name="Holden, Max",
        discretionary_data="",
        addenda_record_indicator=0,
    )


@pytest.fixture
def example_entry_3():
    return ACHEntry(
        transaction_code=32,
        receiving_dfi_identification="07200080",
        dfi_account_number="954632",
        amount=2500,
        individual_id_number="",
        individual_name="Porter, Jack S",
        discretionary_data="",
        addenda_record_indicator=0,
    )


@pytest.fixture
def example_entry_4():
    return ACHEntry(
        transaction_code=32,
        receiving_dfi_identification="07200080",
        dfi_account_number="9875342",
        amount=2799,
        individual_id_number="",
        individual_name="Porter, Jack S",
        discretionary_data="",
        addenda_record_indicator=0,
    )


@pytest.fixture
def example_entry_5():
    return ACHEntry(
        transaction_code=32,
        receiving_dfi_identification="27248012",
        dfi_account_number="857654324",
        amount=14919,
        individual_id_number="",
        individual_name="Good, Rhonda",
        discretionary_data="",
        addenda_record_indicator=0,
    )


@pytest.fixture
def example_entry_6():
    return ACHEntry(
        transaction_code=22,
        receiving_dfi_identification="27248012",
        dfi_account_number="87543",
        amount=44759,
        individual_id_number="",
        individual_name="Good, Rhonda",
        discretionary_data="",
        addenda_record_indicator=0,
    )


@pytest.fixture
def example_entry_7():
    return ACHEntry(
        transaction_code=22,
        receiving_dfi_identification="00306102",  # check_digit == 10, should modulus to 0
        dfi_account_number="5239465",
        amount=39059,
        individual_id_number="",
        individual_name="Dunn, John",
        discretionary_data="",
        addenda_record_indicator=0,
    )


@pytest.fixture
def example_entry_8():
    return ACHEntry(
        transaction_code=27,
        receiving_dfi_identification="072000915",  # with check_digit value of 5,
        dfi_account_number="723458745",
        amount=145330,
        individual_id_number="",
        individual_name="Anderson Enterprises Incorporated",
        discretionary_data="",
        addenda_record_indicator=0,
    )


@pytest.fixture
def example_batch_0(
    example_entry_0,
    example_entry_1,
    example_entry_2,
    example_entry_3,
    example_entry_4,
    example_entry_5,
    example_entry_6,
    example_entry_7,
    example_entry_8,
):
    return ACHBatch(
        service_class_code=200,
        company_name="Anderson Enterprises Incorporated",
        company_discretionary_data="",
        company_id="1381655417",
        standard_class_code="PPD",
        company_entry_description="PAYROLL",
        company_descriptive_date=None,
        effective_entry_date=datetime.date(2002, 11, 13),  # 021113
        settlement_date=None,
        originator_status_code=1,
        originating_dfi_id="072000916",
        entries=[
            example_entry_0,
            example_entry_1,
            example_entry_2,
            example_entry_3,
            example_entry_4,
            example_entry_5,
            example_entry_6,
            example_entry_7,
            example_entry_8,
        ],
    )


@pytest.fixture
def example_nacha_0(example_batch_0):
    return NACHAFile(
        priority_code=1,
        immediate_destination="072000915",
        immediate_origin="072000915",
        file_creation_date=datetime.date(2002, 4, 4),
        file_creation_time=datetime.datetime(2002, 4, 4, 12, 9, 0),
        file_id_modifier="0",
        blocking_factor=10,
        format_code=1,
        immediate_destination_name="First National Bank",
        immediate_origin_name="First National Bank",
        reference_code="",
        batches=[example_batch_0],
    )


def test_entry_str(
    example_entry_0,
    example_entry_1,
    example_entry_2,
    example_entry_3,
    example_entry_4,
    example_entry_5,
    example_entry_6,
    example_entry_7,
    example_entry_8,
):
    output_0 = "6320720008057548332          0000005000               Cox, Melissa            0"
    output_1 = "6220720008051254356          0000026294               Cox, Melissa            0"
    output_2 = "63207200091545876523         0000010000               Holden, Max             0"
    output_3 = "632072000805954632           0000002500               Porter, Jack S          0"
    output_4 = "6320720008059875342          0000002799               Porter, Jack S          0"
    output_5 = "632272480128857654324        0000014919               Good, Rhonda            0"
    output_6 = "62227248012887543            0000044759               Good, Rhonda            0"
    output_7 = "6220030610205239465          0000039059               Dunn, John              0"
    output_8 = "627072000915723458745        0000145330               Anderson Enterprises I  0"
    assert output_0 == str(example_entry_0)
    assert output_1 == str(example_entry_1)
    assert output_2 == str(example_entry_2)
    assert output_3 == str(example_entry_3)
    assert output_4 == str(example_entry_4)
    assert output_5 == str(example_entry_5)
    assert output_6 == str(example_entry_6)
    assert output_7 == str(example_entry_7)
    assert output_8 == str(example_entry_8)


def test_batch_header(example_batch_0):
    output_0 = "5200Anderson Enterpr                    1381655417PPDPAYROLL   000000021113   107200091"
    assert output_0 == example_batch_0.header


def test_batch_control(example_batch_0):
    output_0 = "820000000900980026280000001453300000001453301381655417                         07200091"
    assert example_batch_0.entry_hash == "0098002628"
    assert example_batch_0.total_credit == 145330
    assert example_batch_0.total_debit == 145330
    assert output_0 == example_batch_0.control


def test_ach_header(example_nacha_0):
    output_0 = "101 072000915 07200091502040412090094101First National Bank    First National Bank            "
    assert output_0 == example_nacha_0.header


def test_ach_control(example_nacha_0):
    output_0 = "9000001000002000000090098002628000000145330000000145330                                       "
    assert example_nacha_0.entry_hash == "0098002628"
    assert example_nacha_0.total_credit == 145330
    assert example_nacha_0.total_debit == 145330
    assert output_0 == example_nacha_0.control


complete_nacha_0 = """101 072000915 07200091502040412090094101First National Bank    First National Bank
5200Anderson Enterpr                    1381655417PPDPAYROLL   000000021113   1072000910000001
6320720008057548332          0000005000               Cox, Melissa            0072000910000001
6220720008051254356          0000026294               Cox, Melissa            0072000910000002
63207200091545876523         0000010000               Holden, Max             0072000910000003
632072000805954632           0000002500               Porter, Jack S          0072000910000004
6320720008059875342          0000002799               Porter, Jack S          0072000910000005
632272480128857654324        0000014919               Good, Rhonda            0072000910000006
62227248012887543            0000044759               Good, Rhonda            0072000910000007
6220030610205239465          0000039059               Dunn, John              0072000910000008
627072000915723458745        0000145330               Anderson Enterprises I  0072000910000009
820000000900980026280000001453300000001453301381655417                         072000910000001
9000001000002000000090098002628000000145330000000145330
9999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999
9999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999
9999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999
9999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999
9999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999
9999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999
9999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999
9999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999""
"""
