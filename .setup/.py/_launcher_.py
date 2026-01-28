# Модули
import os, webbrowser, requests, shutil
from pathlib import Path

# Что-либо сделать с текстовыми файлами
def _doSomethingWithAtxt(name, answer, mode, writeTXT):
    with open(Path(".setup") / ".txt" / f"{name}.txt", f"{mode}", encoding="utf-8") as f:
        match answer:
            case "write":
                f.write(writeTXT)
            case "read":
                return f.read()

# Очистка
def _clear():
    if os.name == "nt":
        os.system("cls")
    else:
        os.system("clear")

# Удаление и возращение различных файлов
def _clearAndCreate(need_DeleteFile, name):
    if need_DeleteFile:
        os.remove(Path(_path_) / f"{name}")
    else:
        shutil.rmtree(Path(_path_) / f"{name}")
        os.mkdir(Path(_path_) / f"{name}")

# Получить актуальные данные о чём-то, в текстовом формате
def _requestsInfoGame(txt):
    return requests.get(f"https://raw.githubusercontent.com/blohoped/_serverTXT/main/_nzLauncher/{txt}.txt").text

# Обращения к api Яндекс Диска, чтобы получить прямую ссылку на файл
def _requestsGameLink(link): # принимает саму ссылку на файл
    response = requests.get(f"https://cloud-api.yandex.net/v1/disk/public/resources/download?public_key={link}") # отправляет GET запрос, и получает JSON
    return response.json()["href"] # превращает JSON в словарь, и по ключу href, достаёт и возращает прямую ссылку

# База со всеми играми
base = {}

# Шаблон для добавления игр
class game:
    name = None
    link = None
    description = None
    rating = None
    gameplay = None
    playersNeed = None
    note = None
    autor = None

# Полученные данные разбить на элементы для списка
_namesList_ = _requestsInfoGame("names").splitlines()
_descriptionsList_ = _requestsInfoGame("descriptions").splitlines()
_linksList_ = _requestsInfoGame("links").splitlines()
_gameplayList_ = _requestsInfoGame("gameplay").splitlines()
_playersNeedList_ = _requestsInfoGame("playersNeed").splitlines()
_notesList_ = _requestsInfoGame("notes").splitlines()
_autorsList_ = _requestsInfoGame("autors").splitlines()
_ratingsList_ = list(map(int, _requestsInfoGame("ratings").splitlines()))

# Переменные, которые читают информацию с текстовых файлов        
_minecraftPath = _doSomethingWithAtxt("_path_", "read", "r", None)
_shouldUnzip = _doSomethingWithAtxt("_shouldUnzip_", "read", "r", None)
_path_ = _doSomethingWithAtxt("_path_", "read", "r", None)

# Меню
def menu(forStart):
    while True:
        _clear()
        print("Все доступные игры: ")
        print("<------------------->")
        if forStart: # нужен, чтобы скрипт не добавлял каждый раз игру в базу
            for number, i in enumerate(range(len(_namesList_)), start=1):
                _createGame = game()

                _createGame.name = _namesList_[i]
                _createGame.link = _requestsGameLink(_linksList_[i])
                _createGame.description = _descriptionsList_[i]
                _createGame.rating = _ratingsList_[i]
                _createGame.gameplay = _gameplayList_[i]
                _createGame.playersNeed = _playersNeedList_[i]
                _createGame.note = _notesList_[i]
                _createGame.autor = _autorsList_[i]
            
                base[_namesList_[i]] = _createGame
                base[str(number)] = _createGame
            forStart = False
        for number, i in enumerate(range(len(_namesList_)), start=1):
            print(f"[{number}]: {_namesList_[i]}")
        print("<------------------->")
        print("[0]: выход")

        _answerUser=input("> ")

        if _answerUser in base:
            _saveData = base[_answerUser] # для более удобного обращения к параметрам объекта
            while True:
                _clear()
                print(f"Все действия над {_saveData.name}")
                print(f"<------------------{len(_saveData.name) * "-"}>")
                print("[1]: посмотреть информацию")
                print("[2]: включить геймплей")
                print("[3]: скачать игру")
                print("[0]: выход")
                print(f"<------------------{len(_saveData.name) * "-"}>")
                _answerUser=input("> ")
                match _answerUser:
                    case "1":
                        _clear()
                        print(f"Вся информация об {_saveData.name}")
                        print(f"<---------------------{len(_saveData.name) * "-"}>")
                        print("[Описание]:")
                        print(f"> {_saveData.description}")
                        print("[Рейтинг]:")
                        print(f"> {_saveData.rating}% положительно | {100 - _saveData.rating}% отрицательно")
                        print("[Игроки]:")
                        print(f"> {_saveData.playersNeed}")
                        print("[Заметки]:")
                        print(f"> {_saveData.note}")
                        print("[Авторы]:")
                        print(f"> {_saveData.autor}")
                        print(f"<---------------------{len(_saveData.name) * "-"}>")
                        input("Нажмите Enter, чтобы продолжить...")

                    case "2":
                        webbrowser.open(_saveData.gameplay)

                    case "3":
                        _clear()
                        if _shouldUnzip != "False":
                            if os.path.exists(Path(_path_) / "mods") and os.path.exists(Path(_path_) / "saves") and os.path.exists(Path(_path_) / "shaderpacks") and os.path.exists(Path(_path_) / "resourcepacks"):
                                # проверяет, есть ли папки в каталоге, и если да - пересоздаёт (нужно, чтобы при повторном скачивании режимов, сами режимы не накладывались друг на друга)
                                _clearAndCreate(False, "mods")

                                _clearAndCreate(False, "saves")

                                _clearAndCreate(False, "shaderpacks")

                                _clearAndCreate(False, "resourcepacks")

                            try:
                                # также очищает доп. файлы
                                _clearAndCreate(True, "options.txt")

                                _clearAndCreate(True, "optionsof.txt")

                                _clearAndCreate(True, "optionsshaders.txt")

                                _clearAndCreate(False, "config")
                            except Exception as e:
                                pass # их может и не быть, по этому здесь стоит заглушка

                        try:
                            _pathGame = os.path.join(str(Path.home() / "Downloads"), _saveData.name + ".zip")
                            # _pathGame собирает путь из домашнего каталога, и из папки Downloads. А на конец, скрепляет путь из названия игры и расширения .zip
                            if not os.path.exists(_pathGame): # проверяет, нет ли в директории точно такого-же файла
                                webbrowser.open(_saveData.link) # если нет, скачивает его
                                while True: # дальше, запускается цикл, который дожидается файла, каждый раз проверяя существования его по пути
                                    if os.path.exists(_pathGame):
                                        break

                            print("Подождите немного...")

                            if _shouldUnzip != "False": # тут идут проверки, надо ли распаковывать архив
                                shutil.unpack_archive(_pathGame, _minecraftPath)
                                os.remove(_pathGame) # удаляет исходный архив

                            else:
                                shutil.move(_pathGame, _minecraftPath)

                        except Exception as e:
                            print("Произошла ошибка!")
                            print(f"Код ошибки: {e}")
                            input("Нажмите Enter, чтобы продолжить...")

                        print("Установка завершена!")
                        input("Нажмите Enter, чтобы продолжить...")

                    case "0":
                        break

        elif _answerUser == "0":
            return
menu(True)