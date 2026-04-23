from math import ceil
import random


class ListModifier:
    def __init__(self, num_start, num_end):
        self.num_start = num_start
        self.num_end = num_end
        self.nums_list = []
        self.fill_list()

    def fill_list(self):
       self.nums_list = list(range(self.num_start, self.num_end + 1))

    def is_long_list(self):
        return len(self.nums_list) > 3

    def get_list_middle(self):
        middle_idx = ceil(len(self.nums_list) / 2)
        return self.nums_list[middle_idx - 1]

    #  logic to modify initial list of number on the base of specific item
    #  flag is yes/no answer converted to boolean type
    #  val is start or end element for modified list
    def modify_list_by_range(self, flag, val):
        idx = self.nums_list.index(val)

        if flag:
            self.nums_list = self.nums_list[idx + 1:]
        else:
            self.nums_list = self.nums_list[: idx + 1]

    def remove_num_from_list(self, val):
        self.nums_list.remove(val)

    def modify_list_with_single_num(self, val):
        self.nums_list = [val]


class Predictor(ListModifier):
    def __init__(self, num_start, num_end):
        super().__init__(num_start, num_end)

    def init_print(self):
        print(f'🔮 Please guess any integer number from {self.num_start} to {self.num_end} 🔮')

    def final_print(self):
        print(f'✨ You\'ve guessed the number: {self.nums_list[0]} ✨')

    @staticmethod
    def is_yes_answer(answer):
        return answer.upper() == 'Y' or answer.upper() == 'YES'

    @staticmethod
    def is_no_answer(answer):
        return answer.upper() == 'N' or answer.upper() == 'NO'

    def is_valid_answer(self, answer):
        return self.is_yes_answer(answer) or self.is_no_answer(answer)

    def run_ready_questions(self):
        ready_answer = input('Are you ready? Enter Y or N :  ')

        while not self.is_yes_answer(ready_answer):
            ready_answer = input('Waiting... Are you ready now? Enter Y or N :  ')

    def run_num_questions(self):
        #  logic to reduce prediction steps if list length > 3
        #  loop modifies initial list of numbers on the base of middle item
        while self.is_long_list():
            mid_num = self.get_list_middle()
            answer = input(f'Your number is greater than {mid_num}? Enter Y or N :  ')

            while not self.is_valid_answer(answer):
                answer = input(f'Try again... Your number is greater than {mid_num}? Enter Y or N :  ')
                continue

            self.modify_list_by_range(self.is_yes_answer(answer), mid_num)

        while len(self.nums_list) > 1:
            random_num = random.choice(self.nums_list)
            answer = input(f'Your number is {random_num}? Enter Y or N :  ')

            while not self.is_valid_answer(answer):
                answer = input(f'Try again... Your number is {random_num}? Enter Y or N :  ')
                continue

            if self.is_no_answer(answer):
                self.remove_num_from_list(random_num)
            elif self.is_yes_answer(answer):
                self.modify_list_with_single_num(random_num)
                break

        self.final_print()

    def start(self):
        self.init_print()
        self.run_ready_questions()
        self.run_num_questions()
        self.stop_or_proceed()

    def stop_or_proceed(self):
        proceed_answer = input('Do you want to proceed? Enter Y or N :  ')

        while not self.is_valid_answer(proceed_answer):
            proceed_answer = input('Try again... Do you want to proceed? Enter Y or N :  ')

        if self.is_yes_answer(proceed_answer):
            self.fill_list()
            self.start()
        else:
            return


my_predictor = Predictor(1, 10)
my_predictor.start()
