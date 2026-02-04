import sqlite3
import pyperclip 

NOTE = 'note.db'

def main():
    while True:
        print('----------note app----------')
        print()
        print('Show all notes <1>')
        print('Show specific note <2>')
        print('Create note <3>')
        print('Update note <4>')
        print('Delete note <5>')
        print('NUKE <q>')
        x = input('Enter: ').lower()
        match x:
            case '1':
                pprint(show())
            case '2':
                show(input('Enter note name: '))
            case '3':
                ask()
            case '4':
                update()
            case '5':
                delete()
            case 'q':
                return 0
            case _:
                print('Unkown arguments')

def delete():
    print('----------delete note-----------')
    show()
    try:
        db = sqlite3.connect(NOTE)
        cr = db.cursor()
        x = input('Enter note name to delete: ')
        cr.execute(f'DELETE from Main where name="{x}"')
        db.commit()
        db.close()
    except db.Error as e:
        print(e)


def update():
    print('----------Edit mode---------')
    name = input('Enter note name to edit: ')
    show(name,ys=False)
    new_name = input('Press enter to keep the old name: ')

    db = sqlite3.connect(NOTE)
    cr = db.cursor()
    try:
        cr.execute('''Select * from Main''')
        x = cr.fetchall()
        for i in range(len(x)):
            if x[i][0]==name:
                pyperclip.copy(x[i][1])
                break
    except db.Error as e:
        print(e)
    db.close()
    
    new_content = input('Paste to change the content. \nPress enter to keep the old content: ')

    if new_name=='' and new_content=='':
        db = sqlite3.connect(NOTE)
        cr = db.cursor()
        db.close()
        return 0 
    elif not new_name=='' and not new_content=='':
        db = sqlite3.connect(NOTE)
        cr = db.cursor()
        cr.execute('''update Main set name=?, content=? where name=?''', (new_name, new_content, name))
        db.commit()
        db.close()
        show(new_name)
        return 0
    elif not new_name=='':
        db = sqlite3.connect(NOTE)
        cr = db.cursor()
        cr.execute('''UPDATE Main set name = ? where name = ?''', (new_name, name))
        db.commit()
        db.close()
        show(new_name)
        return 0
    elif not new_content=='':
        db = sqlite3.connect(NOTE)
        cr = db.cursor()
        cr.execute('''UPDATE Main set content = ? where name = ?''' ,(new_content, name))
        db.commit()
        db.close()
        show(name)
        return 0


def pprint(ls):
    print('----------name, content----------')
    print()
    for x in range(len(ls)):
        print(f"name: {ls[x][0]}")
        print(f"content: {ls[x][1]}")
        print()

def add(name, content):
    db = sqlite3.connect(NOTE)
    db.execute("create table if not exists main(name text, content text)")
    cr = db.cursor()
    try: 
        cr.execute(f'insert into main(name, content) values("{name}", "{content}")')
        db.commit()
    except sqlite3.Error as e:
        print(e, 'in add')
    db.close()

def delte(name):
    db = sqlite3.connect(NOTE)
    cr = db.cursor()
    cr.execute('SELECT from main')

def show(y='',ys=True):
    db = sqlite3.connect(NOTE)
    cr = db.cursor()
    try: 
        cr.execute('SELECT * from Main')
        x = cr.fetchall()
    except db.Error as e:
        print(e, 'in show')
    else:
        if not y == '':
            for i in range(len(x)):
                if y == x[i][0]:
                    print()
                    if ys:print('----------name, content----------')
                    print(f"name: {x[i][0]}")
                    print(f"content: {x[i][1]}")
                    print()
                    return 0
        return x

    


def ask():
    name = input('Please Enter note name: ')
    content = input('Please Enter note content: ')
    add(name, content)





    



if __name__=='__main__':
    main()


