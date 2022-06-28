from urllib import response
import requests

BASE = 'http://127.0.0.1:5001/'

print('primero agregaremos varios libros')

# data = [{'nombre' : 'Violeta', 'autor' : 'Isabel Allende','ventas' : 5153},
#         {'nombre' : 'La insoportable levedad del ser', 'autor' : 'Milan Kundera','ventas' : 5100},
#         {'nombre' : 'Al paraíso', 'autor' : 'Hanya Yanagihara','ventas' : 5000},]

# for i in range(len(data)):
#     response = requests.put(BASE + 'libro/' + str(i), data=data[i])
#     print(response)

# response = requests.get(BASE + 'video/1')
# print(response.json())

response = requests.delete(BASE + 'libro/1')
print(response)

response = requests.get(BASE + 'libro/1')
print(response)