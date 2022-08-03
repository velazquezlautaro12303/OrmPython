# This is a sample Python script.

# Press Mayús+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import csv
import sqlobject as SO
from sqlobject.inheritance import InheritableSQLObject

# driver//user/password@localhost/nameDataBase
__connection__ = SO.connectionForURI("mysql://root:murcielago456@localhost/newDataBase2")


# Aca esta la herencia
class Artist(SO.SQLObject):
    name = SO.StringCol(length=120, varchar=True)
    albums = SO.RelatedJoin('Anime')

    def _set_name(self, value):
        self._SO_set_name(value.lower())

    #def _get_name(self):
        #return self._SO_get_name().upper()

class Pass(SO.SQLObject):
    password = SO.StringCol(length=120, varchar=True)
    nameUser = SO.ForeignKey("Artist", default=None)

class Anime(SO.SQLObject):
    name = SO.StringCol(length=160, varchar=True)
    artists = SO.RelatedJoin('Artist')  # relation many to many

class Persona(InheritableSQLObject):
    nombre = SO.UnicodeCol(length=50, varchar=True, notNone=True)
    apellido = SO.UnicodeCol(length=50, varchar=True, notNone=True)

class Profesor(Persona):
    titulo = SO.UnicodeCol(length=150, varchar=True, notNone=True)

class Alumno(Persona):
    carrera = SO.UnicodeCol(length=150, varchar=True, notNone=True)
    legajo  = SO.UnicodeCol(length=20, varchar=True, notNone=True)

def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    # borro la tabla si ya existia
    # __connection__.queryAll("truncate table anime_artist")
    # Pass.dropTable(ifExists=True)
    # Artist.dropTable(ifExists=True)
    # Persona.dropTable(ifExists=True)
    # Profesor.dropTable(ifExists=True)
    # Alumno.dropTable(ifExists=True)
    # Anime.dropTable(ifExists=True)

    input("Se borraron todas las tablas")

    # creo la tabla
    Artist.createTable()
    Pass.createTable()
    Persona.createTable()
    Profesor.createTable()
    Alumno.createTable()

    for n in open('Artist.txt').readlines():
        Artist(name=n.rstrip('\n'))

    reader = csv.DictReader(open("passwords.csv"), delimiter=",", quotechar='"')
    for row in reader:
        artist = Artist.selectBy(name=row['user']).getOne()
        p = Pass(password=row['pass'], nameUser=artist)

    reader = csv.DictReader(open("album.csv"), delimiter=",", quotechar='"')
    for row in reader:
        artist = Artist.selectBy(name=row['artist']).getOne()
        anime = Anime(name=row['anime'])
        artist.addAnime(anime)

    input("miremos como quedo la tabla")

    id = input("busco por id usando get(): ")
    a = Artist.get(int(id))

    print(f"El nombre es: {a.name}")

    print(a)

    #and
    #hay que agregar mas cosas para que traiga una lista? de datos
    id = input("busco por id usando selectBy(): ")
    for a in Artist.selectBy(id = int(id)):
        print(a)

    for artist in Artist.select(orderBy=Artist.q.name, limit=10):
        print(artist.name + ":")
        for pwd in Pass.select(Pass.q.nameUser == artist):
            print(pwd.password)

    for artist in Artist.select(orderBy=Artist.q.name):
        print("{} {}".format(artist.name, Pass.select(Pass.q.nameUser == artist).count()))

    # init = input("join pasar palabra que comienza el user: ")
    # for pwd in Pass.select(SO.AND(Pass.q.artistID == Artist.q.id,
    #                               Artist.q.name.startswith(init))):
    #     print(pwd.nameUser.name, pwd.password)

    init = input("join pasar palabra que comienza el user: ")
    query = "select artist.name, pass.password from artist, pass where artist.id = pass.name_user_id and artist.name like '{}%'".format(init)

    print(query)

    for row in __connection__.queryAll(query):
        print(row)

    user = Artist.selectBy(name="mayli chalco").getOne()
    user.addAnime(Anime(name="Nisekoi"))

    for artist in Artist.select(orderBy=Artist.q.name):
        print(artist.name + ":")
        for animes in artist.albums:
            print("\t" + animes.name)
        print()

    Profesor(nombre="Andres", apellido="Diaz", titulo="Tecnico Electronico")
    Profesor(nombre="Andres", apellido="Di_Donato", titulo="Ing Electronico")
    Profesor(nombre="Jake", apellido="Harper", titulo="Ing Electronico")

    Alumno(nombre="Lautaro", apellido="Velazquez", carrera="Electronica", legajo="xxx.xxx.x")
    Alumno(nombre="Alan", apellido="Harper", carrera="Electronica", legajo="xxx.xxx.a")
    Alumno(nombre="Walden", apellido="Smith", carrera="Sistemas", legajo="yyy.xxx.x")

    print("*****************************************+")
    for alumno in list(Alumno.select()):
        print("{}, {} {} legajo={}".format(alumno.apellido, alumno.nombre, alumno.carrera, alumno.legajo))
    print("*****************************************+")
    for profe in list(Profesor.select()):
        print("{}, {} titulo={}".format(profe.apellido, profe.nombre, profe.titulo))
    print("*****************************************+")

    for persona in list(Persona.select(Persona.q.childName == 'Alumno')):
        print(persona)

    print("*****************************************+")

    for persona in list(Persona.select(Persona.q.childName == 'Profesor')):
        print(persona)

    print("*****************************************+")

    for persona in Persona.select(Persona.q.apellido.startswith('H')):
        print(persona)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
