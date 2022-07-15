'''
This program deals with the client program using async I/O
--------
When the connection has been established the
user commands are executed as per the User_service
--------
The connection is closed based on the user request
'''
import asyncio

async def Client_User_TCP_echo():
    '''
    This function establishes the connection with the server
    '''
    read_msg, write_msg = await asyncio.open_connection(
        '127.0.0.1', 8080)
    request_msg = ''
    while True:
        request_msg = input('please enter your command::')
        if request_msg == "":
            print("Please enter the correct command\n")
            continue
        write_msg.write(request_msg.encode())
        data = await read_msg.read(4096)
        print(f'Received: {data.decode()}')
        if request_msg.lower() == "quit":
            break
    print('Close the connection')
    write_msg.close()

asyncio.run(Client_User_TCP_echo())
