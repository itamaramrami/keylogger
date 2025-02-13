from abc import ABC,abstractmethod

class Encryption(ABC):
    @abstractmethod
    def encrypt(self,text):
        pass

    @abstractmethod
    def decrypt(self,encrypted_text):
        pass

class XOREncryption:

    def __init__(self,password):
        self.password = password.encode("utf-8")


    def encrypt(self,text):
        """
        Accepts unencrypted text and encrypts
         it using the XOR method
        :param text: unencrypted text
        :return: encrypted text
        """
        xor_encrypted = "".join(
            chr(ord(x) ^ ord(y))
            for x, y in zip(
                text, self.password * (len(text) // len(self.password)) + self.password[: len(text) % len(self.password)]
            )
        )
        return xor_encrypted

    # Decode using XOR
    def decrypt(self,encrypted_text):
        """
        Receives an encrypted text using the XOR method and
         returns the unencrypted (original) text
        :param encrypted_text: encrypted text
        :return: unencrypted text
        """
        return "".join(
            chr(ord(x) ^ ord(y))
            for x, y in zip(
                encrypted_text,
                self.password * (len(encrypted_text) // len(self.password))
                + self.password[: len(encrypted_text) % len(self.password)],
            )
        )
