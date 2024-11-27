# Проект для курса "Технологии программирования на python" от Болдаева Александра
## Чат-бот для подготовки к тестам. Имеющий автоматическое создание примеров на тему теста.

### Краткое описание:
Чат-бот для подготовки к тестам. Имеющий автоматическое создание задач на тему теста и показа решения на задачи. 

### Возможности:
- Решение теста, созданного программой.
- Смотреть статистику по решению теста.
- Смотреть решение и ответы на задачи в тесте.
- Возможность пройти тест снова по хэшу.

### Команды:
| Команда                                     | Что делает команда.                                                                                              | Параметры (если есть).                                                                                           | 
|---------------------------------------------|------------------------------------------------------------------------------------------------------------------|------------------------------------------------------------------------------------------------------------------|
| */start*                                    | Выдаёт краткое описание бота и предметы по которым можно выбрать тест.                                           | -                                                                                                                | 
| */help*                                     | Выдаёт список всех команд чат-бота и как правильно вводить ответы на задачу.                                     | -                                                                                                                |
| */tests* object                             | просмотр тем тестов.                                                                                             | object - Выбор предмета из возможных (math, математика; physics, физика)                                         |
| */start_test* name                          | начать решение теста.                                                                                            | name - Название теста или его номер.                                                                             |
| */test_statistics* name                     | выводит статистику теста (Количество попыток, лучший балл, баллы на первой попытке, баллы на последней попытке). | name - Название теста или его номер.                                                                             |
| */answer* task answer или */an* task answer | Дать ответ после начала решения.                                                                                 | task - Номер задачи в тесте; answer - ответ на задачу (правила записи ответа выводятся при вводе команды /help). |
| */end*                                      | заканчивает тест                                                                                                 | -                                                                                                                |

### Правила ввода ответов:
Появиться позже...

## Проектирование:
* *Тесты*:

Нахождение теста по указанному предмету;

Запуск теста по его названию на определённую тему;

Быстрое создание тестов на тему (из-за имеющихся функций в программе);

* *Решения*:
    
Функции для вывода последовательного решения для пользователя (например дискриминант);

Функции упрощающие внутренние вычисления;

* *Статистика и ответы* (информация о тестах):

Вывод статистики человека на задачу;

Нахождение ответов на тесты из json файла;

### Пример разговора с чат-ботом:
*you* - /start

*training_tests_bot* - Здравствуйте! Вы обратились к чат-боту с тестами. Я чат-бот для подготовки к тестам. 
           Имеющий автоматическое создание примеров на тему теста. Чтобы узнать мой функционал, напишите "/help".

*you* - /tests math

*training_tests_bot* - Вот тесты по математике:

...

12. Полные квадратные уравнения.

...

*you* - /start_test 12

*training_tests_bot* - Начинаю тест "Полные квадратные уравнения" под номером 12.

Задачи:
1. x^2 - 6x + 9 = 0

*you* - /an 1 3

*training_tests_bot* - Ответ на 1 вопрос принят (ответ который вы дали - 3).

*you* - /end

*training_tests_bot* - Тест "Полные квадратные уравнения" завершён. Решения нужны (да/нет)?

*you* - да

*training_tests_bot* - Решения:

1 Задача:
1. x^2 - 6x + 9 = 0
2. Найдём дискриминант: D = 6^2 - 4*(9)
3. D = 0, => Один корень
4. x1 = - (-6 / 2*1)
5. x1 = 3

*training_tests_bot* - ответы:
1. Ваш ответ: 3.

Правильный ответ: 3.

Вердикт: Правильно

*training_tests_bot* - Результаты:

Количество попыток - 1

Лучший балл - 1 (100%)

Баллы на первой попытке - 1

Баллы на последней попытке - 1



``` python
#　　　　　／＞　  フ
#　　　　　| 　_　 _|
#　 　　　／`ミ _x 彡
#　　 　 /　　　 　 |
#　　　 /　 ヽ　　 ﾉ
#　／￣|　　 |　|　|
#　| (￣ヽ＿_ヽ_)_)
#　＼二つ
```