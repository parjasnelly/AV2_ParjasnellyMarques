from q1_ParjasnellyMarques import create_transaction
import threading
import time


# Verifica se uma transação foi completada com sucesso
assert (create_transaction('Paulo', '456', 1000, 'Fund Transfer'))
# Verifica se a transação com saldo insuficiente foi recusada
assert (not create_transaction('Thais', '789', 4000, 'Credit'))
# Verifica se a transação com credenciais incorretas foi recusada
assert (not create_transaction('asdasdasd', 'asddasdas', 500, 'Cash'))
print("-------------------Fim testes unitários-------------------")

print("Iniciando teste de stress, aguarde...")
# Adicionei esse delay para os prints não ficarem misturados
time.sleep(1)
# Teste de stress
testdict = lambda dic, key: key in dic.keys()
pbranches = lambda: 10000
threads = [threading.Thread(target=create_transaction, args=('Paulo', '456', 1000, 'Fund Transfer')) for t in range(pbranches())]
start = lambda t: t.start()
join = lambda t: t.join()
[start(t) for t in threads]
[join(t) for t in threads]


