import socket
import os

def get_message_type():
  while True:
      print("--- Menu ---")
      print("1. Send text message")
      print("2. Send file")
      print("3. Quit")
      message_type = input()

      # Try converting the user's input selection to a number
      try:
        message_type = int(message_type)
        return message_type
      except ValueError:
        print(f'{message_type} is not a number\n')    

# create socket
s = socket.socket()
s.bind((socket.gethostname(), 6001))

s.listen()

conn, address = s.accept()

while True:
    # Receive data from client
    message = conn.recv(4096).decode()
    if not message: break

    if message.startswith("\.-SENDING FILE-./"):
        print("Client started sending a file...")
        tokens = message.split(',')
        filename = tokens[1]
        size = tokens[2]
        try:
            size = int(size)
        except ValueError:
            print("size was not sent correctly")
            continue # skip to next iteration of loop

        conn.send('I successfully received the file information'.encode())

        file = open(filename, 'wb')
        data = conn.recv(size, socket.MSG_WAITALL)
        file.write(data)
        file.close()
        
        conn.send('I successfully saved the file\n'.encode())
        print(f'Received file {filename} from client.\n')
    else:
        print('Client: ', message, '\n')
  

    # Send data
    message_type = get_message_type()

    if (message_type == 3):
        break
    elif (message_type == 2):
        print("Enter file name:")

    message = input(' -> ')
    if not message: continue # if user inputted nothing, go to next iteration of loop

    # Send message
    if (message_type == 1):
        conn.send(message.encode())
    elif (message_type == 2):
        filename = os.path.basename(message)
        size = os.path.getsize(message)
        print(size)
        conn.send(f'\.-SENDING FILE-./,{filename},{size}'.encode())

        confirmation_message = conn.recv(4096).decode()
        print(f'Client: {confirmation_message}')

        file = open(message, 'rb')
        data = file.read()
        conn.send(data)

        confirmation_message = conn.recv(4096).decode()
        print(f'Client: {confirmation_message}')
        file.close()


conn.close()
s.close()