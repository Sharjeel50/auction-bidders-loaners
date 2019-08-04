# Parent Class to Inherit from.
class Parent:
    def __init__(self, timestamp, user_id, action, loan_id):
        self.timestamp = timestamp
        self.user_id = user_id
        self.action = action
        self.loan_id = loan_id

# Inherit Parent to reduce code duplication
class Loaner(Parent):
    def __init__(self, timestamp, user_id, action, loan_id, credit, reserve_rate, close_time):
        super().__init__(timestamp, user_id, action, loan_id)
        self.credit = credit
        self.reserve_rate = reserve_rate
        self.close_time = close_time

    # Making Sure i get human readable foramtted objects back
    def __repr__(self):
        return f"Loaner - Timestamp: {self.timestamp}, User ID: {self.user_id}, Action: {self.action}, Loan ID: {self.loan_id}, Credit: {self.credit}, Reserve Date: {self.reserve_rate}, Close Time: {self.close_time}"


class Bidder(Parent):
    def __init__(self, timestamp, user_id, action, loan_id, rate):
        super().__init__(timestamp, user_id, action, loan_id)
        self.rate = rate

    def __repr__(self):
        return f"Bidder - Timestamp: {self.timestamp}, User ID: {self.user_id}, Action: {self.action}, Loan ID: {self.loan_id}, Rate: {self.rate}"


class Results:
    def __init__(self, close_time, loan_id, user_id, status, rate, total_bid_count, highest_rate, lowest_rate):
        self.close_time = close_time
        self.loan_id = loan_id
        self.user_id = user_id
        self.status = status
        self.rate = rate
        self.total_bid_count = total_bid_count
        self.highest_rate = highest_rate
        self.lowest_rate = lowest_rate

    def __repr__(self):
        return f"{self.close_time}|{self.loan_id}|{self.user_id}|{self.status}|{self.rate}|{self.total_bid_count}|{self.highest_rate}|{self.lowest_rate}"


# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


class Auction:
    def __init__(self, file):
        self._bidders_original = []
        self._bidders = []
        # self.total_bid_count = 0  ###REDUNDANT
        self._loaners = []
        self._winners = []
        self.auction_info = {}  # Loan_ID, Start time, Close Time, Reserve Rate
        self.file_contents = [line.rstrip('\n') for line in open(file)]
        self.get_bidders_loaners()
        self.remove_invalid_bid()
        self.final_result_output()

    def get_bidders_loaners(self):
        for i in self.file_contents:
            if len(i) < 20:  # Bidder / Bids
                timestamp, user_id, action, loan_id, rate = i.split("|")
                self._bidders.append(
                    Bidder(timestamp, user_id, action, loan_id, rate))
                self._bidders_original.append(
                    Bidder(timestamp, user_id, action, loan_id, rate))
            else:
                timestamp, user_id, action, loan_id, credit, reserve_rate, close_time = i.split("|")
                self._loaners.append(
                    Loaner(timestamp, user_id, action, loan_id, credit, reserve_rate, close_time))

        for i in self._loaners:
            self.auction_info[i.loan_id] = [
                i.timestamp, i.close_time, i.reserve_rate]

    # Check the times of the bids, remove them if they're not in range.
    # "Arrives after the auction start time and before or on the closing
    # time."

    def check_bid_times(self, key, start_close):
        for i in self._bidders:
            if i.loan_id == key:
                if int(i.timestamp) not in range(
                        int(start_close[0]), int(start_close[1]) + 1):
                    self._bidders.remove(i)

    # Remove bids that are do not match the following condition; "Is smaller
    # than any previous valid bids submitted by the user."

    def check_next_bids(self):
        # Create dictitonary of all bidders/bids
        id_counts = {}
        for b in self._bidders:
            if b.user_id in id_counts:
                # Check for all duplicate id's
                id_counts[b.user_id] += 1
            else:
                id_counts[b.user_id] = 1

        # Add them to a list if their count is more than 1
        result = [b for b in self._bidders if id_counts[b.user_id] > 1]

        for idx, firstElement in enumerate(result):
            # Get first Element
            FirstElement = firstElement
            # Get next element
            NextElement = result[(idx + 1) % len(result)]
            if FirstElement.user_id == NextElement.user_id:                  # if they got the same user_id
                if FirstElement.loan_id == NextElement.loan_id:              # if they got the same loan_id
                    # check if the next element is less than the last "Is
                    # smaller than any previous valid bids submitted by the
                    # user."
                    if NextElement.rate < FirstElement.rate:
                        pass                                                 # pass it
                    # Other wise remove it from the self._bidders which
                    # currently contains all valid bids.
                    else:
                        self._bidders.remove(NextElement)

    # Loop through the loaners and run the check_bid for each key
    def remove_invalid_bid(self):

        for key, start_close in self.auction_info.items(
        ):                   # Loop through self.auction_info and run functions accordingly
            self.check_bid_times(key, start_close)

        self.check_next_bids()

        for key, start_close in self.auction_info.items():
            self._result(key, start_close)

    def _result(self, key, reserve_rate):

        all_bids = []
        earliest_timestap = []
        # Get total bids from original bidders/bids
        total_bid_count = 0

        for i in self._bidders_original:
            if i.loan_id == key:
                total_bid_count += 1

        # If there is only 1 bid, then pay the reserve rate of the loan
        if total_bid_count == 1:
            # print("One")
            for i in self._bidders:
                rate = reserve_rate[2]
                all_bids.append(i.rate)
                status = "SOLD"
                user_id = i.user_id
                rate = min(all_bids)

        # If there is are equal amounts, earliest bid wins.
        elif total_bid_count % 2 == 0:
            for i in self._bidders:
                all_bids.append(i.rate)
                if i.loan_id == key:
                    earliest_timestap.append(i.timestamp)
                    if i.timestamp == min(earliest_timestap):
                        status = "SOLD"
                        user_id = i.user_id
                        rate = i.rate
        else:
            # print("Odd")
            for i in self._bidders:
                if i.loan_id == key:  # Check if keys match                  # If bid == key
                    # Add rates to seperate list so they can be used later
                    all_bids.append(i.rate)
                    # Default status is an empty string
                    status = ""
                    # if the rate of the bid is lower than the reserve_rate of
                    # the loaner then set status to SOLD
                    if i.rate <= reserve_rate[2]:
                        status = "SOLD"
                        # Get correct user_id and rate
                        user_id = i.user_id
                        rate = min(all_bids)
                    # Else set the following values as Not sold, No user_id and
                    # UNSOLD
                    else:
                        rate = "0.00"
                        user_id = ""
                        status = "UNSOLD"

        self._winners.append(
            Results(reserve_rate[1], key, user_id, status, rate, total_bid_count, max(all_bids), min(all_bids)))  # Add winners to list and loop through to print them

    def final_result_output(self):
        for i in self._winners:
            print(i)
        print("\n")

# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


def main():
    print("Enter 'Exit' to close program")
    fileName = input("Enter file name: ") + ".txt".lower()
    print("\n")
    if fileName == "exit.txt" or fileName == "Exit.txt":
        exit()
    else:
        try:
            # Added Try Except check if file exists
            Auction(fileName)
            main()
        except Exception as e:
            print(e, "\n")
            print(" - Try Again - ")
            main()


if __name__ == "__main__":
    main()
