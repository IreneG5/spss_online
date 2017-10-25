# easySPSS (spss-online)
###### E-commerce & Blog web application with User Authentication, PayPal Payments and Support Tickets functionality.

This is my final project for the Code Institute's Full Stack Developer Online Program. 

easySPSS is a fictional e-commerce platform. The content is based on the company I work for, which currently uses digital marketing to promote SPSS software but only sells it through more traditional channels. I decided to build this particular app because it is in my company's plans to move to an e-commece model in the near future.

You can view the deployed version on http://spss-online-herokuapp.com

## Content:
- [Overview](#overview)
- [User roles](#user-roles)
- [Technology used](#technology-used)
- [Architecture / Structure](#architecture--structure)
  - [Apps](#apps)
  - [URLs](#urls)
  - [Models](#models)
  - [Templates](#templates)
  - [Views](#views)
- [Deployment](#deployment)
- [Databases / Static & Media Files](#databases--static-and-media-files)
- [Testing](#testing)
  - [Manual tests](#manual-tests)
  - [Automated tests](#manual-tests)
  - [Testing tables](/testing_tables.md)
- [Installation](#installation)
- [Challenges and known bugs](#challenges-and-known-bugs)
- [Future additions and improvements](#future-additions-and-improvements)


## Overview
The objective of this website is to sell SPSS software (licenses) online through PayPal, provide support to active customers and help visitors learn more about SPSS software and the world of Analytics in a blog.


## User Roles
There are 4 different user roles with different access levels (more detailed information in [views](#views) and [testing](#testing) section). 
Each user is shown specific messages for them in the different parts of the website (status, informational, different call to actions, etc.). 
Below you can find an overview of the functionality of each user type:

- **Visitors**: These are users of the site that are not logged in. They can view the main parts of the website 
but have some limitations. Visitors: 
  -  can't buy products
  -  can't vote or comment in blog posts
  -  can't access "My Profile" page
  -  can't access "My Tickets" page
  -  see a call to action box in the products page encouraging them to register

    To identify these type of users I use the `is_authenticated` field of the `User Model`, which returns True if the user is logged in and False otherwise.

- **Registered users/inactive customers**: These are users that registered to the web page using the registration form and are logged in, but they are not current customers. 
  - **Registered users**: they don't have an active license because they haven't bought any products yet.
  - **Inactive customers**: they don't have an active license because the products they bought have expired and they have not renewed the licenses. 
  
  I decided to unify these 2 users types in the same use case becauses they have almost the same needs. The main differences are:
  - Inactive customers might have old cases, and it makes sense that they can still access those 
  tickets for future reference. It also makes sense for registered users to see this section as it is a way to encourage them to buy a product so they can access this functionality.
  - Inactive customers have old products that are shown in the profile page with a link the products page for reference and to encourage them to buy them again. It also makes sense to show this section to registered users so that they know where their products would be if they were to buy them.
  
  These user types have visitors' access level plus:
  - can vote and comment in blog posts
  - can see their profile
  - can see the tickets page, but can't open new tickets or edit existing ones (if any)
  - see a call to action with a discount offer in the profile and products pages.

  To identify these type of user, I use a new attribute called `is_customer` that is defined in the `User Model` by checking if the user has any purchase with an active license. If that is the case, 
  `is_customer` is set to True, otherwise it is set to False, which is the case for these type of users.
  (More information about active licenses in the [products](#products) section)


- **Active Customers**: These are registered users that have at least one product with an active license. 

  They have registered users' access plus:
  - can open an update tickets
  - can see their active products in the products page
  - see a call to action with a link to contact us in the products and profile page
  
  To identify these type of users, I use the attribute `is_customer` explained above. In this case this attribute is set to True. (More information about active licenses in the [products](#products) section)


- **Staff**: These are easySPSS employees with admin rights. Staff users are created by other admin users by setting the `is_staff` field of the `User Model` to True, (or in the terminal as a superuser). 
  
  In addition to what the other users can do, staff users:
  - can manage the admin part of the website
  - can create products, blog categories and blog posts from the admin panel
  - can add comments and close/reopen all customers' tickets within the admin panel or through the front end (comments form and buttons on the ticket detail page)
  - can't see "My Products" section in the profile (as there is no need to)
  - see a the tickets table in a different format (in the profile and tickets page), which includes the name of the customer that opened each ticket, the status code instead of the full status, and other minor differences. 
  - can't open new tickets from the ticket's page, only from the admin panel, as the ticket has to be assigned to the customer in order for the customer to see it in "My Tickets" section. Staff will be able to assign tickets to customers on the admin panel.
  - see a box with shortcuts to other sections in the profile and products page instead of the other calls to action.

  To identify these type of users, I use the `is_staff` field of the `User Model`.
  
  

## Technology used

- **Django Framework** – The project is built in Django, using a django app for each piece of functionality or website section. (More information on the [apps](#apps) section).
- **HTML, CSS** – For templates and styles.
- **Javascript (jQuery)** – For improving UX and adding extra functionality (e.g. carousel in the home page and tool tips in the products page.)
- **Bootstrap** – To structure and style the templates (e.g. glyphycons, alerts, tables, etc.)
- **Flatpages** - To create the simple about us page
- **Disqus** - To allow users to add comments in the blog posts
- **SQLite Database** – To store the models when working on local environment



## Architecture / Structure

### Apps

#### spss_online
Is the project's main app. Contains `urls.py` and configuration files.

#### home
home app populates the home page of the website, which contains some information about the company as well as shortcuts to other parts of the web app.


#### accounts
accounts app manages everything related to the users. The `custom auth model` allows user registration and authentication. 
Additional functionality: 
- The user receives a welcome email when they register
- When the user is logged in they can see their information in the profile page
- Interacts with other apps to show products and tickets in the profile page

There are 3 important fields that are used to manage the functionality of the different users: 
- is_authenticated: to check if the user is logged in
- is_staff: to check if the user is a member of the staff of easySPSS
- is_customer: (defined in the User model) to check if the user has an active license and is, therefore, a customer. 

  (More information on user roles in the [user roles](#user-roles) section)



#### products
products app manages everything related to the company's products and the purchases made by the users in two different models, Products and Purchases.
- Products are added via Django's admin panel. 
- Purchases are saved when the user buys a product via PayPal or one is added in the admin panel.
- It receives the PayPal signal and sends the information to the PayPal app.
- Apart from other fields, Purchase model contains a field called `license_end`, which is used to define if the user is an active customer or not. This date field is calculated when the user makes a purchase by adding 1 or 2 years (depending on the license type) to the date of the purchase. If there is at least one purchase with a licence_end greater than now, the user is considered an active customer.
  - This field is also used to highlight the licenses as active, expiring soon or expired. This 
enables us to show the right message in the products section of the profile page and to show only what is active in the products page. 
  - This field is also used when a user is opening a new ticket as it is only allowed to open a ticket related to a product with an active license. (More information on the [tickets](#tickets) section).


#### paypal_store
paypal_store app manages the PayPal functionality to make the purchases possible. It processes the ipn signal from PayPal after a purchase is made and shows the purchase's information on the return page.
The note in the paypal_return template indicating the user that they will receive an email is just what should happen in the real world, but it is not implemented in this project.

#### blog
blog app manages everything related with the functionality of the blog and its blog posts. It contains 3 models, Blog, Post and Vote. In the front end it shows the different blog posts in the blog page, giving the user the ability to click on them to see the blog post details. 
- In the blog post detail, users can see the details, the image and the content of the blog post, as well as the number of views and the score (summary of votes) that the blog post has received. 
- Visitors and users can use the tweet button to tweet an editable message pre-defined with the title and the url of the blog post.
- If the user is logged in, they can up-vote or down-vote the blog post and the numbers will be automatically updated. A user can only vote on a blog post once. 
- If the user is logged in, the user will also be able to add a comment using the disqus section below the post content. 
- On the right hand side of the blog and blog post page there are two boxes showing the "Top 3 voted" and "Top 3 viewed" blog posts in descencing order (by score and number of views respectively). This boxes are automatically updated every time a user votes or views a blog post.


#### tickets
tickets app manages everything related to customers' support cases (tickets).
- Customers can open new tickets, but only for their products with an active license (e.g. If a user bought a 2 year license for SPSS Statistics 24 and a 1 year license for SPSS Modeler 18 18 months ago, it will only be possible to open a case for SPSS Statistics 24. If the customer has more than one active license for the same product, it will only be showed once in the ticket form, and the user can get support for all licenses of the same product.
- Customers can also add comments to open tickets, close the open tickets and reopen them again
- The status of the ticket changes automatically, starting with "New" when the ticket is created and is updated according to the last user that commented: if it was the customer, the status changes to Pending easySPSS Response (PER); if it was a staff user, it changes to Pending Customer Response (PCR). It changes to closed when the case is closed and back to PER or PCR when its reopened. 
- The customer receives a notification email when a member of staff adds a comment.
- If a ticket is still open when the license of the product it is related to expires, the user will be able to update it as long as they have another active license for the same or other product.
- If a case is still open when the license expires and the user does not have any other active licenses, the user won't be able to update the ticket, instead, there is a message at the top of the page advising the user to contact easySPSS to finish with the resolution of the case. Staff members will be able to edit/close the ticket for them.
- Staff members can add comments to any customer ticket, but can't open cases from the app as the form automatically takes the logged user as the owner of the ticket. Staff members can create tickets from the admin panel as it is possible to select the owner (user) of the ticket from there. 
As in the admin panel is not possible to show together tickets and comments forms, staff users will need to create a ticket first and then a comment associated to that ticket. If a particular ticket doesn't have at least one comment, it will not be shown in the ticket's table.


#### contact
Simple app that manages the contact us section of the website. It renders the contact.html template, which includes information on how to contact easySPSS and a Google Maps map embedded on the page using Google Maps Embed API.
It contains a contact form that any user, logged or not, can fill in. If the user is logged in, the form pre-populates the fields with the user's details. The visitor will receive a "thank you for your query" email, and an email will be sent to easySPSSweb@gmail.com as a notification to the staff Team indicating they have received a query.


### URLs

The main `urls.py` file is stored at the project level(`spss-online`), and provides the url patterns routes to the different views that allow the navigation and functionality of the web app.
    `from accounts import views as account_views`
    `urlpatterns = [url(r'^profile/$', accounts_views.profile, name='profile'), ...]`


Blog and Tickets apps contain their own `urls.py` with their specific routes and are included in the `urls.py` at the project level via the 'include' function.
`urlpatterns = [url(r'', include('blog.urls')), ...]`


### Models

They represent the data model for each app in the form of a relational database. Each app's models are defined in the `models.py` file located inside the app folder.

**Overview**:

|App|Model|fields|
|---|---|---|
|accounts|User|username, email,  password,  is_staff, is_superuser, is_active, first_name, last_name, date_joined, company, is_customer (attribute)|
|||
|blog|Category|name|
|blog|Post|author(FK), title, content, created_date, published_date, category(FK), image, views, score|
|blog|Vote|user (FK), post, vote|
|||
|contact|Contact|first_name, last_name, email, query|
|||
|products|Product|code, name, osystem, description, price, license_type, image|
|products|Purchase|user (FK), product (FK), license_end|
|||
|tickets|Ticket|subject, user (FK), status, reason, product (FK), opened_date, closed_date|
|tickets|Comment|ticket (FK), user (FK), comment, created_date|



### Templates

Visual representation of the data model. All templates are stored in the `templates directory` at the project level. For the more complex apps, there are some subdirectories with the app name.

**base.py** at the top level defines the main visual structure of the web app. It includes, in this order:
- Head
   - links to CSS and JavaScript libraries and files in the head
- Body
  - the navigation bar
  - a space to show information messages to the user, e.g. log in successfully, errors, etc.
  - a block to insert other templates
    `{% block content %}`
    `{% endblock %}`
  - the footer

**Main pages and app specific templates** are inserted into `base.py`. Some of these templates also include other templates within them, e.g. the call to actions on the right side of the products page are inserted using the indclude tag  `{% include 'template url' %}`

Some templates are receiving data from views from more than one model. This is the case, for example, of the profile page, which shows information from the `User model`, but also information from the `Purchase model` and the `Ticket model` in the Tickets section.

Some templates use `templatetags` to get some information from the models withouth having to go through a view. These template tags are stored in the `templatetags directory` of each app (in this case in `products`, `blog` and `tickets` apps), in a file called `name_extras.py`. 
They use different types of tags depending on the functionality: simple_tag, inclusion_tag or filter.

|App|Templatetag|Type|
|---|---|---|
|products|paypal_form_for|simple_tag
|blog|get_most_voted_posts|inclusion_tag|
|blog|get_most_viewed_posts|inclusion_tag|
|tickets|get_total_ticket_comments|filter|
|tickets|last_comment_user|simple_tag|
|tickets|last_comment_date|simple_tag|
|tickets|comment_date_humanized|simple_tag|

There are also two templates to customise the 404 and 500 error pages:
- 404.html: identifies if the user was looking for:
  - a particular ticket number that doesn't exist by checking if the URL matches the `tickets-detail` URL,  
  - a particular blog post that doesn't exist by checking if the URL matches the p`ost-detail` URL
  It shows a general message otherwise
- 500.html: shows a message advising the user to refresh the page or contact the company if the problem persists


### Views

Views are Python functions that define the business logic that link the templates to the models. They are called on the URL patterns, run the action/functionality and render the template requested.
Views are stored in the `views.py` file inside each app.

**Overview**:

|App|View|Models used|Return to page|
|---|---|---|---|
|accounts|register|accounts.User|register|
|accounts|profile|accounts.User, products.Purchase, tickets.Ticket|profile|
|accounts|login	|accounts.User|login|
|accounts|logout|accounts.User|index|
||||		
|blog|	post_list|blog.Post|blog posts|
|blog|	post_detail|blog.Post|blog posts|
|blog|	post_voteup|blog.Post, blog.Vote|post detail|
|blog|	post_voteup|blog.Post, blog.Vote|post detail|
||||
|contact|get_contact|accounts.User|contact|		
||||
|home|get_index	||index|
||||
|paypal_store|paypal_return|accounts.User, products.Purchase|paypal return|
|paypal_store|paypal_cancel|||
||||
|products|all_products|products.Product, products.Purchase|products|
||||
|tickets|tickets_list|tickets.Ticket, tickets.Comment	|tickets list page|
|tickets|tickets_detail|tickets.Ticket, tickets.Comment	| ticket detail page|
|tickets|new_ticket|tickets.Ticket, tickets.Comment, accounts.User, product.Product, products.Purchase|ticket detail|
|tickets|new_comment|tickets.Ticket, tickets.Comment, accounts.User		|ticket detail|
|tickets|close_ticket|tickets.Ticket|ticket detail|
|tickets|reopen_ticket|tickets.Ticket|ticket detail|
|tickets|delete_comment|tickets.Ticket, tickets.Comment	|ticket detail|


# Deployment

This project was deployed in Heroku and it uses automatic deploys from GitHub ([spss-online master branch](https://github.com/IreneG5/spss_online)



# Databases / Static and Media Files

- Phase 1 - Local development using SQLite to manage the DB. All the Static and Media files were stored locally during this phase.
- Phase 2 - Deployment and local development with remote static & media files. An AWS account was set up to manage and host all the static and media files. Settings were updated accordingly to point to the online resources.
The database is now hosted in Heroku and MySQL Workbench is used to query it (if needed).


# Testing

### Manual tests

All the apps have been extensively tested manually. Template rendering, forms, links, exceptions, etc. 

Some apps' functionality varies depending on the type of user logged in. Different user types have been used to do the manual tests 
(visitor, registered user/inactive customer, active customer and staff).

Below you can find a list with the users available for testing. Please do not take any action that changes the user type of the user (e.g. 
buy a product using an inactive user). To run more extensive tests please register a new user, you will be able to buy products, open tickets, etc. If you would like to test  other functionality not available through this new user (e.g. see a product with 
a license that is about to expire in the profile page), install and run the app locally and change the relevant fields in the 
database, or let me know and I will do it for you in the deployed version.

- Staff user: please send me an email to irene.g5555@gmail.com to get the details.
- Active Customer: arya.stark@gmail.com (password: 123) and jon.snow@gmail.com (password:123)
- Registered User (was never a customer): rose.tyler@gmail.com (password: 123)
- Inactive Customer (was a customer): jessica.jones@gmail.com (password: 123)


[Here](testing_tables.md) you can find a series of tables with a summary of the tests. I have only included the ones that tested a more complex functionality that changes depending on the type of user or other parameters.

Additional manual tests were run on the products and paypal_store apps due to their complexity.
(More information in the [challenges and known bugs](#challenges-and-known-bugs) section).

The responsiveness of the site have also been tested extensively. 


### Automated tests

Automated tests are available for the most complex apps: accounts, products, blog and tickets. Each app contains a `tests.py` file where the tests for that app are stored.

You can find a summary table with all the tests in the second section of [this file](testing_tables.md).



# Installation

Follow the instructions below to clone the project and install it in your local computer.
1. Clone the repository from Github or via terminal
2. Create and activate a new virtual environment via terminal or in a tool like Pycharm
3. Install the project dependencies (requirements.txt)
4. Create AWS Bucket and keys and store them in a secure place
5. Set up a PayPal account and change the details in settings accordingly
6. Run all migrations
7. Test in 127.0.0.1:8000
8. Note that there won't be any products or blog posts as your local database is empty.
There is a testing database that you can use to populate some products, blog posts and users [here](db.sqlite3)
10. Generate a superuser and login to the admin panel to add more blog posts and products.


NOTE: The master branch is linked to Heroku to deploy automatically.

Deployed version in Heroku: []https://spss-online.herokuapp.com/]



# Challenges and known bugs

The lessons in the course were referring to a PayPal API signal that was no longer valid. I had to do a lot of research to be able to properly read and process the signal.
I ran many manual tests by buying products through the sandbox and encountered many difficulties such as the Paypal site not rendering properly sometimes, the signal being delayed and duplicated, the sandbox accounts being deactivated, etc.

For the first phase of the project I used ngrok to simulate a server and be able to test PayPal, but the free version has a lot of limitations. I did test concurrent purchases from 2 different users and half of the times it worked and half of the time it only saved 1 purchase.
On the second phase, using the deployed version, all of the latest tests passed. If there is an issue with the signal and django can't process it, an error will be shown on the screen. 
If that happens, there is a high probability that it will be solved by refreshing the page as indicated in the message to the user. But as previously said, all the latest tests passed without any problem.  

Most of the python files have been validated for pep8 requirements using [PEP8 Online](http://pep8online.com/).

The source code of the published pages have been validated with [W3C MarkUp Validator Center](https://validator.w3.org/). There are some known errors in some pages such as: the "Tweet" functionality in the blog post section, which contains spaces in the href value of the link as the pre-populated text is built using the title value of the blog post; and duplicated IDs in the products page, due to the paypal_form_for created as many times as the number of products.  

**Update 25th October 2017 - Note for Project Assessors**

Since yesterday 24th October in the evening, I have been having problems testing the PayPal functionality. 
IPN signals don't seem to be coming through when they should, so the functionality when returning to paypal_return
after making a purchase is not behaving properly.
Tests run last night showed that no signal was coming through, therefore, a new purchase was not being created in the DB
and the paypal_return page was returning a message saying there was a problem processing the purchase. I thought it 
was a problem with my code so I tried reverting the latest changes, making some new commits, but nothing seemed to be working. 
This morning, all yesterday's signals suddenly came through and the new purchases were saved.
Later in the morning some tests were passing and others were failing, randomly from my perspective as within a 5 minute
time-frame and not making any changes in the code the results were different, e.g. one purchase was not saved, another
one was saved after a few  minutes, and another one worked fine.
Having said that, if you encounter any problem when testing the purchasing process, I would suggest that you to try again 
a few minutes, or even hours, later. 


# Future additions and improvements

I have some ideas that I didn't have the time to build for this project, but that I will probably keep working on
if this app goes into production for my company. 
- **Purchase Name**: Add a field to the Purchase model to save the name of the purchase after it is successfully saved
 (in the paypal_return page).
It will allow users to add a name that will be shown in the products and profile pages so that they can 
easily locate it. E.g. names "SPSS 24 Anna's Laptop", "Main computer training room".
- **Ticket History**: Add a new model to Tickets to store the historical events with dates. E.g. change of status, new comments, etc.
- **Sortable Columns**: Make the columns in the tables sortable.
- **Loading Spin**: Add a template with a loading spin to render while the user is waiting for the site to come back from the PayPal site 
to the paypal_return page.
- **Tickets Stats Graph**: Add a graph to show users how many cases have been opened/closed in the 30 days using [django chartit](https://github.com/chartit/django-chartit). 



### Thank you for visiting my project :)
