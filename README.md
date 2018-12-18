# SI 364 - Fall 2018 - Final Project

#Project Description:
#For this project, I created a created an interactive post-making tool similar to Twitter. Initially, I wanted it to mimic Twitter's functionality, but decided to go a slightly different route and focus on the data manipulation. This application, which I've called Poster, has a main "feed" where you can view posts that users that you've elected to follow have made, routes within which you can view your liked and commented posts, an "Explore" page on which you can view all of the users currently registered on the platform and in the db, and a route within which you can view the weather in your location (uses DarkSky API). To get started, I would strongly suggest creating 3-4 users, creating some posts for each, and following each of these users. Having done this, you should have a feed populated by the posts of different users, but only by those of whom you've chosen to follow. Note: You'll see in the backend that I reference "tweet" and "tweets" a lot. This is because I decided to transition from "Twitter" to "Poster" late in the development process. I kept the definitions so as to not interfere with what I've already done.


**Final project submission deadline: December 17, 2018 at 11:59 pm**

**Total: 3000 points** (potential for 300 points extra credit)

Late assignment policy does NOT apply; late projects are not accepted. If you have a concern about deadlines and dates please let Troy and an advisor in OSA know immediately.

## Overall

**You do NOT need to fork or clone this, and should not -- only the instructions live here.**

**YOU SHOULD READ THIS ENTIRE SET OF INSTRUCTIONS CAREFULLY BEFORE BEGINNING YOUR WORK.**

In this final project assignment, your goal is to build on provided code to build a complete working interactive application, using the material you have learned in this class. Requirements are listed below.

## Instructions and overall requirements

We have *not* provided any setup code for the final project (though in HW6, you will be working on some!). You will be building this project completely from scratch (with the basis of all you've already practiced and learned in SI 364, etc).

Note that some requirements are dependent upon another one being completed successfully, as in all applications!

This final project assignment may be of any theme or any subject you want, and involve any data (*as long as it is appropriate to share with our whole class, and does not include any discriminatory content* -- penalty may vary if this is the case. Please avoid it).

You may use any code that is exactly the same as code used in lecture or section or a previous HW.

You will NOT receive points for any code that you submitted for the midterm. **Keep this in mind if you plan to use a similar theme in this project as you used on the midterm.** Small amendments to it, additions, etc, if it was your own original work on the midterm, are fine and will count.

Reading code you have been given already, written already, and looking at examples from lecture, section, and past HW is one of the *best* ways to approach this. While you can't use the code directly, it can answer a lot of possible questions and provide great examples!
Visual design will not earn you points for this assignment though you may certainly include it if you want -- do *not* prioritize it over the functionality, which is what this final project assignment is about.


## Requirements to complete for 3000 points (100%) -- an awesome, solid app

*(I recommend treating this as a checklist and checking things off as you get them done!)*

### **Documentation README Requirements**

- [X] Create a `README.md` file for your app that includes the full list of requirements from this page. The ones you have completed should be bolded or checked off. (You bold things in Markdown by using two asterisks, like this: `**This text would be bold** and this text would not be`) and should include a 1-paragraph (brief OK) description of what your application does and have the routes


### **Code Requirements**
***Note that many of these requirements of things your application must DO or must INCLUDE go together! Note also that*** ***you should read all of the requirements before making your application plan******.***

- [X] Ensure that your `SI364final.py` file has all the setup (`app.config` values, import statements, code to run the app if that file is run, etc) necessary to run the Flask application, and the application runs correctly on `http://localhost:5000` (and the other routes you set up). **Your main file must be called** `SI364final.py`**, but of course you may include other files if you need.**

- [X] A user should be able to load `http://localhost:5000` and see the first page they ought to see on the application.

- [X] Include navigation in `base.html` with links (using `a href` tags) that lead to every other page in the application that a user should be able to click on. (e.g. in the lecture examples from the Feb 9 lecture, [like this](https://www.dropbox.com/s/hjcls4cfdkqwy84/Screenshot%202018-02-15%2013.26.32.png?dl=0) )

- [X] Ensure that all templates in the application inherit (using template inheritance, with `extends`) from `base.html` and include at least one additional `block`.

- [X] Must use user authentication (which should be based on the code you were provided to do this e.g. in HW4).

- [X] Must have data associated with a user and at least 2 routes besides `logout` that can only be seen by logged-in users.

- [X] At least 3 model classes *besides* the `User` class.

- [X] At least one one:many relationship that works properly built between 2 models.

- [X] At least one many:many relationship that works properly built between 2 models.

- [X] Successfully save data to each table.

- [X] Successfully query data from each of your models (so query at least one column, or all data, from every database table you have a model for) and use it to effect in the application (e.g. won't count if you make a query that has no effect on what you see, what is saved, or anything that happens in the app).

- [X] At least one query of data using an `.all()` method and send the results of that query to a template.

- [X] At least one query of data using a `.filter_by(...` and show the results of that query directly (e.g. by sending the results to a template) or indirectly (e.g. using the results of the query to make a request to an API or save other data to a table).

- [X] At least one helper function that is *not* a `get_or_create` function should be defined and invoked in the application.

- [X] At least two `get_or_create` functions should be defined and invoked in the application (such that information can be saved without being duplicated / encountering errors).

- [X] At least one error handler for a 404 error and a corresponding template.

- [X] Include at least 4 template `.html` files in addition to the error handling template files.

  - [X] At least one Jinja template for loop and at least two Jinja template conditionals should occur amongst the templates.

- [X] At least one request to a REST API that is based on data submitted in a WTForm OR data accessed in another way online (e.g. scraping with BeautifulSoup that *does* accord with other involved sites' Terms of Service, etc).

  - [X] Your application should use data from a REST API or other source such that the application processes the data in some way and saves some information that came from the source *to the database* (in some way).

- [X] At least one WTForm that sends data with a `GET` request to a *new* page.

- [X] At least one WTForm that sends data with a `POST` request to the *same* page. (NOT counting the login or registration forms provided for you in class.)

- [X] At least one WTForm that sends data with a `POST` request to a *new* page. (NOT counting the login or registration forms provided for you in class.)

- [X] At least two custom validators for a field in a WTForm, NOT counting the custom validators included in the log in/auth code.

- [X] Include at least one way to *update* items saved in the database in the application (like in HW5).

- [X] Include at least one way to *delete* items saved in the database in the application (also like in HW5).

- [X] Include at least one use of `redirect`.

- [X] Include at least two uses of `url_for`. (HINT: Likely you'll need to use this several times, really.)

- [X] Have at least 5 view functions that are not included with the code we have provided. (But you may have more!)


## Additional Requirements for extra points -- an app with extra functionality!

- [ ] (100 points) Include a use of an AJAX request in your application that accesses and displays useful (for use of your application) data.
- [ ]  (100 points) Create, run, and commit at least one migration. (We'll see this from the files generated and can check the history)
- [ ]  (100 points) Deploy the application to the internet (Heroku) — only counts if it is up when we grade / you can show proof it is up at a URL and tell us what the URL is in the README. (Heroku deployment as we taught you is 100% free so this will not cost anything.)



## **To submit**
- Commit all changes to your git repository. Should include at least the files:
  - `README.md`
  - `SI364final.py`
  - A `templates/` directory with all templates you have created inside it
  - May include others (e.g. may include a `static` folder if you are including or uploading static files, but this is not necessary!)
- Create a GitHub account called `364final` on your GitHub account. (You are NOT forking and cloning anything this time, you are creating your own repo from start to finish.)

- Submit the *link* to your GitHub repository to the **SI 364 Final Project** assignment on our Canvas site. The link should be of the form: `https://github.com/YOURGITHUBUSERNAME/364final` (if it doesn't look like that, you are probably linking to something specific *inside* the repo, so make sure it does look like that). You can include your API key separately in the text entry.

All set!
