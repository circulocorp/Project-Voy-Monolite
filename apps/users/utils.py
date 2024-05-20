import random
import string

def generate_username(email: str):
    random_numbers = random.sample(range(10), 3)
    username = '{}{}'.format(email.split('@')[0], ''.join(map(str, random_numbers)))
    return username

def generate_otp():
    return random.randint(100000, 999999)

def generate_secure_password(length=8):
    if length < 8:
        raise ValueError("La longitud de la contraseña debe ser al menos 8 caracteres.")

    # Crear conjuntos de caracteres
    all_characters = string.ascii_letters + string.digits
    uppercase_characters = string.ascii_uppercase
    lowercase_characters = string.ascii_lowercase
    digit_characters = string.digits

    # Asegurarse de incluir al menos un carácter de cada tipo
    password = [
        random.choice(uppercase_characters),
        random.choice(lowercase_characters),
        random.choice(digit_characters),
    ]

    # Completar la contraseña con caracteres aleatorios hasta alcanzar la longitud deseada
    while len(password) < length:
        password.append(random.choice(all_characters))

    # Mezclar los caracteres para evitar patrones
    random.shuffle(password)

    return ''.join(password)
    