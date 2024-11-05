class Ceaser: 
    def __init__(self, key = 0): 
         self._key = key 
      
    def get_key(self): 
        return self._key 
      
    def set_key(self, x): 
        self._key = x

    def encypt(self, plaintext):
        key = cipher.get_key()
        phrase = str(plaintext)
        phrase = phrase.lower()
        list_phrase = [char for char in phrase]
        number = []
        updated_num = []
        new_phrase = []
        for letter in list_phrase:
            if ord(letter) == 32:
                number.append(32-key)
            elif ord(letter) >= 97 and ord(letter) <= 122 and ord(letter)+key>122:
                number.append(ord(letter)-26)
            elif ord(letter) >= 97 and ord(letter) <= 122 and ord(letter)+key<97:
                number.append(ord(letter)+26)
            else:
                number.append(ord(letter))
        for int in number:
            updated_num.append(int+key)
        for numby in updated_num:
            new_phrase.append(chr(numby))
        encrypted_string = ""
        for char in new_phrase:
            encrypted_string += char
        return encrypted_string
    def decrypt(self, plaintext):
        key = cipher.get_key()
        phrase = str(plaintext)
        phrase = phrase.lower()
        list_phrase = [char for char in phrase]
        number = []
        updated_num = []
        new_phrase = []
        for letter in list_phrase:
            if ord(letter) == 32:
                number.append(32+key)
            elif ord(letter) >= 97 and ord(letter) <= 122 and ord(letter)-key>122:
                number.append(ord(letter)-26)
            elif ord(letter) >= 97 and ord(letter) <= 122 and ord(letter)-key<97:
                number.append(ord(letter)+26)
            else:
                number.append(ord(letter))
        for int in number:
            updated_num.append(int-key)
        for numby in updated_num:
            new_phrase.append(chr(numby))
        decrypted_string = ""
        for char in new_phrase:
            decrypted_string += char
        return decrypted_string