'''
This program is used for the server 
--------
'''
import asyncio
import signal
from User_service import Client_User

signal.signal(signal.SIGINT, signal.SIG_DFL)

def server_function(current_user, cmd_msg):
    '''
    This function deals with the funtion commands used in the user_service program
    '''
    cmd_msg = cmd_msg.rstrip("\n").rstrip(" ").lstrip(" ")
    if cmd_msg.split(" ")[0] == "commands":
        return current_user.commands()
    if cmd_msg.split(" ")[0] == "register":
        if len(cmd_msg.split(" ")) == 3:
            return current_user.register(cmd_msg.split(" ")[1], cmd_msg.split(" ")[2])
        return "command you entered is invalid"
    if cmd_msg.split(" ")[0] == "quit":
        return current_user.quit()
    if cmd_msg.split(" ")[0] == "login":
        if len(cmd_msg.split(" ")) == 3:
            return current_user.login(cmd_msg.split(" ")[1], cmd_msg.split(" ")[2])
        return "command you entered is invalid"
    if cmd_msg.split(" ")[0] == "list":
        return current_user.list()
    if cmd_msg.split(" ")[0] == "change_folder":
        if len(cmd_msg.split(" ")) == 2:
            return current_user.change_folder(cmd_msg.split(" ")[1])
        return "command you entered is invalid"
    if cmd_msg.split(" ")[0] == "read_file":
        if len(cmd_msg.split(" ")) == 2:
            return current_user.read_file(cmd_msg.split(" ")[1])
        return "command you entered is invalid"
    if cmd_msg.split(" ")[0] == "write_file":
        if len(cmd_msg.split(" ")) >= 2:
            return current_user.write_file(cmd_msg.split(" ")[1], " ".join(cmd_msg.split(" ")[2:]))
        return "command you entered is invalid"
    if cmd_msg.split(" ")[0] == "create_folder":
        if len(cmd_msg.split(" ")) == 2:
            return current_user.create_folder(cmd_msg.split(" ")[1])
        return "command you entered is invalid"
    return "command you entered is invalid"



async def message_handle(reader, writer):
    '''
    This funtion deals with the connection from the client,
    and tells the acknowledgement messages from the client
    '''
    port_address = writer.get_extra_info('peername')
    send_msg = f"{port_address} is connected !!!!"
    print(send_msg)
    client = Client_User()
    while True:
        data = await reader.read(4096)
        send_msg = data.decode().strip()
        if send_msg == 'exit':
            break

        print(f"Received {send_msg} from {port_address}")
        mymsg = server_function(client, send_msg)
        msg = str(mymsg).encode()
        writer.write(msg)
        await writer.drain()
    print("Connection has been lost")
    writer.close()


async def main():
    '''
    This function deals with the connection between the server and client
    '''
    service_message = await asyncio.start_server(
        message_handle, '127.0.0.1', 8080)


    port_address = service_message.sockets[0].getsockname()
    print(f'Serving on the address and port{port_address}')

    async with service_message:
        await service_message.serve_forever()


asyncio.run(main())
