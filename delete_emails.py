# Ниже представлен пример кода, который подключается к почтовому ящику,
# ищет письма с датой меньше 01/01/2024 и удаляет их

import imaplib
import email
from email.header import decode_header


def delete_old_emails(email_user, email_pass):
    # Подключение к IMAP-серверу
    mail = imaplib.IMAP4_SSL('imap.gmail.com')  # Замените на ваш IMAP сервер
    mail.login(email_user, email_pass)

    # Выбор почтового ящика (например, INBOX)
    mail.select("inbox")

    # Поиск писем с датой до 01-Jan-2024
    search_criteria = '(BEFORE "01-Jan-2024")'
    status, messages = mail.search(None, search_criteria)

    # Получение списка идентификаторов писем
    email_ids = messages[0].split()

    if not email_ids:
        print("Нет писем для удаления.")
        return

    for email_id in email_ids:
        # Получение информации о письме (для вывода заголовка)
        _, msg = mail.fetch(email_id, "(RFC822)")

        for response in msg:
            if isinstance(response, tuple):
                msg = email.message_from_bytes(response[1])
                subject, encoding = decode_header(msg["Subject"])[0]
                if isinstance(subject, bytes):
                    subject = subject.decode(encoding if encoding else 'utf-8')
                print(f"Удаление: {subject}")

                # Установка флага на удаление
                mail.store(email_id, '+FLAGS', '\\Deleted')

    # Удаление всех помеченных писем
    mail.expunge()

    # Закрытие почтового ящика и выход
    mail.close()
    mail.logout()


# Пример использования функции
email_user = input('your_email') # Замените на ваш email
email_pass = input('your_password')  # Замените на ваш пароль

delete_old_emails(email_user, email_pass)
