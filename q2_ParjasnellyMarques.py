from q1_ParjasnellyMarques import create_transaction, check_account, confirm_payment
import threading
import time


# Verifica se uma transação foi completada com sucesso
assert (create_transaction('Paulo', '456', 1000, 'Fund Transfer'))
# Verifica se o check_account está retornando uma conta válida
assert (check_account('Paulo', '456'))
# Verifica se a transação com credenciais incorretas foi recusada
assert (not confirm_payment('asdasdasd', 'asddasdas', 500))
print("-------------------Fim testes unitários-------------------")

print("Iniciando teste de stress, aguarde...")
# Adicionei esse delay para os prints não ficarem misturados
time.sleep(2)
# Teste de stress
testdict = lambda dic, key: key in dic.keys()
pbranches = lambda: 10000
threads = [threading.Thread(target=create_transaction, args=('Paulo', '456', 1000, 'Fund Transfer')) for t in range(pbranches())]
start = lambda t: t.start()
join = lambda t: t.join()
[start(t) for t in threads]
[join(t) for t in threads]


