import asyncio
import logging
import time
from creation_test_data import creation_data
from asynctnt import Connection

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


async def create_connection():
    try:
        conn = Connection(host='127.0.0.1', port=3301)
        await conn.connect()
        logger.info("Успешное подключение к Tarantool")
        return conn
    except Exception as e:
        logger.error(f"Ошибка подключения: {e}")
        return None


async def insert_job(conn, task_id, records_per_task, data_set):
    """Асинхронная вставка данных с использованием готового набора данных"""
    start_id = task_id * records_per_task
    data_size = len(data_set)

    for i in range(records_per_task):
        record_id = start_id + i
        # Циклический выбор данных из набора
        data_index = record_id % data_size
        record_data = data_set[data_index]

        try:
            # Вставляем данные с автоматически сгенерированным ID
            await conn.insert(
                "users",
                (record_id, *record_data)
            )
        except Exception as e:
            logger.error(f"Ошибка вставки записи {record_id}: {e}")


async def main():
    """Основная асинхронная функция"""
    # Подключение к Tarantool
    conn = await create_connection()
    if not conn:
        return

    # Получаем тестовые данные
    try:
        test_data = creation_data()
        logger.info(f"Получено {len(test_data)} записей тестовых данных")
    except Exception as e:
        logger.error(f"Ошибка получения тестовых данных: {e}")
        await conn.disconnect()
        return

    # Параметры теста
    num_tasks = 40
    records_per_task = 2500
    total_records = num_tasks * records_per_task

    # Подготовка пространства (очистка)
    try:
        await conn.call('box.space.users:truncate')
        logger.info("Пространство 'users' очищено")
    except Exception as e:
        logger.warning(f"Не удалось очистить пространство: {e}")

    # Создаем задачи
    tasks = []
    start_time = time.monotonic()

    for task_id in range(num_tasks):
        task = asyncio.create_task(
            insert_job(conn, task_id, records_per_task, test_data)
        )
        tasks.append(task)

    # Ожидаем завершения всех задач
    await asyncio.gather(*tasks)
    end_time = time.monotonic()

    # Закрываем соединение
    await conn.disconnect()

    # Выводим результаты
    elapsed = end_time - start_time
    logger.info("\nРезультаты:")
    logger.info(f"Всего записей: {total_records}")
    logger.info(f"Общее время: {elapsed:.2f} секунд")
    logger.info(f"Скорость вставки: {total_records / elapsed:.2f} записей/сек")


if __name__ == "__main__":
    asyncio.run(main())