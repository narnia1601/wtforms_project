from flask import Flask, render_template, redirect
from flask.helpers import url_for
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.fields.choices import SelectField
from wtforms.fields.datetime import TimeField
from wtforms.fields.simple import URLField
from wtforms.validators import URL, DataRequired
import csv

from wtforms.widgets.core import Select

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap(app)


class CafeForm(FlaskForm):
    cafe = StringField('Cafe name', validators=[DataRequired()])
    location = URLField('Location', validators=[DataRequired(), URL()])
    open = TimeField('Open', validators=[DataRequired()])
    close = TimeField('Close', validators=[DataRequired()])
    coffee = SelectField(choices=[('☕️', '☕️'),('☕️☕️','☕️☕️'),('☕️☕️☕️','☕️☕️☕️'),('☕️☕️☕️☕️','☕️☕️☕️☕️'),('☕️☕️☕️☕️☕️','☕️☕️☕️☕️☕️')])
    wifi = SelectField(choices=[('✘','✘'),('💪','💪'),('💪💪','💪💪'),('💪💪💪','💪💪💪'),('💪💪💪💪','💪💪💪💪'),('💪💪💪💪💪','💪💪💪💪💪')])
    power = SelectField(choices=[('✘','✘'),('🔌','🔌'),('🔌🔌','🔌🔌'),('🔌🔌🔌','🔌🔌🔌'),('🔌🔌🔌🔌','🔌🔌🔌🔌'),('🔌🔌🔌🔌🔌','🔌🔌🔌🔌🔌')])
    submit = SubmitField('Submit')

# Exercise:
# add: Location URL, open time, closing time, coffee rating, wifi rating, power outlet rating fields
# make coffee/wifi/power a select element with choice of 0 to 5.
#e.g. You could use emojis ☕️/💪/✘/🔌
# make all fields required except submit
# use a validator to check that the URL field has a URL entered.
# ---------------------------------------------------------------------------


# all Flask routes below
@app.route("/")
def home():
    return render_template("index.html")


@app.route('/add', methods=['GET','POST'])
def add_cafe():
    form = CafeForm()
    if form.validate_on_submit():
        with open('cafe-data.csv', 'a') as myfile:
            myfile.write(f'\n{form.cafe.data},{form.location.data},{form.open.data},{form.close.data},{form.coffee.data},{form.wifi.data},{form.power.data}')
        return redirect(url_for('cafes'))
    # Exercise:
    # Make the form write a new row into cafe-data.csv
    # with   if form.validate_on_submit()
    return render_template('add.html', form=form)


@app.route('/cafes')
def cafes():
    with open('cafe-data.csv', newline='') as csv_file:
        csv_data = csv.reader(csv_file, delimiter=',')
        list_of_rows = []
        for row in csv_data:
            list_of_rows.append(row)
    return render_template('cafes.html', cafes=list_of_rows)


if __name__ == '__main__':
    app.run(debug=True)
