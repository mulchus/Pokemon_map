import folium

from django.shortcuts import render
from django.utils import timezone
from .models import Pokemon, PokemonEntity


MOSCOW_CENTER = [55.751244, 37.618423]


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
    pokemons = Pokemon.objects.all()
    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)
    now = timezone.now()
    pokemon_entities = PokemonEntity.objects.filter(appeared_at__lte=now, disappeared_at__gte=now)
    for pokemon_entity in pokemon_entities:
        add_pokemon(
            folium_map,
            pokemon_entity.lat,
            pokemon_entity.lon,
            request.build_absolute_uri(f'/media/{pokemon_entity.pokemon.photo}')
        )

    pokemons_on_page = []
    for pokemon in pokemons:
        pokemons_on_page.append({
            'pokemon_id': pokemon.id,
            'img_url': request.build_absolute_uri(f'/media/{pokemon.photo}'),
            'title_ru': pokemon.title,
        })
    return render(request, 'mainpage.html', context={
        'map': folium_map._repr_html_(),
        'pokemons': pokemons_on_page,
    })


def show_pokemon(request, pokemon_id):
    pokemon = Pokemon.objects.get(id=pokemon_id)
    now = timezone.now()
    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)
    pokemon_entities = pokemon.pokemon_entity.filter(appeared_at__lte=now, disappeared_at__gte=now)

    pokemons_description = {
        'pokemon_id': pokemon.id,
        'title_ru': pokemon.title,
        'title_en': pokemon.title_en,
        'title_jp': pokemon.title_jp,
        'description': pokemon.description,
        'img_url': request.build_absolute_uri(f'/media/{pokemon.photo}')
    }

    if not pokemon_entities.count():
        pokemons_description['title_ru'] += ' (такой покемон не найден)'

    if pokemon.previous_pokemon.first():
        next_pokemon = pokemon.previous_pokemon.first()
        pokemons_description.update({
            'next_evolution': {
                'title_ru': next_pokemon.title,
                'pokemon_id': next_pokemon.id,
                'img_url': request.build_absolute_uri(f'/media/{next_pokemon.photo}')
            },
        })

    if pokemon.previous_evolution:
        pokemons_description.update({
            'previous_evolution': {
                'title_ru': pokemon.previous_evolution.title,
                'pokemon_id': pokemon.previous_evolution.id,
                'img_url': request.build_absolute_uri(f'/media/{pokemon.previous_evolution.photo}')
            },
        })

    for pokemon_entity in pokemon_entities:
        photo = request.build_absolute_uri(f'/media/{pokemon.photo}')
        add_pokemon(
            folium_map,
            pokemon_entity.lat,
            pokemon_entity.lon,
            photo,
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
