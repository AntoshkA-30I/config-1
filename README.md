# Домашнее задание №1 Вариант 29

## Описание

Этот проект представляет собой эмулятор командной оболочки, который позволяет взаимодействовать с виртуальной файловой системой (VFS), упакованной в архив .tar. С помощью этого эмулятора вы можете выполнять различные команды для управления файлами и директориями внутри VFS.


## Запуск программы

Чтобы запустить эмулятор, используйте следующую команду, указывая путь к вашему архиву VFS:  `python emulator.py <VFS_path> <Log_path> <Start_path>` Где <vfs_path> — это путь к вашему архиву .tar, <Log_path> — это путь к вашему лог-файлу .xml, <Start_path> — это путь к вашему стартовому файлу .txt.

## Start- и Log- файлы
В стартовом файле хранятся команды для выполнения эмулятором. <br />
![](https://github.com/AntoshkA-30I/config-1/blob/main/images/%D1%81%D1%82%D0%B0%D1%80%D1%82%D0%BE%D0%B2%D1%8B%D0%B9%20%D1%81%D0%BA%D1%80%D0%B8%D0%BF%D1%82.png)
Лог файл содержит историю последнего сеанса работы с эмулятором. В данном примере - выполнение команд из стартового файла. <br />
![](https://github.com/AntoshkA-30I/config-1/blob/main/images/%D0%BB%D0%BE%D0%B3%20%D1%84%D0%B0%D0%B9%D0%BB.png)

## Использование

-   ls — показать содержимое текущей директории.
-   cd — сменить текущую директорию.
-   exit — выйти из эмулятора.
-   rmdir— удалить директорию если она пустая.
-   tree — отобразить структуру директорий.


## Тестирование с помощью Pytest
![](https://github.com/AntoshkA-30I/config-1/blob/main/images/%D1%82%D0%B5%D1%81%D1%82%D0%B8%D1%80%D0%BE%D0%B2%D0%B0%D0%BD%D0%B8%D0%B5%20%D0%BF%D1%80%D0%BE%D0%B3%D1%80%D0%B0%D0%BC%D0%BC%D0%BE%D0%B9.png)

## Тестирование
### Запуск программы
![](https://github.com/AntoshkA-30I/config-1/blob/main/images/%D0%B7%D0%B0%D0%BF%D1%83%D1%81%D0%BA.png)
### Команда ls
![](https://github.com/AntoshkA-30I/config-1/blob/main/images/ls.png)
### Команда cd
![](https://github.com/AntoshkA-30I/config-1/blob/main/images/cd1.png)
![](https://github.com/AntoshkA-30I/config-1/blob/main/images/cd2.png)
### Команда rmdir
![](https://github.com/AntoshkA-30I/config-1/blob/main/images/rmdir%201.png)
если директории не существует:
![](https://github.com/AntoshkA-30I/config-1/blob/main/images/rmdir%20fail%201.png)
если директория не пустая:
![](https://github.com/AntoshkA-30I/config-1/blob/main/images/rmdir%20fail%202.png)
### Команда tree
![](https://github.com/AntoshkA-30I/config-1/blob/main/images/tree.png)
### Пример работы с эмулятором
![](https://github.com/AntoshkA-30I/config-1/blob/main/images/%D0%BF%D1%80%D0%B8%D0%BC%D0%B5%D1%80%20%D1%80%D0%B0%D0%B1%D0%BE%D1%82%D1%8B.gif)
