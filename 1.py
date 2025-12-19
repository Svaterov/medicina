import json
import os
from datetime import datetime
from dataclasses import dataclass, asdict
from typing import List, Optional
import sys

@dataclass
class Patient:
    """Класс для представления пациента"""
    id: int
    last_name: str
    first_name: str
    middle_name: Optional[str]
    birth_date: str
    gender: str
    address: str
    phone: str
    email: Optional[str]
    insurance_number: str
    registration_date: str
    medical_history: str
    diagnosis: str
    attending_doctor: str
    
    def display_info(self):
        """Вывод информации о пациенте"""
        print(f"\n{'='*50}")
        print(f"ПАЦИЕНТ: {self.last_name} {self.first_name} {self.middle_name or ''}")
        print(f"{'='*50}")
        print(f"ID: {self.id}")
        print(f"Дата рождения: {self.birth_date}")
        print(f"Пол: {self.gender}")
        print(f"Адрес: {self.address}")
        print(f"Телефон: {self.phone}")
        print(f"Email: {self.email or 'Не указан'}")
        print(f"Страховой номер: {self.insurance_number}")
        print(f"Дата регистрации: {self.registration_date}")
        print(f"История болезни: {self.medical_history}")
        print(f"Диагноз: {self.diagnosis}")
        print(f"Лечащий врач: {self.attending_doctor}")
        print(f"{'='*50}")

class ClinicManagementSystem:
    """Система управления клиникой"""
    
    def __init__(self, filename="patients.json"):
        self.filename = filename
        self.patients = []
        self.load_patients()
    
    def load_patients(self):
        """Загрузка пациентов из файла"""
        try:
            if os.path.exists(self.filename):
                with open(self.filename, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.patients = [Patient(**patient) for patient in data]
                print(f"Загружено {len(self.patients)} пациентов")
            else:
                self.patients = []
        except Exception as e:
            print(f"Ошибка при загрузке данных: {e}")
            self.patients = []
    
    def save_patients(self):
        """Сохранение пациентов в файл"""
        try:
            with open(self.filename, 'w', encoding='utf-8') as f:
                json.dump([asdict(patient) for patient in self.patients], 
                         f, ensure_ascii=False, indent=2)
            print(f"Данные сохранены. Всего пациентов: {len(self.patients)}")
        except Exception as e:
            print(f"Ошибка при сохранении данных: {e}")
    
    def get_next_id(self):
        """Получение следующего ID для пациента"""
        if not self.patients:
            return 1
        return max(patient.id for patient in self.patients) + 1
    
    def add_patient(self):
        """Добавление нового пациента"""
        print("\n=== ДОБАВЛЕНИЕ НОВОГО ПАЦИЕНТА ===")
        
        try:
            patient = Patient(
                id=self.get_next_id(),
                last_name=input("Фамилия: ").strip(),
                first_name=input("Имя: ").strip(),
                middle_name=input("Отчество (если есть): ").strip() or None,
                birth_date=input("Дата рождения (ДД.ММ.ГГГГ): ").strip(),
                gender=self.select_gender(),
                address=input("Адрес: ").strip(),
                phone=input("Телефон: ").strip(),
                email=input("Email (необязательно): ").strip() or None,
                insurance_number=input("Страховой номер: ").strip(),
                registration_date=datetime.now().strftime("%d.%m.%Y %H:%M"),
                medical_history=input("История болезни: ").strip(),
                diagnosis=input("Предварительный диагноз: ").strip(),
                attending_doctor=input("Лечащий врач: ").strip()
            )
            
            self.patients.append(patient)
            self.save_patients()
            print(f"\n✓ Пациент успешно добавлен (ID: {patient.id})")
            
        except Exception as e:
            print(f"Ошибка при добавлении пациента: {e}")
    
    def select_gender(self):
        """Выбор пола пациента"""
        while True:
            print("Выберите пол:")
            print("1 - Мужской")
            print("2 - Женский")
            choice = input("Ваш выбор: ").strip()
            
            if choice == "1":
                return "Мужской"
            elif choice == "2":
                return "Женский"
            else:
                print("Неверный выбор. Попробуйте снова.")
    
    def find_patient(self):
        """Поиск пациента"""
        print("\n=== ПОИСК ПАЦИЕНТА ===")
        print("1 - Поиск по фамилии")
        print("2 - Поиск по ID")
        print("3 - Поиск по страховому номеру")
        print("4 - Поиск по телефону")
        
        choice = input("Выберите тип поиска: ").strip()
        search_term = input("Введите значение для поиска: ").strip().lower()
        
        found_patients = []
        
        if choice == "1":
            found_patients = [p for p in self.patients 
                            if search_term in p.last_name.lower()]
        elif choice == "2":
            try:
                search_id = int(search_term)
                found_patients = [p for p in self.patients if p.id == search_id]
            except ValueError:
                print("ID должен быть числом!")
        elif choice == "3":
            found_patients = [p for p in self.patients 
                            if search_term in p.insurance_number.lower()]
        elif choice == "4":
            found_patients = [p for p in self.patients 
                            if search_term in p.phone.lower()]
        else:
            print("Неверный выбор!")
            return
        
        if found_patients:
            print(f"\nНайдено пациентов: {len(found_patients)}")
            for patient in found_patients:
                patient.display_info()
        else:
            print("\nПациенты не найдены!")
    
    def edit_patient(self):
        """Редактирование данных пациента"""
        print("\n=== РЕДАКТИРОВАНИЕ ДАННЫХ ПАЦИЕНТА ===")
        
        try:
            patient_id = int(input("Введите ID пациента для редактирования: ").strip())
            patient = next((p for p in self.patients if p.id == patient_id), None)
            
            if not patient:
                print("Пациент с таким ID не найден!")
                return
            
            patient.display_info()
            
            print("\nКакие данные вы хотите изменить?")
            print("1 - Личные данные (ФИО, дата рождения, пол)")
            print("2 - Контактные данные (адрес, телефон, email)")
            print("3 - Медицинские данные")
            print("4 - Все данные")
            
            choice = input("Ваш выбор: ").strip()
            
            if choice in ["1", "4"]:
                patient.last_name = input(f"Фамилия [{patient.last_name}]: ").strip() or patient.last_name
                patient.first_name = input(f"Имя [{patient.first_name}]: ").strip() or patient.first_name
                patient.middle_name = input(f"Отчество [{patient.middle_name or ''}]: ").strip() or patient.middle_name
                patient.birth_date = input(f"Дата рождения [{patient.birth_date}]: ").strip() or patient.birth_date
                if input("Изменить пол? (да/нет): ").strip().lower() == "да":
                    patient.gender = self.select_gender()
            
            if choice in ["2", "4"]:
                patient.address = input(f"Адрес [{patient.address}]: ").strip() or patient.address
                patient.phone = input(f"Телефон [{patient.phone}]: ").strip() or patient.phone
                patient.email = input(f"Email [{patient.email or ''}]: ").strip() or patient.email
                patient.insurance_number = input(f"Страховой номер [{patient.insurance_number}]: ").strip() or patient.insurance_number
            
            if choice in ["3", "4"]:
                patient.medical_history = input(f"История болезни [{patient.medical_history}]: ").strip() or patient.medical_history
                patient.diagnosis = input(f"Диагноз [{patient.diagnosis}]: ").strip() or patient.diagnosis
                patient.attending_doctor = input(f"Лечащий врач [{patient.attending_doctor}]: ").strip() or patient.attending_doctor
            
            self.save_patients()
            print("✓ Данные пациента обновлены!")
            
        except ValueError:
            print("ID должен быть числом!")
        except Exception as e:
            print(f"Ошибка при редактировании: {e}")
    
    def delete_patient(self):
        """Удаление пациента"""
        print("\n=== УДАЛЕНИЕ ПАЦИЕНТА ===")
        
        try:
            patient_id = int(input("Введите ID пациента для удаления: ").strip())
            patient = next((p for p in self.patients if p.id == patient_id), None)
            
            if not patient:
                print("Пациент с таким ID не найден!")
                return
            
            patient.display_info()
            
            confirm = input("\nВы уверены, что хотите удалить этого пациента? (да/нет): ").strip().lower()
            
            if confirm == "да":
                self.patients = [p for p in self.patients if p.id != patient_id]
                self.save_patients()
                print("✓ Пациент удален!")
            else:
                print("Удаление отменено.")
                
        except ValueError:
            print("ID должен быть числом!")
        except Exception as e:
            print(f"Ошибка при удалении: {e}")
    
    def display_all_patients(self):
        """Отображение всех пациентов"""
        print(f"\n=== ВСЕ ПАЦИЕНТЫ (всего: {len(self.patients)}) ===")
        
        if not self.patients:
            print("Нет зарегистрированных пациентов.")
            return
        
        # Сортировка по фамилии
        sorted_patients = sorted(self.patients, key=lambda x: x.last_name)
        
        print(f"\n{'ID':<5} {'ФИО':<30} {'Дата рождения':<15} {'Телефон':<15} {'Лечащий врач':<20}")
        print("-" * 90)
        
        for patient in sorted_patients:
            full_name = f"{patient.last_name} {patient.first_name[0]}.{patient.middle_name[0] + '.' if patient.middle_name else ''}"
            print(f"{patient.id:<5} {full_name:<30} {patient.birth_date:<15} {patient.phone:<15} {patient.attending_doctor:<20}")
    
    def display_statistics(self):
        """Отображение статистики"""
        print("\n=== СТАТИСТИКА КЛИНИКИ ===")
        
        if not self.patients:
            print("Нет данных для статистики.")
            return
        
        total = len(self.patients)
        male_count = len([p for p in self.patients if p.gender == "Мужской"])
        female_count = len([p for p in self.patients if p.gender == "Женский"])
        
        # Группировка по лечащим врачам
        doctors = {}
        for patient in self.patients:
            doctors[patient.attending_doctor] = doctors.get(patient.attending_doctor, 0) + 1
        
        print(f"Всего пациентов: {total}")
        print(f"Мужчин: {male_count} ({male_count/total*100:.1f}%)")
        print(f"Женщин: {female_count} ({female_count/total*100:.1f}%)")
        
        print("\nРаспределение по врачам:")
        for doctor, count in sorted(doctors.items(), key=lambda x: x[1], reverse=True):
            print(f"  {doctor}: {count} пациентов ({count/total*100:.1f}%)")
    
    def display_menu(self):
        """Отображение главного меню"""
        print("\n" + "="*50)
        print("СИСТЕМА УЧЕТА ПАЦИЕНТОВ МЕДИЦИНСКОЙ КЛИНИКИ")
        print("="*50)
        print("1 - Просмотр всех пациентов")
        print("2 - Добавить нового пациента")
        print("3 - Найти пациента")
        print("4 - Редактировать данные пациента")
        print("5 - Удалить пациента")
        print("6 - Показать статистику")
        print("7 - Сохранить данные")
        print("8 - Загрузить данные")
        print("0 - Выход")
        print("="*50)
    
    def run(self):
        """Запуск приложения"""
        print("Добро пожаловать в систему учета пациентов!")
        
        while True:
            self.display_menu()
            
            try:
                choice = input("\nВыберите действие: ").strip()
                
                if choice == "1":
                    self.display_all_patients()
                elif choice == "2":
                    self.add_patient()
                elif choice == "3":
                    self.find_patient()
                elif choice == "4":
                    self.edit_patient()
                elif choice == "5":
                    self.delete_patient()
                elif choice == "6":
                    self.display_statistics()
                elif choice == "7":
                    self.save_patients()
                elif choice == "8":
                    self.load_patients()
                elif choice == "0":
                    print("Сохранение данных...")
                    self.save_patients()
                    print("До свидания!")
                    break
                else:
                    print("Неверный выбор. Попробуйте снова.")
                
                input("\nНажмите Enter для продолжения...")
                
            except KeyboardInterrupt:
                print("\n\nПрограмма прервана пользователем.")
                self.save_patients()
                break
            except Exception as e:
                print(f"Произошла ошибка: {e}")
                input("Нажмите Enter для продолжения...")

def main():
    """Точка входа в приложение"""
    system = ClinicManagementSystem()
    
    # Создание тестовых данных, если файл пустой
    if not os.path.exists(system.filename) or len(system.patients) == 0:
        print("Создание базы данных...")
        # Можно добавить тестовые данные здесь при необходимости
    
    try:
        system.run()
    except Exception as e:
        print(f"Критическая ошибка: {e}")
        input("Нажмите Enter для выхода...")

if __name__ == "__main__":
    main()