#### Transaction Codes

The transaction code identifies a transaction as a debit or credit – and indicates the type of account to which the transaction is intended (i.e. checking or savings). The transaction code is a mandatory numeric field for the Entry Detail Record (‘6’) and is in positions 02-03.

CHECKING (DDA) ACCOUNTS	SAVINGS ACCOUNTS

22 – Credit	32 – Credit
23 – Credit Prenote	33 – Credit Prenote
27 – Debit	37 – Debit
28 – Debit Prenote	38 – Debit Prenote
For a full list of transaction codes, please refer to Appendix Three, Subpart 3.2 – Glossary of Data Elements the Rules.

#### Service Class Codes

The Service Class Code identifies whether the batch contains both debit and credit transactions, only credit transactions, or only debit transactions. The Service Class Code is a mandatory numeric field for the Batch Header Record (‘5’) and the Batch Control Record (‘8’). The codes are in positions 02-04 in both records, and the code values within a single batch must be the same.

200 – Mixed Debits and Credits
220 – Credits only
225 – Debits only
