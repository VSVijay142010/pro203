from os import remove
import socket
from threading import Thread
import random

server= socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ip_address= '127.0.0.1'
port=8000

server.bind((ip_address, port))
server.listen()

clients= []

questions=[
    "What was the first film of Harry Potter's movie series? \n a.Harry Potter and the Prisoner of Azkaban \n b.Harry Potter and the Philosopher's Stone \n c.Harry Potter and the Half-Blood Prince \n d.Harry Potter and the Order of the Phoenix",
    "Which house at Hogwarts does Harry belong to? \n a.Gryffindor \n b.Slytherin \n c.Ravenclaw \n d.Hufflepuff",
    " Lord Voldemort was from the Muggle world\n a.True \n b.False",
    " What is Harry Potter's Patronus?\n a.Horse \n b.Lion \n c.Unicorn \n d.Stag",
    " Harry Potter is a Parselmouth; what is that mean\n a.He can speak to snakes \n b.He can speak to all animals \n c.He can turn into a snake \n d.He can turn into any animal",
    "Who did save Harry, when the basilisk bit Harry? \n a.Susan Bones \n b.Fawkes the Phoenix \n c.Amycus Carrow \n d.Michael Corner",
    " What was Rita Skeeter’s magic? \n a.She turns into a werewolf \n b.She turns into a beetle \n c.She turns into a cat \n d.She turns into a owl",
    "How the wizards can do Patronus charm? \n a.By thinking about their happiest memories \n b.By thinking about their worst memories \n c.By thinking about their family \n d.By thinking about their best friends",
    " Do you know what the Thestral is?\n a.An old Pixie \n b.A cat \n c.A winged-horse \n d.A half giant",
    " What type of bag does Rita Skeeter have in the Goblet of Fire?\n a.Snake skin \n b.Crocodile Skin \n c.Hippogriff feathers\n d.Dragon Skin",
    "What shape scar does Harry have on his forehead?\n a.A cat\n b.A moon \n c.A lightening bolt \n d.A fidget spinner",
    "What is the name of Hermione Granger's cat? \n a.Bart\n b.Crookshanks \n c.Peppa \n d.Sarah",
]

answers=['b','a','a','d','a','b','b','a','c','d','c','b']

print("Server has started...")

def get_random_question_answer(conn):
    random_index= random.randint(0,len(questions)-1)
    random_question= questions[random_index]
    random_answer=answers[random_index]
    conn.send(random_question.encode('utf-8'))
    return random_index, random_question, random_answer

def remove_question(index):
    questions.pop(index)
    answers.pop(index)


def clientthread(conn):
    score=0
    conn.send('Welcome to Harry Potter quiz game!'.encode('utf-8'))
    conn.send('You will receive a question. The answer to the question would be one of a, b, c or d.'.encode('utf-8'))
    conn.send('Go and ace it!!\n\n'.encode('utf-8'))
    index, question, answer= get_random_question_answer(conn)
    print(answer)
    while True:
        try:
            message= conn.recv(2048).decode('utf-8')
            if message:
                if message.lower()==answer:
                    score+=1
                    conn.send(f"Bravo! Your score is {score}\n\n".encode('utf-8'))
                else:
                    conn.send("Incoorect answer! Better luck next time".encode('utf-8'))
                remove_question(index)
                index, question, answer= get_random_question_answer(conn)
            else:
                remove(conn)
        except:
            continue

def remove(connection):
    if connection in clients:
        clients.remove(connection)

while True:
    conn, addr= server.accept()
    clients.append(conn)
    print(addr[0]+ ' connected')

    new_thread= Thread(target=clientthread, args=(conn,addr))
    new_thread.start()