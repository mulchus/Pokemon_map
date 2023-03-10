import folium
import os
import requests


from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.utils import timezone
from .models import Pokemon, PokemonEntity


MOSCOW_CENTER = [55.751244, 37.618423]
DEFAULT_IMAGE_URL = (
    'https://vignette.wikia.nocookie.net/pokemon/images/6/6e/%21.png/revision'
    '/latest/fixed-aspect-ratio-down/width/240/height/240?cb=20130525215832'
    '&fill=transparent'
)


def add_pokemon(folium_map, lat, lon, image_url):
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
    if not os.path.isfile(request.build_absolute_uri('/media/default_image.png')):
        default_image = requests.get(DEFAULT_IMAGE_URL)
        default_image.raise_for_status()
        with open('media/default_image.png', 'wb') as file:
            file.write(default_image.content)

    pokemons = Pokemon.objects.all()
    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)
    now = timezone.now()
    pokemon_entities = PokemonEntity.objects.filter(appeared_at__lte=now, disappeared_at__gte=now)
    for pokemon_entity in pokemon_entities:
        add_pokemon(
            folium_map,
            pokemon_entity.lat,
            pokemon_entity.lon,
            request.build_absolute_uri(pokemon_entity.pokemon.photo.url)
        )

    pokemons_on_page = []
    for pokemon in pokemons:
        pokemons_on_page.append({
            'pokemon_id': pokemon.id,
            'img_url': request.build_absolute_uri(pokemon.photo.url),
            'title_ru': pokemon.title,
        })
    return render(request, 'mainpage.html', context={
        'map': folium_map._repr_html_(),
        'pokemons': pokemons_on_page,
    })


def show_pokemon(request, pokemon_id):
    pokemon = get_object_or_404(Pokemon, id=pokemon_id)
    now = timezone.now()
    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)
    pokemon_entities = pokemon.entities.filter(appeared_at__lte=now, disappeared_at__gte=now)

    pokemons_description = {
        'pokemon_id': pokemon.id,
        'title_ru': pokemon.title,
        'title_en': pokemon.title_en,
        'title_jp': pokemon.title_jp,
        'description': pokemon.description,
        'img_url': request.build_absolute_uri(pokemon.photo.url)
    }

    if not pokemon_entities.count():
        pokemons_description['title_ru'] = f"{pokemons_description['title_ru']} (такой покемон не найден)"

    if pokemon.next_evolution.first():
        next_evolution = pokemon.next_evolution.first()
        pokemons_description.update({
            'next_evolution': {
                'title_ru': next_evolution.title,
                'pokemon_id': next_evolution.id,
                'img_url': request.build_absolute_uri(next_evolution.photo.url)
            },
        })

    if pokemon.previous_evolution:
        pokemons_description.update({
            'previous_evolution': {
                'title_ru': pokemon.previous_evolution.title,
                'pokemon_id': pokemon.previous_evolution.id,
                'img_url': request.build_absolute_uri(pokemon.previous_evolution.photo.url)
            },
        })

    for pokemon_entity in pokemon_entities:
        add_pokemon(
            folium_map,
            pokemon_entity.lat,
            pokemon_entity.lon,
            request.build_absolute_uri(pokemon.photo.url),
        )
        pokemons_description.update({
                'entities': {
                    'level': pokemon_entity.level,
                    'lat': pokemon_entity.lat,
                    'lon': pokemon_entity.lon
                },
        })

    return render(request, 'pokemon.html', context={
        'map': folium_map._repr_html_(),
        'pokemon': pokemons_description
    })
