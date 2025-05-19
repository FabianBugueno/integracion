from django.forms import ValidationError

class MaxSizeFileValidator:
    def __init__(self, max_size=5):  
        self.max_size = max_size
    def __call__(self, value):
        size = value.size
        max_size = self.max_size * 1048576

        if size > max_size: 
            raise ValidationError(f'El tamaño del archivo no puede ser mayor a {self.max_size} MB')
        return value