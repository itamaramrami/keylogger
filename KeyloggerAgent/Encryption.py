from abc import ABC,abstractmethod

class IEncrypter(ABC):
    @abstractmethod
    def encrypt(self,text):
        pass

    @abstractmethod
    def decrypt(self,encrypted_text):
        pass

class XOREncryption(IEncrypter):

    def __init__(self,password):
        self.__password = password


    def encrypt(self,text):
        """
        Accepts unencrypted text and encrypts
         it using the XOR method
        :param text: unencrypted text
        :return: encrypted text
        """
        xor_encrypted = list(
            (ord(x) ^ ord(y))
            for x, y in zip(
                text, self.__password * (len(text) // len(self.__password)) + self.__password[: len(text) % len(self.__password)]
            )
        )
        return xor_encrypted


    def decrypt(self,encrypted_text):
        """
        Receives an encrypted text using the XOR method and
         returns the unencrypted (original) text
        :param encrypted_text: encrypted text
        :return: unencrypted text
        """
        return ''.join(
            chr(x ^ ord(y))
            for x, y in zip(
                encrypted_text,
                self.__password * (len(encrypted_text) // len(self.__password))
                + self.__password[: len(encrypted_text) % len(self.__password)]
            )
        )

