from flask import session

def encrypt_message( message):
        encrypted_message = ""
        key = int( session['shared'] )
        for c in message:
            encrypted_message += chr(ord(c)+key)
        return encrypted_message

def decrypt_message( encrypted_message):
        decrypted_message = ""
        key = int( session['shared'] )
        for c in encrypted_message:
            decrypted_message += chr(ord(c)-key)
        return decrypted_message
