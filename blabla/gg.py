from td import TdJson

# Создаём клиента TDLib
client = TdJson()

# Простейший тест: получить TDLib версию
client.send({'@type': 'getTdlibParameters'})
print("TDLib работает!")