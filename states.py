from aiogram.fsm.state import State, StatesGroup


class RegisterAccount(StatesGroup):
    waiting_for_email = State()
    waiting_for_password = State()
    waiting_for_server = State()


class AddAlias(StatesGroup):
    waiting_for_email = State()
    waiting_for_name = State()


class RemoveAlias(StatesGroup):
    waiting_for_email = State()


class SearchEmails(StatesGroup):
    waiting_for_query = State()
