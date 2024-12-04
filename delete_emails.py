# Ниже представлен пример кода, который подключается к почтовому ящику,
# ищет письма с датой меньше 01/01/2024 и удаляет их

import imaplib
import email
from email.header import decode_header


# Настройки подключения
IMAP_SERVER = 'server'  # Замените на ваш IMAP-сервер
USERNAME = 'name@mail.ru'  # Ваш email
PASSWORD = 'password'  # Ваш пароль

# Период для фильтрации писем (например, последние 30 дней)
#days = 30
# date_since = (datetime.now() - timedelta(days=days)).strftime("%d-%b-%Y")
# Дата для фильтрации писем (до 2024 года)
date_until = "01-Feb-2024"

# Подключение к IMAP-серверу
mail = imaplib.IMAP4_SSL(IMAP_SERVER)
mail.login(USERNAME, PASSWORD)

# Выбор папки "Входящие"
mail.select("inbox")

status, messages = mail.search(None, f'BEFORE {date_until}')

# Получение идентификаторов писем
mail_ids = messages[0].split()

# Обработка каждого письма
for mail_id in mail_ids:
    status, msg_data = mail.fetch(mail_id, '(RFC822)')
    msg = email.message_from_bytes(msg_data[0][1])

    # Проверка наличия заголовка Subject
    subject = msg.get('Subject')
    if subject:
        # Декодирование заголовка Subject
        decoded_subject = decode_header(subject)
        subject_str = ''

        for part in decoded_subject:
            if isinstance(part[0], bytes):
                subject_str += part[0].decode(part[1] or 'utf-8')  # Декодируем с учетом кодировки
            else:
                subject_str += part[0]  # Если уже строка

        from_ = msg.get('From')
        date_ = msg.get('Date')

        print(f"Удаление письма:")
        print(f"Тема: {subject_str}")
        print(f"От: {from_}")
        print(f"Дата: {date_}")

        # Установка флага \Deleted для удаления письма
        mail.store(mail_id, '+FLAGS', '\\Deleted')
    else:
        print("Тема: (нет темы)")
        print(f"От: {msg.get('From')}")
        print(f"Дата: {msg.get('Date')}")

        # Установка флага \Deleted для удаления письма
        mail.store(mail_id, '+FLAGS', '\\Deleted')

# Окончательное удаление писем с установленным флагом \Deleted
mail.expunge()

# Закрытие соединения
mail.logout()
