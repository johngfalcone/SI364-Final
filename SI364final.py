import os
import flask
from flask import Flask, render_template, session, redirect, url_for, flash, request
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, FileField, PasswordField, BooleanField, SelectMultipleField, ValidationError, HiddenField
from wtforms.validators import Required # Here, too
from flask_sqlalchemy import SQLAlchemy
from flask_script import Manager, Shell
import requests
import json
from wtforms.validators import Required, Length, Email, Regexp, EqualTo
from flask_login import LoginManager, login_required, logout_user, login_user, UserMixin, current_user
from werkzeug.security import generate_password_hash, check_password_hash
import random
from flask_migrate import Migrate, MigrateCommand
from threading import Thread
from werkzeug import secure_filename
from geopy.geocoders import Nominatim
import json
import requests

#basic setup
app = Flask(__name__)
app.debug = True
app.use_reloader = True
app.config['SECRET_KEY'] = 'hard to guess string from si364'


#db setup
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://localhost/falconeFINAL"
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

#db stuff
manager = Manager(app)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
manager.add_command('db', MigrateCommand)

login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'login'
login_manager.init_app(app) # set up login manager



###################################
########## MODELS #################
###################################



class User(UserMixin, db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), index=True)

    password_hash = db.Column(db.String(128))
    location = db.Column(db.String(128))
    #TODO 364: In order to complete a relationship with a table that is detailed below (a one-to-many relationship for users and gif collections), you'll need to add a field to this User model. (Check out the TODOs for models below for more!)
    # Remember, the best way to do so is to add the field, save your code, and then create and run a migration!
    tweets = db.relationship("Tweet", backref = "Tweet", primaryjoin = "Tweet.user_id == User.id")
    following = db.relationship("Following", backref = "User", primaryjoin = "Following.user_1 == User.id")

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

@login_manager.user_loader
def load_user(username):
    return User.query.get(username) # returns User object or None



###################################
########## OTHER MODELS ###########
###################################



class Tweet(db.Model):
    __tablename__ = 'tweets'
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(280))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    user_ref = db.relationship("User", foreign_keys=[user_id])

class Comment(db.Model):
    __tablename__ = 'comments'
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(280))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    tweet_id = db.Column(db.Integer, db.ForeignKey('tweets.id'))
    user_ref = db.relationship("User", foreign_keys=[user_id])
    tweet_ref = db.relationship("Tweet", foreign_keys=[tweet_id])

class Like(db.Model):
    __tablename__ = 'likes'
    id = db.Column(db.Integer, primary_key=True)
    tweet_id = db.Column(db.Integer, db.ForeignKey('tweets.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    user_ref = db.relationship("User", foreign_keys=[user_id])
    tweet_ref = db.relationship("Tweet", foreign_keys=[tweet_id])


class Following(db.Model):
    # User1 Follows User2
    __tablename__ = "following"
    user_1 = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    user_2 = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    username_1 = db.relationship("User", foreign_keys=[user_1])
    username_2 = db.relationship("User", foreign_keys=[user_2])



###################################
########## FORMS ##################
###################################


class RegistrationForm(FlaskForm):

    username = StringField('Username: ',validators=[Required(), Length(1,64),Regexp('^[A-Za-z][A-Za-z0-9_.]*$',0,'Usernames must have only letters, numbers, dots or underscores')])
    password = PasswordField('Password: ',validators=[Required(), EqualTo('password2', message="Passwords must match")])
    password2 = PasswordField("Confirm Password: ",validators=[Required()])
    location = StringField('Location (City): ', validators=[Required(), Length(1,64)])
    submit = SubmitField('Register User')
    #search = StringField("Hoping this runs")

    #Additional checking methods for the form
    def validate_username(self,field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('Username already taken. Try another one!')



class LoginForm(FlaskForm):
    username = StringField('Username: ', validators=[Required(), Length(1,64)])
    password = PasswordField('Password: ', validators=[Required()])
    remember_me = BooleanField('Keep me logged in to this account')
    submit = SubmitField('Login')



class CreateTweetForm(FlaskForm):

    def validate_length(self, field):
        tweet = str(field)
        if len(tweet) > 280:
            raise ValidationError("Post text must be under 280 characters!")

    tweet = StringField('What would you like to Post?',validators=[Required(), Length(1,280)])
    submit = SubmitField("Post")

class CreateFollowForm(FlaskForm):
    new_follow = StringField('Who would you like to Follow?',validators=[Length(1,280)])
    submit = SubmitField("Follow")

#tweet_id_in = 0

class CreateLikeForm(FlaskForm):

    def validate_length(self, field):
        tweet_id = str(field)
        if len(tweet_id) < 1:
            raise ValidationError("ID must be at least one integer!")

    tweet_id = StringField('What post would you like to "Like"? (Enter Post ID)', validators=[Required()])
    submit = SubmitField("Like")

class CreateCommentForm(FlaskForm):
    comment_tweet_id = StringField('What post would you like to comment on? (Enter Post ID)', validators=[Required()])
    comment_text = StringField('What would you like to comment?', validators=[Required()])
    submit = SubmitField("Comment")


class UpdateLocationForm(FlaskForm):
    new_location = StringField('What would you like to make your location? (City names only, please)',validators=[Required(), Length(1,280)])
    submit = SubmitField("Update")

class UpdateLikeForm(FlaskForm):
    delete_like = StringField('What post would you like to remove from your likes? (Enter Post ID)',validators=[Required(), Length(1,280)])
    submit = SubmitField("Delete")

###################################
########## FUNCTIONS ##############
###################################

def get_or_create_tweet(text):
    
    #current_tweet = db.session.query(Tweet).filter_by(text=text).first()
    current_tweet = db.session.query(Tweet, User).filter(Tweet.text == text).filter(User.id == Tweet.user_id).first()
    
    if current_tweet:
        return current_tweet


    else:
        current_tweet = Tweet(text = text, user_id=current_user.id)
        db.session.add(current_tweet)
        db.session.commit()
        return current_tweet



def get_or_create_follow(username):
    
    #Maybe add code for if user does not exist? Is this happening already?
    #current_tweet = db.session.query(Tweet).filter_by(text=text).first()
    user_to_be_followed = db.session.query(User).filter_by(username=username).first()
    current_follow = db.session.query(User, Following).filter(Following.user_1==current_user.id).filter(Following.user_2==user_to_be_followed.id).first()
    print(current_user.username)
    print(user_to_be_followed.username)
    print(current_follow)

    if current_follow:
        flash('You already follow this user! Try another one.')
        return current_follow



    else:
        current_follow = Following(user_1=current_user.id, user_2=user_to_be_followed.id)
        db.session.add(current_follow)
        db.session.commit()
        return current_follow




def get_or_create_like(tweet_id_in):
    
    #current_tweet = db.session.query(Tweet).filter_by(text=text).first()
    #current_tweet = db.session.query(Tweet, User).filter(Tweet.text == text).filter(User.id == Tweet.user_id).first()
    test = db.session.query(Like).all()
    print("test")
    print(test)
    #tweet_to_be_liked = db.session.query(User, Like)
    #liked_tweet = Like.query.filter_by(tweet_ref = tweet.id)
    #if I can get tweet to be a single tweet id, problem solved
    #print(tweet)
    #tweet_to_be_liked = db.session.query(Tweet).filter_by(id=tweet).first()
    print(tweet_id_in)
    almost = int(tweet_id_in)
    tweet_to_be_liked = almost
    liked_tweet = db.session.query(Like).filter(Like.tweet_id == tweet_to_be_liked).filter(Like.user_id == current_user.id).first()
    #liked_tweet = db.session.query(Tweet, Like).filter(Tweet.id == tweet_to_be_liked).join(Like, Like.user_id == current_user.id).first()
    print("TWEET TO BE LIKED " + str(tweet_to_be_liked))
    print("TWEETIDIN" + str(tweet_id_in))
    print("LIKED_TWEET" + str(liked_tweet))
    flash("Attempting to create like.")

    
    if liked_tweet:
        #return liked_tweet
        flash("You've already liked this!")


    else:
        liked_tweet = Like(tweet_id = almost, user_id = current_user.id)
        db.session.add(liked_tweet)
        db.session.commit()
        flash("You've added this to your likes!")


def get_or_create_comment(comment_in, tweet_id_in):

    comment = db.session.query(Comment).filter(Comment.tweet_id == tweet_id_in).filter(Comment.user_id == current_user.id).first()
    flash("Attempting to create comment.")

    almost = int(tweet_id_in)

    if comment:
        flash("You've already commented on this post!")

    else:
        comment = Comment(tweet_id = almost, user_id = current_user.id, text = comment_in)
        db.session.add(comment)
        db.session.commit()
        flash("You've added this to your comments!")

def update_location(location):
    user_to_be_updated = db.session.query(User).filter_by(id=current_user.id).first()

    new_location = location
    user_to_be_updated.location = new_location

    return new_location
    flash("You've updated your location!")

def get_weather(location):

        #location = city.data

        geolocator = Nominatim(user_agent="test")
        weather_location = geolocator.geocode(location)

        url = "https://api.darksky.net/forecast/c7f71279af92395e316a9c2760491416/" + str(weather_location.latitude) + "," + str(weather_location.longitude)
        
        response = requests.get(url)
        jData = json.loads(response.content)
        report = "The weather in " + str(location) + " today was " + jData['hourly']['summary'] + " with a high of " + str(jData['daily']['data'][0]['temperatureHigh']) + " and a low of " + str(jData['daily']['data'][0]['temperatureLow']) + "."
        
        return report

def delete_like(post_to_be_deleted):

    print(post_to_be_deleted)
    like_to_be_deleted = db.session.query(Like, User).filter(Like.user_id == current_user.id).filter(Like.tweet_id == post_to_be_deleted).first()
    print("LIKETOBEDELETED" + str(post_to_be_deleted))
    d = Like.query.filter_by(tweet_id = post_to_be_deleted)
    d.delete()

    #return like_to_be_deleted


###################################
########## ROUTES #################
###################################
## Error handling routes
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500


@app.route('/login',methods=["GET","POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user, form.remember_me.data)
            return redirect(request.args.get('next') or url_for('index'))
        flash('Invalid username or password.')
    return render_template('login.html',form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('***** You have been logged out! *****')
    return redirect(url_for('index'))

@app.route('/register',methods=["GET","POST"])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data,password=form.password.data, location=form.location.data)
        db.session.add(user)
        db.session.commit()
        flash('***** You can now log in! *****')
        return redirect(url_for('login'))
    return render_template('register.html',form=form)

@app.route('/secret')
@login_required
def secret():
    return "Only authenticated users can do this! Try to log in or contact the site admin."


@app.route('/', methods=['GET', 'POST'])
def index():
    # TODO 364: Edit this view function, which has a provided return statement, so that the GifSearchForm can be rendered.
    # If the form is submitted successfully:
    # invoke get_or_create_search_term on the form input and redirect to the function corresponding to the path /gifs_searched/<search_term> in order to see the results of the gif search. (Just a couple lines of code!)
    # HINT: invoking url_for with a named argument will send additional data. e.g. url_for('artist_info',artist='solange') would send the data 'solange' to a route /artist_info/<artist>
    if not current_user.is_authenticated:
        return flask.redirect(url_for('login'))


    #tweets_condensed = (db.session.query(Tweet, User, Following).filter(current_user.id == Following.user_1).filter(Tweet.user_id == Following.user_2).all())
    #tweets2 = db.session.query(Tweet, User).all()
    tweets = db.session.query(Tweet, Following).join(Following, current_user.id == Following.user_1).filter(Tweet.user_id == Following.user_2).all()
    #likes = tweets = db.session.query(Like).filter(Like.user_id==current_user.id).all()

    tweets_condensed = []


    form3 = CreateLikeForm()
    form6 = CreateCommentForm()

    #for x in tweets:
    #    tweets_condensed.append(x[0])

    #for y in tweets_condensed:
    #    print(y)
    #    print(y.id)
    #    tweet_id_in = y.id

    #form1 = CreateFollowForm()
    #if form1.validate_on_submit():
    #    get_or_create_follow(username=form1.new_follow.data)
    #    return redirect(url_for("index"))
    #    flash_string = '***** Followed User {}! *****'.format(form1.new_follow.data)
    #    flash(flash_string)

    if form3.validate_on_submit():
        id_in = form3.tweet_id.data
        print("ID IN = " + str(id_in))
        get_or_create_like(tweet_id_in=id_in)
        return redirect(url_for("index"))

    if form6.validate_on_submit():
        comment_in = form6.comment_text.data
        tweet_id_in = form6.comment_tweet_id.data
        print("ATTEMPTING TO CREATE COMMENT")
        get_or_create_comment(comment_in=comment_in, tweet_id_in=tweet_id_in)
        return redirect(url_for("index"))

    form2 = CreateTweetForm()
    if form2.validate_on_submit():
    	get_or_create_tweet(text=form2.tweet.data)
    	return redirect(url_for("index"))

    #print(tweets)
    #print(tweets_condensed)

    tweets_condensed.reverse()
    tweets.reverse()

    #for item in tweets_condensed:
        #print("ITEM: " + str(item))

        ##dead
        #for this_object in item:
            #next_object = this_object.id
            #if form3.validate_on_submit():
            #    print('THIS_OBJECT' + str(this_object))
            #    get_or_create_like(tweet = next_object)
            #    return redirect(url_for("index"))
        #for this_object in item:


        ##alive
        #next_object = item.id
        #if form3.validate_on_submit():
            #get_or_create_like(tweet = next_object)
            #return redirect(url_for("index"))

    return render_template('index.html', form2=form2, form3=form3, tweets=tweets, form6=form6)

@app.route('/explore',methods=["GET","POST"])
def explore():
    users = db.session.query(User).all()

    form1 = CreateFollowForm()

    if form1.validate_on_submit():
        get_or_create_follow(username=form1.new_follow.data)
        return redirect(url_for("index"))
        flash_string = '***** Followed User {}! *****'.format(form1.new_follow.data)
        flash(flash_string)

    return render_template('explore.html', form1=form1, users=users)

@app.route('/your_posts',methods=["GET","POST"])
@login_required
def your_posts():
    tweets = db.session.query(Tweet).filter_by(user_id = current_user.id).all()
    return render_template('your_posts.html', tweets=tweets)

@app.route('/your_likes',methods=["GET","POST"])
@login_required
def your_likes():

    form5 = UpdateLikeForm()
    likes = db.session.query(Like).filter(Like.user_id == current_user.id).all()
    filtered_tweets = []

    for x in likes:
        if x not in filtered_tweets:
            filtered_tweets.append(x)
    print("LIKES_TWEETS" + str(likes))

    if form5.validate_on_submit():
        delete_like(post_to_be_deleted = form5.delete_like.data)
        #delete_object.delete()
        db.session.commit()

        return redirect(url_for("your_likes"))

    return render_template('your_likes.html', likes=likes, form5=form5)


@app.route('/your_comments',methods=["GET","POST"])
@login_required
def your_comments():

    comments = db.session.query(Comment).filter(Comment.user_id == current_user.id).all()

    return render_template('your_comments.html', comments=comments)

@app.route('/your_weather',methods=["GET","POST"])
@login_required
def your_weather():

    location_query = db.session.query(User).filter_by(id = current_user.id).first()
    location = location_query.location

    form4 = UpdateLocationForm()

    if form4.validate_on_submit():
        update_location(location = form4.new_location.data)
        return redirect(url_for("your_weather"))

    current_weather = get_weather(location)


    return render_template('your_weather.html', location=location, location_query=location_query, form4=form4, current_weather=current_weather)

if __name__ == '__main__':
    db.create_all()
    manager.run()