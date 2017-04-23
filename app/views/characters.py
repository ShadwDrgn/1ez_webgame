from flask import render_template, request, jsonify
from flask_security import current_user
from app.game.location import Location
from app.views.forms.new_character import NewCharacter
from app.game.character import Character
from app import app


@app.route('/characters/new', methods=["GET", "POST"])
def new_character():
    if request.method == 'GET':
        form = NewCharacter()
        template = render_template('characters/new_character.html', form=form)
        return jsonify({'modal': '#bodyModal', '#bodyModal': template})
    if request.method == "POST":
        form = NewCharacter(request.form)
        if form.validate_on_submit():
            try:
                loc = Location.objects.get(x=0, y=0)
            except Location.DoesNotExist:
                loc = Location(x=0, y=0).save()
            chr = Character(name=form.name.data, location=loc)
            chr.save()
            if len(current_user.characters) < 3:
                print('>3')
                current_user.characters.append(chr)
                current_user.save()
                template = render_template('account/loggedin.html')
                return jsonify({'#navright': template})
            template = render_template('alert.html',
                                       sev='danger',
                                       title='ERROR!',
                                       message='Character Creation Failed!')
            return jsonify({"alert": template})
