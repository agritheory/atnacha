from dataclasses import dataclass, field
import datetime
import math


@dataclass
class NACHAFile:
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
		return 94

	@property
	def block_count(self):
		# The total number of records included in the ACH file, rounded up to the nearest 10, then divided by 10. (08-13) 6 numeric.
		total_entries = sum([len(batch.entries) for batch in self.batches]) + (len(self.batches) * 2) + 2
		return math.ceil(total_entries / 10)

	@property
	def entry_addenda_acount(self):
		return sum([len(batch.entries) for batch in self.batches])

	@property
	def entry_hash(self):
		# The sum of all Entry Hash fields in the ACH file. If the total contains more digits than the field size allows, the number is automatically truncated. (22-31) 10 numeric.
		entry_hash = sum([int(batch.entry_hash) for batch in self.batches])
		entry_hash = str(entry_hash)[len(str(entry_hash)) - 10:] if len(str(entry_hash)) > 10 else str(entry_hash)
		return f"{entry_hash:0>10}"

	@property
	def total_credit(self):
		return sum([batch.total_credit for batch in self.batches])

	@property
	def total_debit(self):
		return sum([batch.total_debit for batch in self.batches])

	@property
	def header(self):
		# position 1 2-3                   4-13                             14-23                       24-29                                     30-33                                   34                     35-37                 38-39                   40                 41-63                            64-86                       87-94                
		return f"""1{self.priority_code:02}{self.immediate_destination: >10}{self.immediate_origin: >10}{self.file_creation_date.strftime('%y%m%d')}{self.file_creation_time.strftime('%H%M')}{self.file_id_modifier}{self.record_size:003}{self.blocking_factor:02}{self.format_code}{self.immediate_destination_name: <23}{self.immediate_origin_name: <23}{self.reference_code: >8}"""
	
	@property
	def control(self):
		# position 1 2-7                   8-13                14-23                       24-29                                     30-33                                   34                     35-37                 38-39                   40                 41-63                            64-86                       87-94                
		return f"""9{len(self.batches):06}{self.block_count:06}{self.entry_addenda_acount:08}{self.entry_hash}{self.total_debit:0>12}{self.total_credit:0>12}{'': >39}"""
	
	def batch_number(self, batch):
		return f"{self.batches.index(batch) + 1:>07}"

	def __str__(self):
		return self()

	def __call__(self):
		output = f"{self.header}\n"
		output += '\n'.join(f'{batch(batch_number=self.batch_number(batch))}' for batch in self.batches)
		output += f"{self.control}\n"
		total_entries = sum([len(batch.entries) for batch in self.batches]) + (len(self.batches) * 2) + 2
		if total_entries !=  self.block_count:
			output += '\n'.join([f"{'':9>94}" for row_fill in range((self.block_count * 10) - total_entries)])
		return output


@dataclass
class ACHBatch:
	service_class_code: int = 200 # 200, 220 or 225
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
	entries: list = field(default_factory=list)

	@property
	def header(self):
		company_descriptive_date = self.company_descriptive_date if self.company_descriptive_date else "000000"
		settlement_date = self.settlement_date if self.settlement_date else "   "
		# position 1 2-4                        5-20                    21-40                                 41-50                 51-53                        64-69                                           70-75                                       76-78                 79                           80-87                     88-94
		return f"""5{self.service_class_code}{self.company_name[:16]: <16}{self.company_discretionary_data: <20}{self.company_id: <10}{self.standard_class_code: <3}{self.company_entry_description: <10}{company_descriptive_date}{self.effective_entry_date.strftime('%y%m%d')}{settlement_date}{self.originator_status_code}{self.originiating_dfi_id}"""

	@property
	def control(self):
		return f"""8{self.service_class_code}{len(self.entries):06}{self.entry_hash}{self.total_debit:0>12}{self.total_credit:0>12}{self.company_id}{"": >19}{"": >6}{self.originiating_dfi_id[:8]}"""

	@property
	def total_credit(self):
		return sum([getattr(entry, 'amount', 0) for entry in self.entries if entry.transaction_code in (22, 23, 24, 32, 33, 34, 52)])

	@property
	def total_debit(self):
		return sum([getattr(entry, 'amount', 0) for entry in self.entries if entry.transaction_code in (27, 28, 29, 37, 38, 39, 53)])

	@property
	def entry_hash(self):
		entry_hash = sum([int(getattr(entry, 'receiving_dfi_identification', 0)[:8]) for entry in self.entries])
		entry_hash = str(entry_hash)[len(str(entry_hash)) - 10:] if len(str(entry_hash)) > 10 else str(entry_hash)
		return f"{entry_hash:0>10}"

	def trace_number(self, entry):
		# A 15-digit number in which positions 1-8 are the first eight digits of the originator's routing number, and positions 9-15 are numbers assigned in ascending order to each transaction within the Company / Batch Header Record. (80-94) 15 numeric.
		return self.originiating_dfi_id + f"{self.entries.index(entry) + 1:>07}"


	def __str__(self):
		return self()

	def __call__(self, batch_number=1):
		output = f"{self.header}{batch_number:0>7}\n"
		output += '\n'.join(f'{entry()}{self.trace_number(entry)}' for entry in self.entries) + "\n"
		output += f"{self.control}{batch_number:0>7}\n"
		return output


@dataclass
class ACHEntry:
	transaction_code: int = 0
	receiving_dfi_identification: str = ''
	check_digit: int = 0
	dfi_account_number: str = ''
	amount: int = 0 # in cents
	individual_id_number: str = ''
	individual_name: str = ''
	discretionary_data: str = ''
	addenda_record_indicator: str = ''
	batch: ACHBatch = None

	def __str__(self):
		# position 1 2-3                      4-11                                    12                13-29                         30-39            40-54                            55-76                           77-78                        79
		return f"""6{self.transaction_code:02}{self.receiving_dfi_identification}{self.check_digit}{self.dfi_account_number: <17}{self.amount:010}{self.individual_id_number: <15}{self.individual_name[0:22]: <22}{self.discretionary_data: <2}{self.addenda_record_indicator}"""

	def __call__(self):
		return self.__str__()


{
	22: "Checking Credit Live",
	23: "Checking Credit Prenote",
	24: "Checking Credit Child Support prenote",
	27: "Checking Debit Live",
	28: "Checking Debit Prenote",
	29: "Checking Debit Child Support prenote",
	32: "Savings Credit Live",
	33: "Savings Credit Prenote",
	34: "Savings Credit Child Support prenote",
	37: "Savings Debit Live",
	38: "Savings Debit Prenote",
	39: "Savings Debit Child Support prenote",
	52: "Loan Credit Live",
	53: "Loan Credit Prenote",
}