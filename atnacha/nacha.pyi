import datetime
from dataclasses import dataclass

@dataclass
class NACHAFile:
    priority_code: int = ...
    immediate_destination: str = ...
    immediate_origin: str = ...
    file_creation_date: datetime.date = ...
    file_creation_time: datetime.time = ...
    file_id_modifier: str = ...
    blocking_factor: int = ...
    format_code: int = ...
    immediate_destination_name: str = ...
    immediate_origin_name: str = ...
    reference_code: str = ...
    batches: list = ...
    @property
    def record_size(self) -> int: ...
    @property
    def block_count(self) -> int: ...
    @property
    def entry_addenda_account(self) -> int: ...
    @property
    def entry_hash(self) -> str: ...
    @property
    def total_credit(self) -> int: ...
    @property
    def total_debit(self) -> int: ...
    @property
    def header(self) -> str: ...
    @property
    def control(self) -> str: ...
    def batch_number(self, batch: ACHBatch) -> str: ...
    def __call__(self) -> str: ...
    def __init__(
        self,
        priority_code=...,
        immediate_destination=...,
        immediate_origin=...,
        file_creation_date=...,
        file_creation_time=...,
        file_id_modifier=...,
        blocking_factor=...,
        format_code=...,
        immediate_destination_name=...,
        immediate_origin_name=...,
        reference_code=...,
        batches=...,
    ) -> None: ...

@dataclass
class ACHBatch:
    service_class_code: int = ...
    company_name: str = ...
    company_discretionary_data: str = ...
    company_id: str = ...
    standard_class_code: str = ...
    company_entry_description: str = ...
    company_descriptive_date: str = ...
    effective_entry_date: datetime.date = ...
    settlement_date: str = ...
    originator_status_code: str = ...
    originating_dfi_id: str = ...
    entries: list = ...
    @property
    def header(self) -> str: ...
    @property
    def control(self) -> str: ...
    @property
    def total_credit(self) -> int: ...
    @property
    def total_debit(self) -> int: ...
    @property
    def entry_hash(self) -> str: ...
    def trace_number(self, entry) -> str: ...
    def __call__(self, batch_number: int = 1) -> str: ...
    def __init__(
        self,
        service_class_code=...,
        company_name=...,
        company_discretionary_data=...,
        company_id=...,
        standard_class_code=...,
        company_entry_description=...,
        company_descriptive_date=...,
        effective_entry_date=...,
        settlement_date=...,
        originator_status_code=...,
        originating_dfi_id=...,
        entries=...,
    ) -> None: ...

@dataclass
class ACHEntry:
    transaction_code: int = ...
    receiving_dfi_identification: str = ...
    dfi_account_number: str = ...
    amount: int = ...
    individual_id_number: str = ...
    individual_name: str = ...
    discretionary_data: str = ...
    addenda_record_indicator: str = ...
    batch: ACHBatch | None = ...
    @property
    def check_digit(self) -> int: ...
    def __call__(self) -> str: ...
    def __init__(
        self,
        transaction_code=...,
        receiving_dfi_identification=...,
        dfi_account_number=...,
        amount=...,
        individual_id_number=...,
        individual_name=...,
        discretionary_data=...,
        addenda_record_indicator=...,
        batch=...,
    ) -> None: ...
