import csv
from dataclasses import dataclass
from typing import List


@dataclass
class Contact:
    """Контакт в телефонной книге"""
    last_name: str
    first_name: str
    middle_name: str
    organization: str
    work_phone: str
    personal_phone: str

    def display(self) -> str:
        """Возвращает строковое представление контакта"""
        return f"{self.last_name} {self.first_name}\n" \
               f"Организация: {self.organization}\n" \
               f"Тел. раб.: {self.work_phone}, личный: {self.personal_phone}"


class PhoneBook:
    def __init__(self, file_path: str, page_size: int = 5):
        self.file_path = file_path
        self.page_size = page_size

    def _read_contacts(self) -> List[Contact]:
        """Читает все контакты из файла"""
        try:
            with open(self.file_path, 'r', encoding='utf-8') as file:
                return [Contact(*row) for row in csv.reader(file)]
        except FileNotFoundError:
            return []

    def _save_contacts(self, contacts: List[Contact]) -> None:
        """Сохраняет контакты в файл"""
        with open(self.file_path, 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            for contact in contacts:
                writer.writerow(vars(contact).values())

    def add(self, contact: Contact) -> None:
        """Добавляет новый контакт"""
        contacts = self._read_contacts()
        contacts.append(contact)
        self._save_contacts(contacts)

    def get_page(self, page: int = 1) -> List[Contact]:
        """Возвращает контакты для указанной страницы"""
        contacts = self._read_contacts()
        start = (page - 1) * self.page_size
        return contacts[start:start + self.page_size]

    def search(self, query: str) -> List[Contact]:
        """Поиск контактов"""
        query = query.lower()
        return [contact for contact in self._read_contacts()
                if query in str(contact).lower()]

    def edit(self, index: int, new_contact: Contact) -> bool:
        """Редактирует контакт по индексу"""
        contacts = self._read_contacts()
        if 0 <= index < len(contacts):
            contacts[index] = new_contact
            self._save_contacts(contacts)
            return True
        return False
