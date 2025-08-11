class StringUtils:
    def reverse_string(self,s:str)->str:
        if not isinstance(s, str):
            raise TypeError("Должна быть строка")
        return s[::-1]

    def get_initials(self, full_name:str)->str:
        if not isinstance(full_name,str):
            raise TypeError("Должна быть строка")
        if not full_name:
            raise ValueError("Не должно быть пусто")
        return "".join(word[0].upper() for word in full_name.strip().split())
