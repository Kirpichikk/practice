import asyncio
import logging
import time
from creation_data.creation_test_data_cache import creation_data
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


async def insert_job(conn, task_id, records_per_task, data_set, space_name):
    """Асинхронная вставка данных с использованием готового набора данных"""
    start_id = task_id * records_per_task
    data_size = len(data_set)

    for i in range(records_per_task):
        record_id = start_id + i
        # Циклический выбор данных из набора
        data_index = record_id % data_size
        record_data = data_set[data_index]

        try:
            # ИСПРАВЛЕНО: правильный формат вставки данных
            await conn.insert(space_name, record_data)
        except Exception as e:
            logger.error(f"Ошибка вставки записи {record_id}: {e}")


async def main_cache1():
    """Основная асинхронная функция"""
    # Подключение к Tarantool
    conn = await create_connection()
    if not conn:
        return

    # Получаем тестовые данные
    try:
        # ИСПРАВЛЕНО: используем функцию создания тестовых данных
        test_data = creation_data(1)
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
        # ИСПРАВЛЕНО: правильный формат вызова truncate
        await conn.eval('box.space.cache1:truncate()')
        logger.info("Пространство 'cache1' очищено")
    except Exception as e:
        logger.warning(f"Не удалось очистить пространство: {e}")

    # Создаем задачи
    tasks = []
    start_time = time.monotonic()

    for task_id in range(num_tasks):
        task = asyncio.create_task(
            insert_job(conn, task_id, records_per_task, test_data, "cache1")
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

async def main_cache2():
    """Основная асинхронная функция"""
    # Подключение к Tarantool
    conn = await create_connection()
    if not conn:
        return

    # Получаем тестовые данные
    try:
        # ИСПРАВЛЕНО: используем функцию создания тестовых данных
        test_data = creation_data(2)
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
        # ИСПРАВЛЕНО: правильный формат вызова truncate
        await conn.eval('box.space.cache2:truncate()')
        logger.info("Пространство 'cache2' очищено")
    except Exception as e:
        logger.warning(f"Не удалось очистить пространство: {e}")

    # Создаем задачи
    tasks = []
    start_time = time.monotonic()

    for task_id in range(num_tasks):
        task = asyncio.create_task(
            insert_job(conn, task_id, records_per_task, test_data, "cache2")
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
    asyncio.run(main_cache1())
    asyncio.run(main_cache2())