# Sokoban

Логическая 2d игра-головоломка, в которой игрок передвигает ящики по лабиринту, показанному сверху, с целью поставить все ящики на заданные конечные позиции. Только один ящик может быть передвинут за раз, причём герой игры может только толкать ящики, но не тянуть их. Перемещение с помощью W,A,S,D, хватать/отпускать ящик с помощью E, выход в меню esc. Игрок также может создавать собственные уровни.

# Это должно будет выглядеть примерно так:
![Иллюстрация к проекту](https://github.com/Konopatkin-OV/MSU_Python_Project_Prac_2020/blob/master/gui.jpg)

# Участники:
1. Конопаткин Олег (524 группа)
2. Коробова Екатерина (524 группа)
3. Некрасова Мария (511 группа)

# Установка
К проекту прикручены setuptools и wheel, поэтому можно просто написать команду:

python setup.py bdist_wheel

и в папке dist появится wheel проекта.

В нормальных коммитах в папке dist уже должен лежать готовый wheel для текущего состояния проекта, его можно установить командой:

pip install [path_to_project]\dist\Sokoban-0.1-py3-none-any.whl

Пример запуска приложения в файле launch.py

# Есть немножко юнит-тестов
Их можно выполнить, импортировав модуль Sokoban.tests
