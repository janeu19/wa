import asyncio
import websockets

PORT = 8080

connected_clients = {}
banned_ips = {}
unban_time = 10
client_id = 1


async def handle_client(websocket, path):
    global client_id

    client_ip = websocket.remote_address[0]
    print(f"Incoming IP: {client_ip}, current ID: {client_id}")

    # Zkontroluje, zda je klient blokován.
    if client_ip in banned_ips:
        if not check_if_unban(client_ip):
            return

        # Odešle klientovi zprávu, že byl odblokován.
        await websocket.send("SERVER_MESSAGE: Unbanned.")

    # Přidá klienta do seznamu připojených klientů.
    connected_clients[client_id] = websocket
    client_id += 1

    try:
        async for message in websocket:
            print(f"Received message from client: {message}")

            # Zkontroluje, zda klient odeslal zakázané slovo.
            if message == "pica":
                await ban(websocket)
                return

            # Zjistí ID aktuálního klienta.
            current_id = 0
            for id, client in connected_clients.items():
                if client == websocket:
                    current_id = id
                    break

            # Odešle zprávu všem připojeným klientům.
            for id, client in connected_clients.items():
                print(f"Sending to {id}")
                await client.send(f"{current_id} said: {message}")
    except websockets.exceptions.ConnectionClosed as e:
        print("A client just disconnected")
    finally:
        await disconnect(websocket)


async def disconnect(websocket):
    print("Disconnected")

    # Odstraní klienta ze seznamu připojených klientů.
    for id, client in connected_clients.items():
        if client == websocket:
            del connected_clients[id]
            break

    # Zavře připojení klienta.
    await websocket.close()


async def ban(websocket):
    print("Banned")

    # Odešle klientovi zprávu, že byl blokován.
    await websocket.send("SERVER_MESSAGE: Banned.")

    # Přidá klienta do seznamu blokovaných ip adres.
    banned_ips[websocket.remote_address[0]] = time.time()

    # Odstraní klienta ze seznamu připojených klientů.
    await disconnect(websocket)


def check_if_unban(client_ip):
    if time.time() - banned_ips[client_ip] > unban_time:
        del banned_ips[client_ip]
        print(f"Unbanned: {client_ip}")
        return True

    return False


if __name__ == "__main__":
    start_server = websockets.serve(handle_client, "0.0.0.0", PORT)
    asyncio.get_event_loop().run_until_complete(start_server)
    asyncio.get_event_loop().run_forever()
