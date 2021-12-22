from textwrap import dedent
from dataclasses import dataclass, field
import datetime


@dataclass
class NACHAFile:
	record_type_code: int = 1
	priority_code: int = 1
	immediate_destination: str = ''
	immediate_origin: str = ''
	file_creation_date: datetime.date = datetime.date.today()
	file_creation_time: datetime.time = datetime.datetime.now().time()
	file_id_modifier: str = ''
	blocking_factor: int = 0
	format_code: int = 1
	immediate_destination_name: str = ''
	immediate_origin_name: str = ''
	reference_code: str = ''
	batches: list = field(default_factory=list)

	@property
	def record_size(self):
		return sum([[len(entries) for entries in batch.entries] for batch in self.batches])

	def __str__(self):
		# position 1                       2-3                   4-13                             14-23                       24-29                                     30-33                                   34                     35-37                 38-39                   40                 41-63                            64-86                       87-94                
		return f"""{self.record_type_code}{self.priority_code:02}{self.immediate_destination: >10}{self.immediate_origin: >10}{self.file_creation_date.strptime('%y%m%d')}{self.file_creation_time.strptime('%H%M')}{self.file_id_modifier}{self.record_size:003}{self.blocking_factor:02}{self.format_code}{self.immediate_destination_name}{self.immediate_origin_name}{self.reference_code}"""

	def __call__(self):
		return '\n'.join(f'{batch()}' for batch in self.batches)


@dataclass
class ACHBatch:
	record_type_code: int = 5
	service_class_code: int = 0
	company_name: str = ''
	company_discretionary_data: str = ''
	company_id: str = ''
	standard_class_code: str = ''
	company_entry_description: str = ''
	company_descriptive_date: str = ''
	effective_entry_date: datetime.date = datetime.date.today()
	settlement_date: str = ''
	originator_status_code: str = ''
	originiating_dfi_id: str = ''
	batch_number: int = 1
	entries: list = field(default_factory=list)

	def __str__(self):
		company_descriptive_date = self.company_descriptive_date if self.company_descriptive_date else "      "
		settlement_date = self.settlement_date if self.settlement_date else "   "
		# position 1                       2-4                        5-20                    21-40                                 41-50                 51-53                        64-69                                           70-75                                       76-78                 79                           80-87                     88-94
		return f"""{self.record_type_code}{self.service_class_code}{self.company_name: <16}{self.company_discretionary_data: <20}{self.company_id: <10}{self.standard_class_code: <3}{self.company_entry_description: <10}{company_descriptive_date}{self.effective_entry_date.strftime('%y%m%d')}{settlement_date}{self.originator_status_code}{self.originiating_dfi_id}{self.batch_number:07}"""
	
	def __repr__(self):
		return self.__str__()

	def __call__(self):
		return '\n'.join(f'{entry}' for entry in self.entries)


@dataclass
class ACHEntry:
	record_type_code: int = 6
	transaction_code: int = 0
	receiving_dfi_identification: str = ''
	check_digit: int = 0
	dfi_account_number: str = ''
	amount: int = 0 # in cents
	individual_id_number: str = ''
	individual_name: str = ''
	discretionary_data: str = ''
	addenda_record_indicator: str = ''
	trace_number: int = 0

	def __str__(self):
		# position 1                      2-3                        4-11                              12                13-29                          30-39           40-54                           55-76                        77-78                        79                             80-94
		return f"""{self.record_type_code}{self.transaction_code:02}{self.receiving_dfi_identification[0:8]}{self.check_digit}{self.dfi_account_number: <17}{self.amount:010}{self.individual_id_number: <15}{self.individual_name[0:22]: <22}{self.discretionary_data: <2}{self.addenda_record_indicator}{self.trace_number}"""
		
	def __repr__(self):
		return self.__str__()

	def __call__(self):
		return self.__str__()
