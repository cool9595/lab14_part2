import asyncio

async def test_client(msg):
    reader, writer = await asyncio.open_connection('127.0.0.1', 9095)
    
    writer.write(msg.encode())
    await writer.drain()
    
    data = await reader.read(1024)
    writer.close()
    await writer.wait_closed()
    
    print(f"Клиент получил: {data.decode().strip()}")

async def main():
    tasks = [
        test_client("Hello from client 1!\n"),
        test_client("Hello from client 2!\n"),
        test_client("Hello from client 3!\n")
    ]
    await asyncio.gather(*tasks)


if __name__ == '__main__':
    try:
        print("--- Один клиент ---")
        asyncio.run(main())

        print("\n--- Несколько клиентов одновременно ---")
        asyncio.run(main_multiple())
    except ConnectionRefusedError:
        print("\nОшибка: не удалось подключиться к серверу.")
        print("Убедитесь, что сервер 02_echo_server.py запущен в другом терминале.")
