#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

import json
import dateutil.parser
import babel
from flask import Flask, render_template, request, Response, flash, redirect, url_for, abort
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import logging
from logging import Formatter, FileHandler
from flask_wtf import Form
from forms import *
from datetime import date
#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
moment = Moment(app)
app.config.from_object('config')
db = SQLAlchemy(app)
migrate = Migrate(app, db)
# TODO: connect to a local postgresql database

#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#
artist_shows = db.Table('artist_shows',
    db.Column('show_id', db.Integer, db.ForeignKey('Show.id'), primary_key=True),
    db.Column('artist_id', db.Integer, db.ForeignKey('Artist.id'), primary_key=True)

)

venue_shows = db.Table('venue_shows',
    db.Column('show_id', db.Integer, db.ForeignKey('Show.id'), primary_key=True),
    db.Column('venue_id', db.Integer, db.ForeignKey('Venue.id'), primary_key=True)
)


class Venue(db.Model):
    __tablename__ = 'Venue'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    city = db.Column(db.String(120), nullable=False)
    state = db.Column(db.String(120), nullable=False)
    address = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(120), nullable=False)
    genres = db.Column(db.String)
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    website_link = db.Column(db.String(120))
    seeking_performers = db.Column(db.CHAR, server_default="y")


class Artist(db.Model):
    __tablename__ = 'Artist'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), nullable=False)
    city = db.Column(db.String(120), nullable=False)
    state = db.Column(db.String(120))
    phone = db.Column(db.String(120), nullable=False)
    genres = db.Column(db.String)
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    website_link = db.Column(db.String(120))
    seeking_performances = db.Column(db.CHAR, server_default="y")



# TODO Implement Show and Artist models, and complete all model relationships and properties, as a database migration.
class Show(db.Model):
    __tablename__ = 'Show'

    id = db.Column(db.Integer, primary_key=True)
    artist_id = db.Column(db.Integer, db.ForeignKey('Artist.id'), nullable=False)
    venue_id = db.Column(db.Integer, db.ForeignKey('Venue.id'), nullable=False)
    start_time = db.Column(db.DateTime, nullable=False)
    artists = db.relationship('Artist', secondary=artist_shows, backref=db.backref('shows', lazy=True))
    venues = db.relationship('Venue', secondary=venue_shows, backref=db.backref('venues', lazy=True))




#----------------------------------------------------------------------------#
# Filters.
#----------------------------------------------------------------------------#

def format_datetime(value, format='medium'):
  date = dateutil.parser.parse(value)
  if format == 'full':
      format="EEEE MMMM, d, y 'at' h:mma"
  elif format == 'medium':
      format="EE MM, dd, y h:mma"
  return babel.dates.format_datetime(date, format)

app.jinja_env.filters['datetime'] = format_datetime

#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#

@app.route('/')
def index():
  return render_template('pages/home.html')


#  Venues
#  ----------------------------------------------------------------

@app.route('/venues')
def venues():
  cities = db.session.query(Venue.city).distinct()
  dataset = []
  for city in cities:
      venues = Venue.query.filter_by(city = city).all()
      for venue in venues:
          state = venue.state
          city_name = venue.city
          data = {
            "city": city_name,
            "state": state,
            "venues": venues
          }
      dataset.append(data)



  return render_template('pages/venues.html', areas=dataset);

@app.route('/venues/search', methods=['POST'])
def search_venues():
  search_term = request.form.get('search_term', '')
  search_results = Venue.query.filter(Venue.name.ilike('%' + search_term + '%')).all()
  number_results = len(search_results)

  return render_template('pages/search_venues.html', results=search_results, number_results=number_results, search_term=search_term)

@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
  venue = Venue.query.get(venue_id)
  genres = venue.genres
  genres = genres.split(",")
  genres = [genre.replace("}","") for genre in genres ]
  genres = [genre.replace("{","") for genre in genres ]
  now = datetime.utcnow()
  upcoming_shows = Show.query.filter(Show.venue_id == venue_id, Show.start_time > now).all()
  upcoming_shows_list = []
  for show_listing in upcoming_shows:
      artist = Artist.query.get(show_listing.artist_id)
      show = {
        "artist_image_link": artist.image_link,
        "artist_id": artist.id,
        "artist_name": artist.name,
        "start_time": str(show_listing.start_time)
      }
      upcoming_shows_list.append(show)
  past_shows = upcoming_shows = Show.query.filter(Show.venue_id == venue_id, Show.start_time < now).all()
  past_shows_list = []
  for show_listing in past_shows:
      artist = Artist.query.get(show_listing.artist_id)
      show = {
        "artist_image_link": artist.image_link,
        "artist_id": artist.id,
        "artist_name": artist.name,
        "start_time": str(show_listing.start_time)
      }
      past_shows_list.append(show)
  data = {
    "venue": venue,
    "upcoming_shows": upcoming_shows_list,
    "upcoming_shows_count": len(upcoming_shows_list),
    "genres": genres,
    "past_shows": past_shows_list,
    "past_shows_count": len(past_shows_list)
  }


  return render_template('pages/show_venue.html', data=data)

#  Create Venue
#  ----------------------------------------------------------------

@app.route('/venues/create', methods=['GET'])
def create_venue_form():
  form = VenueForm()
  return render_template('forms/new_venue.html', form=form)

@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
  error = False
  try:
      name = request.form['name']
      city = request.form['city']
      state = request.form['state']
      address = request.form['address']
      phone = request.form['phone']
      genres = request.form.getlist('genres')
      facebook_link = request.form['facebook_link']
      website_link = request.form['website_link']
      image_link = request.form['image_link']
      seeking_performers = request.form['seeking_performers']
      venue = Venue(name=name, city=city, state=state, address=address, phone=phone,
      genres=genres, facebook_link=facebook_link, seeking_performers=seeking_performers,
      image_link=image_link, website_link=website_link)
      db.session.add(venue)
      db.session.commit()
  except:
      db.session.rollback()
      error = True
  finally:
      db.session.close()
  if error:
      flash('An error occured. Venue ' + request.form['name'] + ' could not be listed.')
  else:
      flash('Venue ' + request.form['name'] + ' was successfully listed!')

  return render_template('pages/home.html')

@app.route('/venues/<venue_id>', methods=['DELETE'])
def delete_venue(venue_id):
  venue = Venue.query.filter_by(id=venue_id).first()
  try:
      db.session.delete(venue)
      db.session.commit()
  except:
      db.session.rollback()
      flash('An error occured. Venue ' + venue.name + ' could not be deleted.')
  finally:
      db.session.close()
      flash('Venue ' + venue.name + ' was successfully deleted!')
  return render_template('pages/home.html')

#  Artists
#  ----------------------------------------------------------------
@app.route('/artists')
def artists():
  artists = Artist.query.all()
  return render_template('pages/artists.html', artists=artists)


@app.route('/artists/search', methods=['POST'])
def search_artists():
  search_term = request.form.get('search_term', '')
  search_results = Artist.query.filter(Artist.name.ilike('%' + search_term + '%')).all()
  number_results = len(search_results)

  return render_template('pages/search_artists.html', results=search_results, number_results=number_results, search_term=search_term)


@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
  artist = Artist.query.get(artist_id)
  genres = artist.genres
  genres = genres.split(",")
  genres = [genre.replace("}","") for genre in genres ]
  genres = [genre.replace("{","") for genre in genres ]
  now = datetime.utcnow()
  upcoming_shows = Show.query.filter(Show.artist_id == artist_id, Show.start_time > now).all()
  upcoming_shows_list = []
  for show_listing in upcoming_shows:
      venue = Venue.query.get(show_listing.venue_id)
      show = {
        "venue_image_link": venue.image_link,
        "venue_id": venue.id,
        "venue_name": venue.name,
        "start_time": str(show_listing.start_time)
      }
      upcoming_shows_list.append(show)

  past_shows = upcoming_shows = Show.query.filter(Show.artist_id == artist_id, Show.start_time < now).all()
  past_shows_list = []
  for show_listing in past_shows:
      venue = Venue.query.get(show_listing.venue_id)
      show = {
        "venue_image_link": venue.image_link,
        "venue_id": venue.id,
        "venue_name": venue.name,
        "start_time": str(show_listing.start_time)
      }
      past_shows_list.append(show)

  data = {
    "artist": artist,
    "genres": genres,
    "upcoming_shows": upcoming_shows_list,
    "upcoming_shows_count": len(upcoming_shows_list),
    "past_shows": past_shows_list,
    "past_shows_count": len(past_shows_list)
  }

  return render_template('pages/show_artist.html', data=data)

#  Update
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
  artist = Artist.query.get(artist_id)
  form = ArtistForm(obj=artist)
  return render_template('forms/edit_artist.html', form=form, artist=artist)

@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
  artist = Artist.query.filter_by(id=artist_id).first()
  try:
      artist.name = request.form['name']
      artist.city = request.form['city']
      artist.state = request.form['state']
      artist.phone = request.form['phone']
      artist.genres = request.form.getlist('genres')
      artist.facebook_link = request.form['facebook_link']
      artist.website_link = request.form['website_link']
      artist.image_link = request.form['image_link']
      artist.seeking_performances = request.form['seeking_performances']
      db.session.commit()
      flash("Artist: " + artist.name + " updated succefully!")
  except:
      db.session.rollback()
      flash("Error, Artist: " + artist.name + " could not be updated.")
  finally:
      db.session.close()

  return redirect(url_for('show_artist', artist_id=artist_id))


@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
  venue = Venue.query.get(venue_id)
  form = VenueForm(obj=venue)

  return render_template('forms/edit_venue.html', form=form, venue=venue)

@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
  venue = Venue.query.filter_by(id=venue_id).first()
  venue.name = request.form['name']
  venue.city = request.form['city']
  venue.state = request.form['state']
  venue.address = request.form['address']
  venue.phone = request.form['phone']
  venue.genres = request.form.getlist('genres')
  venue.facebook_link = request.form['facebook_link']
  venue.website_link = request.form['website_link']
  venue.image_link = request.form['image_link']
  venue.seeking_performers = request.form.get("seeking_performers")
  try:
      db.session.commit()
      flash("Venue: " + venue.name + " updated succefully!")
  except:
      db.session.rollback()
      flash("Error, Venue: " + venue.name + " could not be updated.")
  finally:
      db.session.close()
  return redirect(url_for('show_venue', venue_id=venue_id))

#  Create Artist
#  ----------------------------------------------------------------

@app.route('/artists/create', methods=['GET'])
def create_artist_form():
  form = ArtistForm()
  return render_template('forms/new_artist.html', form=form)

@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
    error = False
    try:
        name = request.form['name']
        city = request.form['city']
        state = request.form['state']
        phone = request.form['phone']
        genres = request.form.getlist('genres')
        facebook_link = request.form['facebook_link']
        website_link = request.form['website_link']
        image_link = request.form['image_link']
        artist = Artist(name=name, city=city, state=state, phone=phone,
                        genres=genres, facebook_link=facebook_link, website_link=website_link, image_link=image_link)
        db.session.add(artist)
        db.session.commit()
    except:
        db.session.rollback()
        error = True
    finally:
        db.session.close()
    if error:
        flash('An error occured. Artist ' + request.form['name'] + ' could not be listed.')
    else:
        flash('Artist ' + request.form['name'] + ' was successfully listed!')

    return render_template('pages/home.html')


#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():
  shows = Show.query.all()
  dataset = []
  for show in shows:
      venue = Venue.query.get(show.venue_id)
      artist = Artist.query.get(show.artist_id)
      data = {
        "venue_id": show.venue_id,
        "venue_name": venue.name,
        "artist_id": show.artist_id,
        "artist_name": artist.name,
        "artist_image_link": artist.image_link,
        "start_time": str(show.start_time)
      }
      dataset.append(data)
  return render_template('pages/shows.html', shows=dataset)

@app.route('/shows/create')
def create_shows():
  form = ShowForm()
  return render_template('forms/new_show.html', form=form)

@app.route('/shows/create', methods=['POST'])
def create_show_submission():
  error = False
  try:
      artist_id = request.form["artist_id"]
      venue_id = request.form["venue_id"]
      start_time = request.form["start_time"]
      show = Show(artist_id=artist_id, venue_id=venue_id, start_time=start_time)
      db.session.add(show)
      db.session.commit()
  except:
      error = True
      db.session.rollback()
  finally:
      db.session.close()
  if error:
      flash('An error occurred. Show could not be listed.')
  else:
      flash('Show was successfully listed!')

  return render_template('pages/home.html')


@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def server_error(error):
    return render_template('errors/500.html'), 500


if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':
    app.run()

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''
