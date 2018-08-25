from flask import render_template, request, jsonify
from flask_security import current_user
from app.game.models.location import Location
from app.game.views.form_new_character import NewCharacter
from app.game.models.character import Character
from app import app


@app.route('/characters/new', methods=["GET", "POST"])
def new_character():
    if request.method == 'GET':
        form = NewCharacter()
        template = render_template('characters/new_character.html', form=form)
        return jsonify({'modal': '#bodyModal', '#bodyModal': template})
    if request.method == "POST":
        if len(current_user.characters) == 3:
            template = render_template('alert.html',
                                       sev='danger',
                                       title='ERROR!',
                                       message='Too many characters!')
            return jsonify({"alert": template})
        form = NewCharacter(request.form)
        if form.validate_on_submit():
            loc = list(Location.objects.aggregate({"$sample": {'size': 1}}))[0]['_id']
            loc = Location.objects.get(id=loc)
            chr = Character(name=form.name.data, location=loc)
            chr.save()
            if len(current_user.characters) < 3:
                current_user.characters.append(chr)
                current_user.save()
                template = render_template('account/loggedin.html')
                return jsonify({'#navright': template})
            template = render_template('alert.html',
                                       sev='danger',
                                       title='ERROR!',
                                       message='Character Creation Failed!')
            ltemplate = render_template('account/loggedin.html')
            return jsonify({"alert": template, '#navright': ltemplate})


@app.route('/characters/delete/<charname>')
def delete_character(charname):
    char = Character.objects.get(name=charname)
    if char.name == charname:
        current_user.characters.remove(char)
        current_user.save()
        char.delete()
        template = render_template('alert.html',
                                   sev='success',
                                   title='SUCCESS!',
                                   message='Character BALETED!')
        ltemplate = render_template('account/loggedin.html')
        return jsonify({"alert": template, '#navright': ltemplate})
