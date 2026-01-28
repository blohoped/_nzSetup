# Модули
import os, subprocess, webbrowser, shutil
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

# Удаление и возращение папки
def _clearAndCreate(need_OsRemove, name):
    if need_OsRemove:
        os.remove(Path(_path_) / f"{name}")
    else:
        shutil.rmtree(Path(_path_) / f"{name}")
        os.mkdir(Path(_path_) / f"{name}")


# Меню
while True:
    _clear()
    print("_nzSetup | v0.1")
    print("<---------------->")
    print("[1]: скачать игру")
    print("[2]: настройки")
    print("[3]: автор")
    print("[0]: выход")
    print("<---------------->")
    _answerUser = input("> ")
    match _answerUser:
        case "1":
            if _path_ != "":
                subprocess.run(["python", Path(".setup") / ".py" / "_launcher_.py"])
            else:
                _clear()
                print("Сначало введите путь!")
                input("Нажмите Enter, чтобы продолжить...")

        case "2":
            _clear()
            _path_ = _doSomethingWithAtxt("_path_", "read", "r", None)
            _shouldUnzip_ = _doSomethingWithAtxt("_shouldUnzip_", "read", "r", None)
            print("Текущий раздел: настройки")
            print("<------------------------->")
            print(f"[1]: путь ({_path_})")
            print(f"[2]: распаковка ({_shouldUnzip_})")
            print(f"[3]: очистка папки майнкрафта")
            print("<------------------------->")
            _answerUser = input("> ")
            match _answerUser:
                case "1":
                    _clear()
                    _answerUser = input("Введите путь: ")
                    if os.path.exists(_answerUser) and not os.path.isfile(_answerUser) and not '"' in _answerUser[0][-1]:
                        _doSomethingWithAtxt("_path_", "write", "w", _answerUser)
                    else:
                        _clear()
                        print("Путь не должен ввести к файлам (архивам, изображением и т.д.)")
                        print("Путь не должен содержать кавычек в начале и в конце")
                        print("А также он должен существовать!")
                        input("Нажмите Enter, чтобы продолжить...")

                case "2":
                    _clear()
                    _answerUser = input("Введите либо True, либо False: ")
                    if _answerUser == "True" or _answerUser == "False":
                        _doSomethingWithAtxt("_shouldUnzip_", "write", "w", _answerUser)
                
                case "3":
                    if os.path.exists(Path(_path_) / "mods") and os.path.exists(Path(_path_) / "saves") and os.path.exists(Path(_path_) / "shaderpacks") and os.path.exists(Path(_path_) / "resourcepacks"):
                        _clearAndCreate(False, "mods")

                        _clearAndCreate(False, "saves")

                        _clearAndCreate(False, "shaderpacks")

                        _clearAndCreate(False, "resourcepacks")

                        try:
                            _clearAndCreate(True, "options.txt")

                            _clearAndCreate(True, "optionsof.txt")

                            _clearAndCreate(True, "optionsshaders.txt")

                            _clearAndCreate(False, "config")
                        except Exception as e:
                                pass

                    else:
                        _clear()
                        print("Вы пытаетесь очистить каталог майнкрафта, при этом заданный путь не ведёт к файлам майнкрафта!")
                        input("Нажмите Enter, чтобы продолжить")
            
        case "3":
            _clear()
            print("Перейти на страницу:")
            print("<------------------->")
            print("[NZ] - Nazzy")
            print("[BH] - blohoped")
            print("<------------------->")
            _answerUser = input("> ")
            match _answerUser:
                case "BH":
                    webbrowser.open("https://github.com/blohoped")
                case "NZ":
                    webbrowser.open("https://www.youtube.com/@NazzyChannel")

        case "0":
            break