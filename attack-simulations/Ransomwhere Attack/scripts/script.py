from cryptography.fernet import Fernet

key = Fernet.generate_key()

with open("grades.csv", "rb") as original_file:
    original = original_file.read()

f = Fernet(key)

encrypted = f.encrypt(original)

with open("grades.csv", "wb") as encrypted_file:
    encrypted_file.write(encrypted)


# DECRYPT 

with open("grades.csv", "rb") as decrypted_file:
    decrypted_file.read()

decrypt = f.decrypt(encrypted)

with open ("decrypt_grades.csv", "wb") as decrypted_file:
    decrypted_file.write(decrypt)




