if not exist utils\states.py (
echo # Conversation states > utils\states.py
echo SELECTING_AMOUNT, CONFIRMING_DEPOSIT = range(2) >> utils\states.py
echo SELECT_SERVICE, ENTER_LINK, ENTER_QUANTITY, CONFIRM_ORDER = range(4, 8) >> utils\states.py
)