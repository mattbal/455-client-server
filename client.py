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

# create socket and connect to server
s = socket.socket()
s.connect((socket.gethostname(), 6001))

while True:
    message_type = get_message_type()

    if (message_type == 3):
        break
    elif (message_type == 2):
        print("Enter file name:")

    message = input(' -> ')
    if not message: continue # if user inputted nothing, go to next iteration of loop

    # Send message
    if (message_type == 1):
        s.send(message.encode())
    elif (message_type == 2):
        filename = os.path.basename(message)
        size = os.path.getsize(message)
        s.send(f'\.-SENDING FILE-./,{filename},{size}'.encode())

        confirmation_message = s.recv(4096).decode()
        print(f'Server: {confirmation_message}')

        file = open(message, 'rb')
        data = file.read()
        s.send(data)

        confirmation_message = s.recv(4096).decode()
        print(f'Server: {confirmation_message}')
        file.close()


    # Receive data from server
    message = s.recv(4096).decode()
    if not message: break

    if message.startswith("\.-SENDING FILE-./"):
        print("Server started sending a file...")
        tokens = message.split(',')
        filename = tokens[1]
        size = tokens[2]
        print(size)
        try:
            size = int(size)
        except ValueError:
            print("size was not sent correctly")
            continue # skip to next iteration of loop

        s.send('Thanks for the file information!'.encode())

        file = open(filename, 'wb')
        data = s.recv(size, socket.MSG_WAITALL)
        file.write(data)
        file.close()
        
        s.send('I got the file!\n'.encode())
        print(f'Received file {filename} from server.\n')
    else:
        print('Server: ', message, '\n')
  

s.close()

