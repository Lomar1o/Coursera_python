import os
import csv


class CarBase:
    required = []

    def __init__(self, brand, photo_file_name, carrying):
        self.photo_file_name = self.validate_photo_name(photo_file_name)
        self.brand = self.validate_value(brand)
        self.carrying = float(self.validate_value(carrying))

    def validate_value(self, value):
        if value == '':
            raise ValueError
        return value

    def validate_photo_name(self, photo_file_name):
        formats = ('.jpg', '.jpeg', '.png', '.gif')
        if os.path.splitext(photo_file_name)[1] in formats:
            return photo_file_name
        raise ValueError

    @classmethod
    def create_from_dict(cls, data):
        parametrs = [data[parametr] for parametr in cls.required]
        return cls(*parametrs)

    def get_photo_file_ext(self):
        formats = ('.jpg', '.jpeg', '.png', '.gif')
        if os.path.splitext(self.photo_file_name)[1] in formats:
            return os.path.splitext(self.photo_file_name)[1]


class Car(CarBase):
    required = ['brand', 'photo_file_name', 'carrying', 'passenger_seats_count']

    def __init__(self, brand, photo_file_name, carrying, passenger_seats_count):
        super().__init__(brand, photo_file_name, carrying)
        self.passenger_seats_count = int(self.validate_value(passenger_seats_count))
        self.car_type = 'car'


class Truck(CarBase):
    required = ['brand', 'photo_file_name', 'carrying', 'body_whl']

    def __init__(self, brand, photo_file_name, carrying, body_whl):
        super().__init__(brand, photo_file_name, carrying)
        self.car_type = 'truck'
        try:
            self.body_length = float(body_whl[:body_whl.find('x')])
            self.body_width = float(body_whl[body_whl.find('x')+1:body_whl.rfind('x')])
            self.body_height = float(body_whl[body_whl.rfind('x')+1:])
        except ValueError:
            self.body_length = float(0)
            self.body_width = float(0)
            self.body_height = float(0)

    def get_body_volume(self):
        return self.body_length * self.body_width * self.body_height


class SpecMachine(CarBase):
    required = ['brand', 'photo_file_name', 'carrying', 'extra']

    def __init__(self, brand, photo_file_name, carrying, extra):
        super().__init__(brand, photo_file_name, carrying)
        self.extra = self.validate_value(extra)
        self.car_type = 'spec_machine'


def get_car_list(csv_filename):
    car_list = []
    csv.register_dialect('cars', delimiter=';')
    car_types = {'car': Car, 'spec_machine': SpecMachine, 'truck': Truck}
    with open(csv_filename, 'r') as f:
        reader = csv.DictReader(f, dialect='cars')
        for row in reader:
            try:
                car_class = car_types[row['car_type']]
                car_list.append(car_class.create_from_dict(row))
            except Exception:
                pass
    return car_list


if __name__ == '__main__':
    print(get_car_list('Car.csv'))
