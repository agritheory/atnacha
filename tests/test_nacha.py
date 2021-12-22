import datetime
import pytest

from nacha import ACHEntry, ACHBatch, NACHAFile

@pytest.fixture
def example_entry_0():
	return ACHEntry(
		record_type_code=6,
		transaction_code=22,
		receiving_dfi_identification='11234567',
		check_digit=8,
		dfi_account_number='1123456789',
		amount=12345,
		individual_id_number='98789789',
		individual_name='TEST CREDIT 1',
		discretionary_data='',
		addenda_record_indicator=0,
		trace_number=127372060000001
	)

@pytest.fixture
def example_entry_1():
	return ACHEntry(
		record_type_code=6,
		transaction_code=22,
		receiving_dfi_identification='13154134',
		check_digit=8,
		dfi_account_number='1312545400',
		amount=145,
		individual_id_number='12312312',
		individual_name='TEST CREDIT 2',
		discretionary_data='',
		addenda_record_indicator=0,
		trace_number=127372060000002
	)

# @pytest.fixture
def example_batch_0(example_entry_0, example_entry_1):
	return ACHBatch(
		record_type_code=5,
		service_class_code=200,
		company_name='ALALALAD',
		company_discretionary_data='ACH SETTLEMENT',
		company_id='2273720697',
		standard_class_code='PPD',
		company_entry_description='PAYOUTS',
		company_descriptive_date=None,
		effective_entry_date=datetime.date(2013, 1, 16),
		settlement_date=None,
		originator_status_code=1,
		originiating_dfi_id=12737206,
		batch_number=1,
	)


def test_entry_str(example_entry_0, example_entry_1):
	output_0 = '6221123456781123456789       000001234598789789       TEST CREDIT 1           0127372060000001'
	output_1 = '6221315413481312545400       000000014512312312       TEST CREDIT 2           0127372060000002'
	assert output_0 == example_entry_0()
	assert output_1 == example_entry_1()


def test_batch_str(example_batch_0):
	output_0 = '5200ALALALAD        ACH SETTLEMENT      2273720697PPDPAYOUTS         130116   1127372060000001'
	assert output_0 == str(example_batch_0)


def test_ach_header():
	pass


def test_ach_footer():
	pass


def test_complete_nacha_file():
	pass