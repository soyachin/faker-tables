from random import choice, randint
import pandas as p
import pandas as pd
from faker import Faker
import hashlib, uuid, json


faker = Faker()
Faker.seed(0)

def generar_tabla_usuarios():
    n = 10000
    usuarios = p.DataFrame({
        'tenant_id': [faker.unique.ascii_email() for _ in range(n)],
        'country': [faker.country() for _ in range(n)],
        'username': [faker.user_name() for _ in range(n)],
        'password': [hashlib.sha256(faker.password(length=randint(8,12)).encode('utf-8')).hexdigest() for _ in range(n)],
        'picture': [faker.image_url() for _ in range(n)],

    })

    return usuarios

def generar_canciones_favoritas_usuario(usuarios, canciones):
    n = 20000
    favs = p.DataFrame({
        'tenant_id': [choice(usuarios['tenant_id']) for _ in range(n)],
        'date_added': [faker.unique.date_time().strftime('%Y-%m-%d %H:%M:%S') for _ in range(n)],
        'song_id': [choice(canciones['song_uuid']) for _ in range(n)]

    })
    return favs

def generar_tabla_podcaster():
    n = 25000
    podcasters = p.DataFrame({
        'creator_id': [faker.unique.ascii_email() for _ in range(n)],
        'country': [faker.country() for _ in range(n)],
        'name': [faker.name() for _ in range(n)],
        'password': [hashlib.sha256(faker.password(length=randint(8,12)).encode('utf-8')).hexdigest() for _ in range(n)],
        'info': [faker.text(max_nb_chars=20) for _ in range(n)],
        'picture': [faker.image_url() for _ in range(n)],

    })

    return podcasters

def generar_podcast(podcasters):
    podcast_genres = [
        "Interviews",
        "True Crime",
        "Comedy",
        "News and Current Affairs",
        "Education",
        "History",
        "Technology",
        "Pop Culture",
        "Personal Development",
        "Fiction",
        "Business and Finance",
        "Sports",
        "Music",
        "Science",
        "Relationships",
        "Society",
        "Travel",
        "Health and Wellbeing",
        "Humor and Entertainment",
        "Self-help"
    ]

    n = 10000
    podcasts = p.DataFrame({
        'creator_id': [choice(podcasters['creator_id']) for _ in range(n)],
        'podcast_uuid': [str(uuid.uuid4()) for _ in range(n)],
        'genre#release_date': [choice(podcast_genres) + '#' + faker.unique.date_time().strftime('%Y-%m-%d %H:%M:%S') for _ in range(n)],
        'info': [faker.text(max_nb_chars=20) for _ in range(n)],
        'data': [
            json.dumps({
                'explicit': faker.boolean(),
                'language': faker.language_code(),
                'picture': faker.image_url(),
            })
            for _ in range(n)
        ]
    })

    return podcasts

def main():
    usuarios = generar_tabla_usuarios()
    print(f'Generados {len(usuarios)}')
    podcasters = generar_tabla_podcaster()
    print(f'Generados {len(podcasters)}')

    canciones = pd.read_csv('songs.csv')
    podcasts = generar_podcast(podcasters)
    print(f'Generados {len(podcasts)}')

    canciones_favoritas = generar_canciones_favoritas_usuario(usuarios, canciones)
    print(f'Generados {len(canciones_favoritas)}')

    usuarios.to_csv('usuarios.csv', index=False)
    podcasters.to_csv('podcasters.csv', index=False)
    podcasts.to_csv('podcasts.csv', index=False)
    canciones_favoritas.to_csv('canciones_favoritas.csv', index=False)


if __name__ == '__main__':
    main()