from typing import Dict, Type


class InfoMessage:
    """Информационное сообщение о тренировке."""

    def __init__(self,
                 training_type: str,
                 duration: float,
                 distance: float,
                 speed: float,
                 calories: float
                 ) -> None:
        self.training_type = training_type
        self.duration = duration
        self.distance = distance
        self.speed = speed
        self.calories = calories

    def get_message(self) -> str:
        return (f'Тип тренировки: {self.training_type}; '
                f'Длительность: {self.duration:.3f} ч.; '
                f'Дистанция: {self.distance:.3f} км; '
                f'Ср. скорость: {self.speed:.3f} км/ч; '
                f'Потрачено ккал: {self.calories:.3f}.')


class Training:
    """Базовый класс тренировки."""

    weight: float
    LEN_STEP: float = 0.65
    M_IN_KM: float = 1000
    TRAINING_TIME_MINUTES: float = 60

    def __init__(self,
                 action: float,
                 duration: float,
                 weight: float,
                 ) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        pass

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(self.__class__.__name__,
                           self.duration,
                           self.get_distance(),
                           self.get_mean_speed(),
                           self.get_spent_calories()
                           )


class Running(Training):
    """Тренировка: бег."""

    COEFF_MEAN_SPEED_1: float = 18
    COEFF_MEAN_SPEED_2: float = 20

    def get_spent_calories(self) -> float:
        return((self.COEFF_MEAN_SPEED_1 * self.get_mean_speed()
               - self.COEFF_MEAN_SPEED_2)
               * self.weight / self.M_IN_KM
               * self.duration * self.TRAINING_TIME_MINUTES)


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""

    WEIGHT_COEFF_1: float = 0.035
    WEIGHT_COEFF_2: float = 0.029
    EXPONENT: float = 2

    def __init__(self,
                 action: float,
                 duration: float,
                 weight: float,
                 height: float) -> None:
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        return((self.WEIGHT_COEFF_1 * self.weight
               + (self.get_mean_speed() ** self.EXPONENT // self.height)
               * self.WEIGHT_COEFF_2 * self.weight)
               * self.duration * self.TRAINING_TIME_MINUTES)


class Swimming(Training):
    """Тренировка: плавание."""

    COEFF_MEAN_SPEED: float = 1.1
    WEIGHT_COEFF: float = 2
    LEN_STEP: float = 1.38

    def __init__(self,
                 action: float,
                 duration: float,
                 weight: float,
                 length_pool: float,
                 count_pool: float) -> None:
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self) -> float:
        return(self.length_pool * self.count_pool
               / self.M_IN_KM / self.duration)

    def get_spent_calories(self) -> float:
        return((self.get_mean_speed() + self.COEFF_MEAN_SPEED)
               * self.WEIGHT_COEFF * self.weight)


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    training_types: Dict[str, Type[Training]] = {
        'SWM': Swimming,
        'RUN': Running,
        'WLK': SportsWalking
    }
    if workout_type not in training_types:
        raise ValueError(f'Значения ключа {workout_type} нет в словаре')
    return training_types[workout_type](*data)


def main(training: Training) -> None:
    """Главная функция."""
    return print(training.show_training_info().get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        main(read_package(workout_type, data))
