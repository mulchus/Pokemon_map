import folium

from django.shortcuts import render
from .models import Pokemon, PokemonEntity
from datetime import datetime


MOSCOW_CENTER = [55.751244, 37.618423]
DEFAULT_IMAGE_URL = (
    'https://vignette.wikia.nocookie.net/pokemon/images/6/6e/%21.png/revision'
    '/latest/fixed-aspect-ratio-down/width/240/height/240?cb=20130525215832'
    '&fill=transparent'
)


def add_pokemon(folium_map, lat, lon, image_url=DEFAULT_IMAGE_URL):
    icon = folium.features.CustomIcon(
        image_url,
        icon_size=(50, 50),
    )
    folium.Marker(
        [lat, lon],
        # Warning! `tooltip` attribute is disabled intentionally
        # to fix strange folium cyrillic encoding bug
        icon=icon,
    ).add_to(folium_map)


def show_all_pokemons(request):
    pokemons = Pokemon.objects.all()
    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)
    now = datetime.now().timestamp()
    pokemon_entities = PokemonEntity.objects.all()
    for pokemon_entity in pokemon_entities:
        if pokemon_entity.appeared_at.timestamp() <= now <= pokemon_entity.disappeared_at.timestamp():
            add_pokemon(
                folium_map,
                pokemon_entity.lat,
                pokemon_entity.lon,
                f'{request.build_absolute_uri("/media/")}{pokemon_entity.pokemon.photo}'
            )

    pokemons_on_page = []
    for pokemon in pokemons:
        pokemons_on_page.append({
            'pokemon_id': pokemon.id,
            'img_url': f'{request.build_absolute_uri("/media/")}{pokemon.photo}',
            'title_ru': pokemon.title,
        })
    return render(request, 'mainpage.html', context={
        'map': folium_map._repr_html_(),
        'pokemons': pokemons_on_page,
    })


def show_pokemon(request, pokemon_id):
    pokemon = Pokemon.objects.get(id=pokemon_id)
    now = datetime.now().timestamp()
    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)
    pokemon_entities = pokemon.pokemon_entity.all()
    for pokemon_entity in pokemon_entities:
        if pokemon_entity.appeared_at.timestamp() <= now <= pokemon_entity.disappeared_at.timestamp():
            photo = f'{request.build_absolute_uri("/media/")}{pokemon.photo}'
            add_pokemon(
                folium_map,
                pokemon_entity.lat,
                pokemon_entity.lon,
                photo,
            )

            pokemons_description = {
                'pokemon_id': pokemon.id,
                'title_ru': pokemon.title,
                'title_en': pokemon.title_en,
                'title_jp': pokemon.title_jp,
                'description': pokemon.description,
                'img_url': f'{request.build_absolute_uri("/media/")}{pokemon.photo}',
                'entities': {
                    'level': pokemon_entity.level,
                    'lat': pokemon_entity.lat,
                    'lon': pokemon_entity.lon
                },
            }
            if pokemon.previous_pokemon.first():
                next_pokemon = pokemon.previous_pokemon.first()
                pokemons_description.update({
                    'next_evolution': {
                        'title_ru': next_pokemon.title,
                        'pokemon_id': next_pokemon.id,
                        'img_url': f'{request.build_absolute_uri("/media/")}{next_pokemon.photo}'
                    },
                })
            if pokemon.previous_evolution:
                pokemons_description.update({
                    'previous_evolution': {
                        'title_ru': pokemon.previous_evolution.title,
                        'pokemon_id': pokemon.previous_evolution.id,
                        'img_url': f'{request.build_absolute_uri("/media/")}{pokemon.previous_evolution.photo}'
                    },
                })

    return render(request, 'pokemon.html', context={
        'map': folium_map._repr_html_(),
        'pokemon': pokemons_description
    })
