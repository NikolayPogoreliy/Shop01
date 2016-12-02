import random
from django.conf import settings


class ImageUploader:
    """Mixin-класс для определения пути сохранения файлов, и переопределения имен файлов
        rename_file(self, filename) - переименовывает файл
        make_upload_path(self, filename) - создает папку с заданным именем"""

    def rename_file(self, filename):
        """ Возвращает новое имя файла
        Переопределение имени загружаемого файла путем добавления трех случайных чисел к имени файла"""
        n1 = random.randint(0, 10000)
        n2 = random.randint(0, 10000)
        n3 = random.randint(0, 10000)
        return str(n1) + "_" + str(n2) + "_" + str(n3) + '_' + filename

    def make_upload_path(self, filename):
        """ Возвращает полный путь для сохранения файла
        Создает папку с именем, на которое ссыдлается атрибут класса folder_name, (например если задать
        folder_name = 'attr_name' - метод будет сохранять файлы в папку с именем, на которое указывает
        attr_name). Если folder_name не задано - все будет сохраняться в /other/...
         Переопределяет имя файла путем вызова метода rename_file(self, filename)"""
        if self.folder_name:
            folder = getattr(self, self.folder_name, self.folder_name)
        else:
            folder = 'other'
        return '{}/{}/{}'.format(settings.IMAGE_UPLOAD_DIR, folder, self.rename_file(filename))
