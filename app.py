import json
import os
import mimetypes

from flask import Flask
from flask import jsonify


app = Flask(__name__)

with open('data/creatures.json') as f:
    creatures = json.loads(f.read())

creatures_by_idx = {}
for idx in range(len(creatures)):
    creatures_by_idx[idx] = creatures[idx]

def trait_by_type(creature, trait_type):
    for attr in creature['attributes']:
        if attr['trait_type'] == trait_type:
            return attr['value']
    return ''


@app.route('/api/creature/<token_id>')
def creature(token_id):
    token_id = int(token_id)

    creature = creatures_by_idx[token_id]
    if not creature:
        return None

    return jsonify(creature)


@app.route('/api/box/<token_id>')
def box(token_id):
    token_id = int(token_id)
    image_url = _compose_image(['images/box/lootbox.png'], token_id, "box")

    attributes = []
    _add_attribute(attributes, 'number_inside', [3], token_id)

    return jsonify({
        'name': "Creature Loot Box",
        'description': "This lootbox contains some OpenSea Creatures! It can also be traded!",
        'image': image_url,
        'external_url': 'https://openseacreatures.io/%s' % token_id,
        'attributes': attributes
    })


@app.route('/api/factory/<token_id>')
def factory(token_id):
    token_id = int(token_id)
    if token_id == 0:
        name = "One OpenSea creature"
        description = "When you purchase this option, you will receive a single OpenSea creature of a random variety. " \
                      "Enjoy and take good care of your aquatic being!"
        image_url = _compose_image(['images/factory/egg.png'], token_id, "factory")
        num_inside = 1
    elif token_id == 1:
        name = "Four OpenSea creatures"
        description = "When you purchase this option, you will receive four OpenSea creatures of random variety. " \
                      "Enjoy and take good care of your aquatic beings!"
        image_url = _compose_image(['images/factory/four-eggs.png'], token_id, "factory")
        num_inside = 4
    elif token_id == 2:
        name = "One OpenSea creature lootbox"
        description = "When you purchase this option, you will receive one lootbox, which can be opened to reveal three " \
                      "OpenSea creatures of random variety. Enjoy and take good care of these cute aquatic beings!"
        image_url = _compose_image(['images/box/lootbox.png'], token_id, "factory")
        num_inside = 3

    attributes = []
    _add_attribute(attributes, 'number_inside', [num_inside], token_id)

    return jsonify({
        'name': name,
        'description': description,
        'image': image_url,
        'external_url': 'https://openseacreatures.io/%s' % token_id,
        'attributes': attributes
    })


def _add_attribute(existing, attribute_name, options, token_id, display_type=None):
    trait = {
        'trait_type': attribute_name,
            'value': options[token_id % len(options
        )]
    }
    if display_type:
        trait['display_type'] = display_type
    existing.append(trait)


if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)
