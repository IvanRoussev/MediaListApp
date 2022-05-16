from flask import Flask, render_template, request, redirect
from models.media import Media
from models.mediamanager import MediaManager
from models.mediatype import MediaType
import json

app = Flask(__name__)

PRESET_TYPE_DATA = [
    ['music', 'artist', 'album', 'genre'],
    ['book', 'author', 'publisher', 'genre'],
    ['game', 'main_platform', 'publisher' ,'genre']
]

@app.route("/", methods=['GET'])
def homepage():
    mediamnger = MediaManager()
    
    media_entries = mediamnger.media
    return render_template('index.html', data=media_entries, types=mediamnger.types, manager=mediamnger), 200

@app.route("/about", methods=["GET"])
def get_about():
    return render_template('about.html'), 200
    
@app.route("/updated", methods=['POST'])
def homepage_updated():
    mediamnger = MediaManager()
    type = request.form['type']
    name = request.form['name']
    f1 = request.form['field_1']
    f2 = request.form['field_2']
    f3 = request.form['field_3']
    media = mediamnger.view_media(name, type)
    if media == None:
        mediamnger.add_media(name, type, f1, f2, f3)
        mediamnger.save()
    else:
        for attribute in ('name', 'field_1', 'field_2', 'field_3'):
            setattr(media, attribute, request.form[attribute])
        mediamnger.save()

    media_entries = mediamnger.media
    return render_template('index.html', data=media_entries, types=mediamnger.types, manager=mediamnger), 200

@app.route("/editentry/<string:media_type>/<string:name>", methods=['PUT'])
def edit_entry(media_type, name):
    mediamnger = MediaManager()
    entry_to_edit = mediamnger.view_media(name, media_type)
    
    entry_to_edit.name = request.form['name']
    entry_to_edit.field_1 = request.form['field_1']
    entry_to_edit.field_2 =  request.form['field_2']
    entry_to_edit.field_3 = request.form['field_3']
    mediamnger.save()
    return "", 204

@app.route('/addentry', methods=['GET', 'POST'])
def form_display():
    mediamnger = MediaManager()
    select_media = request.form['medias']
    media_type = mediamnger.search_for_type(select_media)
    return render_template('create.html', type=media_type), 200

@app.route("/editentry/<string:media_type>/<string:name>", methods=['GET'])
def edit_form_display(media_type, name):
    mediamnger = MediaManager()
    entry = mediamnger.view_media(name, media_type)
    return render_template('edit.html', type=media_type, data=entry), 200

    
@app.route("/deleteentry/<string:media_type>/<string:name>", methods=['DELETE'])
def delete_entry(media_type, name):
    mediamnger = MediaManager()
    mediamnger.delete_media(name, media_type)
    mediamnger.save()
    return "", 201

@app.route("/<string:media_type>/<string:name>", methods=["GET"])
def get_entry(media_type, name):
    mediamnger = MediaManager()
    entry = mediamnger.view_media(name, media_type)
    if entry is None:
        return 'Entry not found', 404
    return render_template('entry.html', name=name, data=entry.to_dict()), 200






if __name__ == "__main__":
    app.run(debug=True)