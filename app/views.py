from app import app, forms, db
from flask import render_template, g, redirect, url_for
from app.models import Colors


@app.route('/', methods=['GET', 'POST'])
@app.route('/colorpickers', methods=['GET', 'POST'])
def color_pickers():
    form = forms.ColorPickers()
    if form.validate_on_submit():
        if Colors.query.filter_by(text_color=form.text_color.data, background_color=form.background_color.data).first() is None:
            db.session.add(Colors(text_color=form.text_color.data, background_color=form.background_color.data))
            db.session.commit()
            return "Значения сохренены"
        else:
            return "Значения уже сохранены"
    return render_template('colorpickers.html', form=form)
