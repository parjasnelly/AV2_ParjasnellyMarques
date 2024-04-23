contas = [
    {'login': 'Irineu', 'senha': '123', 'saldo': 1000},
    {'login': 'Paulo', 'senha': '456', 'saldo': 2000},
    {'login': 'Thais', 'senha': '789', 'saldo': 3000}
]


def close_transaction(msg):
    # Coloquei os \n para pular linha e ficar mais organizado
    print(f"{msg}, Closed (Canceled) Transaction\n")
    # Coloquei o return False para saber se a transação foi fechada com falha nos testes unitários
    return False


def complete_transaction():
    # Coloquei o \n para pular linha e ficar mais organizado
    print("Completed Transaction\n")
    # Coloquei o return True para saber se a transação foi completada com sucesso nos testes unitários
    return True


get_account = lambda login, senha: [conta for conta in contas if conta['login'] == login and conta['senha'] == senha]
check_account = lambda login, senha: get_account(login, senha)[0] if get_account(login, senha) else []

confirm_payment = lambda login, senha, valor: (update_balance(check_account(login, senha), valor) if check_account(login,senha)['saldo'] >= valor else close_transaction("Insufficient balance")) if len(check_account(login, senha)) > 0 else close_transaction("Verify your credentials)")
confirm_cash = lambda login, senha, valor: (update_balance_cash(check_account(login, senha), valor) if check_account(login,senha)['saldo'] >= valor else close_transaction("Insufficient balance")) if len(check_account(login, senha)) > 0 else close_transaction("Verify your credentials")
check_payment_condition = lambda login, senha, valor, forma_pagamento: cash(login, senha, valor) if forma_pagamento == 'Cash' else fund_transfer(login, senha, valor) if forma_pagamento == 'Fund Transfer' else credit(login, senha, valor) if forma_pagamento == 'Credit' else close_transaction("Invalid payment condition")


def create_transaction(login, senha, valor, forma_pagamento):
    print("Create Transaction")
    print(f"Chosen Payment Condition: {forma_pagamento}")
    return check_payment_condition(login, senha, valor, forma_pagamento)


def update_balance(conta, valor):
    conta.update({'saldo': conta['saldo'] - valor})
    print(f"Confirmed payment approval from bank, updated balance: ${conta['saldo']}")
    return complete_transaction()

def update_balance_cash(conta, valor):
    conta.update({'saldo': conta['saldo'] - valor})
    print(f"Cash received, updated balance: ${conta['saldo']}")
    print("Return Payment Receipt")
    return complete_transaction()


def fund_transfer(login, senha, valor):
    print(f"Provide Bank Deposit Details: Account id: {login}, password: {senha}")
    return confirm_payment(login, senha, valor)


def credit(login, senha, valor):
    print(f"Provide Credit Account Details: Account id: {login}, password: {senha}")
    print(f"Request Payment from bank: {valor}")
    return confirm_payment(login, senha, valor)


def cash(login, senha, valor):
    print(f"Cash to receive: ${valor}")
    return confirm_cash(login, senha, valor)


def main():
    # Exemplo de uso da função create_transaction
    create_transaction('Paulo', '456', 1000, 'Fund Transfer')
    create_transaction('Paulo', '456', 1000, 'Cash')
    create_transaction('Thais', '789', 1000, 'Credit')
    # Exemplos de falha
    create_transaction('Thais', '789', 4000, 'Credit')
    create_transaction('Thais', '789', 500, 'Fund')
    create_transaction('Irineu', '', 500, 'Cash')
    create_transaction('asdasdasd', 'asddasdas', 500, 'Cash')


# Verifica se o arquivo foi importado ou executado diretamente
check_import = lambda: main() if __name__ == '__main__' else None
check_import()
