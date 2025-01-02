# Lista de números
numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

# Usar una función lambda para filtrar los números pares
evens = list(filter(lambda x: x % 2 == 0, numbers))

# Usar una función lambda para elevar cada número al cuadrado
squares = list(map(lambda x: x ** 2, numbers))

# Imprimir los resultados
print("Original numbers:", numbers)
print("Even numbers:", evens)
print("Squared numbers:", squares)

# Crear tu propia función lambda
# Aquí tienes un ejemplo para multiplicar cada número por 3
your_result = list(map(lambda x: x * 3, numbers))
print("Your result:", your_result)
