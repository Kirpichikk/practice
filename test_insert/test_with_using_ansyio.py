import asyncio
import logging
import time
from asynctnt import Connection  # Асинхронный клиент для Tarantool

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


async def insert_job(conn, task_id, records_per_task):
    """Асинхронная вставка данных"""
    start_id = task_id * records_per_task
    for i in range(records_per_task):
        record_id = start_id + i
        try:
            await conn.insert(
                "users",
                (record_id,
                 'session_12345',
                 '250011223344550',
                 '+79123456789',
                 'user@domain.com',
                 ['192.168.1.100', '10.0.0.1'],  # Используем списки вместо кортежей
                 ['2001:db8::/64', '2001:db8:1::/64'],
                 '00-11-22-33-44-55')
            )
        except Exception as e:
            logger.error(f"Ошибка вставки записи {record_id}: {e}")


async def main():
    """Основная асинхронная функция"""
    # Подключение к Tarantool
    conn = await create_connection()
    if not conn:
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
    for task_id in range(num_tasks):
        task = asyncio.create_task(insert_job(conn, task_id, records_per_task))
        tasks.append(task)

    # Замер времени выполнения
    start_time = time.monotonic()
    await asyncio.gather(*tasks)
    end_time = time.monotonic()

    # Закрываем соединение
    await conn.disconnect()

    # Выводим результаты
    elapsed = end_time - start_time
    print(f"\nРезультаты:")
    print(f"Всего записей: {total_records}")
    print(f"Общее время: {elapsed:.2f} секунд")
    print(f"Скорость вставки: {total_records / elapsed:.2f} записей/сек")


if __name__ == "__main__":
    asyncio.run(main())