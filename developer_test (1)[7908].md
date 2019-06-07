Leap Lending
============
Programming Test - Loan Auction System
--------------------------------------

Requirements:
 - Please complete the following programming exercise. Allow for about 4-6 hours.
 - You must use Python. Only use the standard lib, no third parties. Test code can use common 3rd parties
 - Provide all source code in a zip file.
 - Do not host solution on GitHub.
 - Please produce production-quality code, providing tests and comments where necessary.
 - Provide README file on how to build/run your program


Task
----

Your task is to build an Auction system for a Fintech loan website. Borrowers can put up loan requests,
and Lenders can bid to fulfil them by offering the loan at a lower interest rate.
At the end of each loan auction, if the bids are equal to or less than the reserve rate, the lowest Lender wins.
The lowest lender matches the loan at the rate of the second lowest valid bid.

A bid is valid if and only if:
  - Arrives after the auction start time and before or on the closing time. DONE
  - Is smaller than any previous valid bids submitted by the user. DONE

If there is only 1 bid, then pay the reserve rate of the loan. If there is are equal amounts, earliest bid wins. DONE


Spec
----

The input file contains the start times for loan auctions, bids places. Execute all instructions and output winning bid,
rate matched and user.

Input File
----------

A pipe-delimited input file representing the started auctions, and bids. The
first entry on each line of this file will be a timestamp, the file will be strictly in-order
of timestamp. There are three types of rows found in this file:

1) Borrower listing loan for sale.

This appears in the format:

timestamp|user_id|action|loan_id|credit|reserve_rate|close_time

`timestamp` will be an integer representing a unix epoch time and is the auction start time,
`user_id` is an integer user id
`action` will be the string "SELL"
`loan_id` is a unique string code for that loan.
`credit` is a decimal representing the credit required the borrower
`reserve_rate` is a decimal representing the loans reserve rate
`close_time` will be an integer representing a unix epoch time


2) Lender bids on Loans

This will appear in the format:

timestamp|user_id|action|loan_id|rate

`timestamp` will be an integer representing a unix epoch time and is the time of the bid
`user_id` is an integer user id
`action` will be the string "BID"
`loan_id` is a unique string code for that loan
`rate` is a decimal representing the bidded rate

3) Heartbeat messages

These messages may appear periodically in the input to ensure that auctions can be closed
in the absence of bids, they take the format:

timestamp

`timestamp` will be an integer representing a unix epoch time.


Expected Output:

The program should produce the following expected output, with each line representing the
outcome of a completed auction. This should be written to stdout or a file and be pipe
delimited with the following format:

close_time|loan_id|user_id|status|rate|total_bid_count|highest_rate|lowest_rate

`close_time` should be a unix epoch of the time the auction finished
`loan_id` is the unique string loan code.
`user_id` is the integer id of the winning Lender, or blank if the loan did not sell.
`status` should contain either "SOLD" or "UNSOLD" depending on the auction outcome.
`rate` should be the rate given to the borrower by the auction winner (0.00 if the loan is UNSOLD), as a
number to two decimal places.
`total_bid_count` should be the number of valid bids received for the loan.
'highest_rate' the highest rate received for the loan as a number to two decimal places
`lowest_rate` the lowest rate placed on the loan as a number to two decimal places


Example:

Input:

10|1|SELL|430|42000|0.12|18 
11|8|BID|430|0.20 
13|13|BID|430|0.15 
13|7|SELL|431|32990|0.13|22
17|8|BID|430|0.10
18|1|BID|431|0.15
19|3|BID|431|0.14
20|3|BID|430|0.09 
21|3|BID|431|0.14

Output:

18|430|8|SOLD|0.12|4|0.20|0.10
22|431||UNSOLD|0.00|3|0.15|0.14