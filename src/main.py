from phonebook import PhoneBook, Contact


def input_contact() -> Contact:
    """Запрашивает данные контакта у пользователя"""
    return Contact(
        input("Фамилия: "),
        input("Имя: "),
        input("Отчество: "),
        input("Организация: "),
        input("Рабочий телефон: "),
        input("Личный телефон: ")
    )


def show_contacts_page(book: PhoneBook, current_page: int) -> int:
    """Показывает текущую страницу контактов и обрабатывает навигацию"""
    contacts = book.get_page(current_page)
    if not contacts:
        print("\nКонтакты не найдены!")
        input("\nНажмите Enter для возврата в меню...")
        return -1

    print(f"\n=== Страница {current_page} ===")
    for i, contact in enumerate(contacts, 1):
        print(f"\n{i}. {contact.display()}")

    print("\nНавигация:")
    print("1. Предыдущая страница")
    print("2. Следующая страница")
    print("Enter - вернуться в меню")

    choice = input("\nВыберите действие: ")

    match choice:
        case "1":
            return max(1, current_page - 1)
        case "2":
            return current_page + 1
        case "":  # Пустой ввод (просто Enter)
            return -1
        case _:
            return current_page


def main():
    book = PhoneBook("../data/contacts.csv")
    commands = {
        "1": "Показать контакты",
        "2": "Добавить контакт",
        "3": "Редактировать контакт",
        "4": "Поиск контактов",
        "5": "Выход"
    }

    while True:
        print("\nТелефонный справочник")
        for key, value in commands.items():
            print(f"{key}. {value}")

        match input("\nВыберите действие (1-5): "):
            case "1":
                current_page = 1
                while current_page > 0:
                    current_page = show_contacts_page(book, current_page)

            case "2":
                print("\n=== Добавление нового контакта ===")
                book.add(input_contact())
                print("\nКонтакт добавлен!")
                input("\nНажмите Enter для продолжения...")

            case "3":
                print("\n=== Редактирование контакта ===")
                try:
                    index = int(input("Введите номер контакта: ")) - 1
                    if book.edit(index, input_contact()):
                        print("\nКонтакт обновлен!")
                    else:
                        print("\nКонтакт не найден!")
                    input("\nНажмите Enter для продолжения...")
                except ValueError:
                    print("\nОшибка: введите корректный номер")
                    input("\nНажмите Enter для продолжения...")

            case "4":
                print("\n=== Поиск контактов ===")
                query = input("Введите поисковый запрос: ")
                results = book.search(query)
                if results:
                    for i, contact in enumerate(results, 1):
                        print(f"\n{i}. {contact.display()}")
                else:
                    print("\nКонтакты не найдены!")
                input("\nНажмите Enter для продолжения...")

            case "5":
                print("\nДо свидания!")
                break


if __name__ == "__main__":
    main()
