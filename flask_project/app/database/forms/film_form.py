from wtforms import StringField, IntegerField, validators, DateField

from . import FlaskForm


class FilmForm(FlaskForm):
    movie_title = StringField("Movie title", validators=[validators.InputRequired(), validators.Length(min=2, max=20)])
    release_date = DateField('Release date', format='%Y/%m/%d', validators=[validators.Optional()])
    rating = IntegerField("Rating", validators=[validators.InputRequired(), validators.NumberRange(min=0, max=10)])


class SearchForm(FlaskForm):
    search = StringField('Search course', validators=[validators.DataRequired(), validators.Length(max=60)])

class FilmEditForm(FlaskForm):
    release_date = DateField('Release date', format='%Y/%m/%d', validators=[validators.Optional()])
    rating = IntegerField("Rating", validators=[validators.InputRequired(), validators.NumberRange(min=0, max=10)])
    id_director = IntegerField("Rating", validators=[validators.InputRequired(), validators.NumberRange(min=1)])