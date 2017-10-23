# easySPSS
###### Ecommerce & Blog web application with User Authentication, Paypal Payments and Support Tickets functionality
Final project for the Code Institute's online program. easySPSS is a fictional ecommerce platform. The content is based on the company I work for, which currently uses digital marketing to promote SPSS software but only sells through more traditional channels. The reason I chose to build this web app is because it is in my company's plan to move to an ecommerce model in the future soon.

You can view the deployed version on http://spss-online-herokuapp.com

## Overview
The objective of this website is to sell SPSS software (licenses) online, provide support to active customers and help visitors learn more about SPSS software and the world of Analytics in a blog.

There are 4 different user roles with different access level (more detailed information in views and testing section). Each user can see specific messages for them in the different parts of the website (status messages, messages indicating funcionality or different call to actions. This is an overivew of their functionality:

- **Visitors** (not is_authenticated): People not registered or not logged in can view the main parts of the website but have some limitations, visitors: 
  -  can't buy products. 
  -  can't vote or comment in blog posts. 
  -  can't access "My Profile" page
  -  can't access "My Tickets" page
  -  see a call to action box to register in products page 

    To identify these type of users the code uses the `is_authenticated` field of the User model, which returns True if the user is logged in and False otherwise.

- **Registered users/inactive customers**: Users that registered to the web page using the registration form and are loged in but they don't have any active license. 
  - **Registered users**: they don't have an active license because they haven't buy any product yet.
  - **Inactive customers**: they don't have an active license because the products they bought have expired licenses and they have not renewed. 
  
  I decided to unify these 2 types of users in the same use case as they basically have the same functionality. The only differences are that: inactive customers might have old cases and it make sense that they can still access those tickets for future reference, but also makes sense for registered users to see this section as it is a way to encourage them to buy a product so they can access this functionality; inactive customers have old products that are shown in the profile page with a link the products page, and it also makes sense to show this section to registered users so they know where their products would be if they buy them.
- These type of users have visitors' access plus:
  - can vote and comment in blog posts.
  - can see their profile, tickets page and old tickets details (if any)
  - can't open new ticket or edit existing tickets.
  - see a call to action with a discount offer and a link to contact us in the profile and products pages.

  To identify these type of users the code uses: a new attribute called `is_customer` that is computed in the User Model by checking if that particular logged user has any purchase with an active license. If that is positive, `is_customer` is set up to True, otherwise it is set up to False - this last one is the case for these types of users. (More about active licenses in the products section)


- **Active Customers**: Customers are registered users that have at least one product with an active license. They have registered users access plus:
  - can open an update tickets
  - can see their active products in the products page. 
  - see a call to action with a link to contact us in the products and profile page
  
  To identify these type of users the code uses the attibute `is_customer` explained above. In this case this attibute is set up to True.(More about active licenses in the products section)


- **Staff**: Staff users are created by an admin by modifying the `is_staff` field of the User Model to True (or in the terminal as a superuser). In addition to what the other users can do, staff users:
  - can manage the admin part of the website
  - can create products, blog categories and blog posts from the admin panel
  - can add comments and close/reopen all customer's tickets within the admin panel or through the comments form and buttons on the ticket detail page. 
  - can't see "My Products" section in the profile.
  - see a different tickets table in the profile and tickets page that includes the name of the customer that open each tickets and the status code instead of the full status to save space.
  - can't open new tickets from the web page, only from the admin panel as the ticket has to be assigned to the customer in order for the customer to see it in "My Tickets" section.
  - see a box with shortcuts to other sections in the profile and products page instead of the other call to actions.

  To identify these type of users I use: 
    - the `is_authenticated` field of the User model to check they are logged in
    - the `is_staff` field of the User Model.
  
  
## Technology used
- **Django Framework** – The project is build in Django, using a django app for each piece of functionality / website section (see apps section for more information).
- **HTML, CSS** – For templates and styles.
- **Javascript (jQuery)** – For improving the UX and add extra functionality (e.g. carousel in the home page and tool tips in the products page.)
- **Bootstrap** – To structure and style the templates (e.g. glyphycons, alerts, tables, etc.)
- **Flatpages** - To create the simple about us page
- **Disqus** - To allow users to add comments to the blog
- **SQLite Database** – To store the models when working on local environment

## Architecture / Structure

### Apps

#### spss_online
Is the project's main app. Contains `urls.py` and configuration files.

#### home
It populates the home page of the website (`index.html`), which contains some information about the company as well as shortcuts to other parts of the web app.


#### accounts
Manage everything related to the users. The custom auth model allows user registration and authentication. 
More functionality: 
- The user receives an welcome email when he registers. 
- Any type of user can log in and out at any stage. 
- When the user is logged in he can see his information in the profile page
- Interacts with other apps to show products and tickets in the profile page
There are 3 important fields that are used to manage the functionality of the different users: 
- is_authenticated: to check if the user is logged in
- is_staff: to ckec if the user is a member of the staff of easySPSS
- is_customer: this attibute is computed in the User model. It checks the purchases that that customer has made and if there is at least one purchase with an active license it returns True
Different types of users are explained in another section of this file.



#### products
products app manages everything related to the company's products and the purchases made by the users in two different models.
- Products are added via Django's admin panel. Purchases are stored when the user buys a product via Paypal or added in the admin panel.
- It receives the paypal signal and send the information to the paypal app.
- Apart from other fields in the model, Purchase model contains a field called license_end, this is the field used to compute if the user is an active customer or not. This field is calculated when the user made the purchase, adding 1 or 2 years (depending on the license) to the date of the purchase. If there is at least one licence that ends in the future, the user is considered an active customer.
- This field is also used to identify the different users the customer has: active, expiring soon or expired. This allows to highligh them with the right message in the products section of the profile page, and show only the active one in the products page. 
- This field is also used when a user is opening a new ticket as it is only allowed to open a ticket for active products (see more in the tickets' app).



#### paypal_store
paypal_store app manage the paypal funcionality to make the purchases posible. It processes the signal from paypal after a purchase is made and shows the purchase's information on the return page.

#### blog
blog app manage everything related with the functionality of the blog and its blog posts. It shows the different blog posts in the blog page, giving the user the ability to click on them to go to the blog post details. 
- In the blog post detail users can see the details, image and content of the blog post, as well as the number of views and the score (votes) that the blog post has received. 
- Visitors and users can use the tweet button to tweet an editable pre-defined message with the title and the url of the blog post.
- If the user is logged in, the user can upvote or downvote the blog post and the numbers will be automatically updated. A user can only vote on a blog post once. 
- If the user is logged in, the user will also be able to add a comment using the disqus section below the post content. 
- On the right hand side of the blog and blog post page there are two boxes showing the "Top 3 voted" and "Top 3 viewed" showing the posts with the highest number of points. This boxes are dinamically changed every time a user vote or view a blog post.


#### tickets
Manages everything relate to customer's support cases (tickets).
- Customers can open new tickets, only for their products which have an active license (e.g. If user bought 18 months ago 2 year license for SPSS Statistics 24 Win 64 and 1 year license for SPSS Modeler Win24, will only be posible to open a case for SPSS Statistics 24 Win 64. If the customer has more than one active license for the same product it will only be showed once.
- Customers can also close the open tickets and reopen them again, and add comments to open tickets. 
- The status of the ticket changes automatically, starting with "New" when the ticket is created and updating according to the last user that commented: if it was the customer the status changes Pending easySPSS Response (PER), and if it was a staff user it changes to Pending Customer Response (PCR). It changes to closed when the case is closed and back to PER or PCR when its reopened. 
- The customer receives an notification email when a member of staff add a comment.
- If a case is still open when the license expires the user will be able to update it as long as it has another active license for the same or other product.
- If a case is still open when the license expires and the user doesn't have any other active license, the user won't be able to update the ticket, instead there is a message at the top of the page advising the user to contact easySPSS if that is the case to finish the resolution of the case. Staff members will be able to edit/close the ticket for them.
- Staff members can add comments to any customer case, but can't open cases from the app as, the form automatically takes the logged user as the owner of the ticket. Staff members can create tickets from the admin panel as it is possible to select the author from there. 


#### contact
Simple app that manages the contact us section of the website. It renders the contact.html template, which includes information on how to contact easySPSS and a Google Maps map embeded on the page using Google Maps Embed API.
It contains a contact form that anyone can fill in. If the user is logged in the form pre-populate the form with the user's details. The visitor will receive a "thank you for your query" email, and an email will be sent to easySPSSweb@gmail.com as a notification to the staff Team indicating they have received a query.

### URLs

The main urls.py file is stored at the project level(spss-online), and provides the url patterns routes to the differnt views that allow the navigation and funcionality of the web app.
    `from accounts import views as account_views`
    `urlpatterns = [url(r'^profile/$', accounts_views.profile, name='profile'), ...]`


Blog and Tickets apps contain their own urls.py with their specific routes and are included in the urls.py at a project level via the 'include' function.
`urlpatterns = [url(r'', include('blog.urls')), ...]`


### Models

Represent the data model for each app in the form of a relational database. Models related to each app are defined in the models.py file located inside the specific app.
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

Visual representation of the data model. All templates are stored in the templates directory at the project level and subdirectories with the app name for some apps.

**base.py** at the top level defines the main visual structure of the web app. It includes, in this order:
- Head
   - links to CSS and Javascript libraries and files in the head
- Body
  - the navigation bar
  - a space to show information messages to the user, e.g. log in successfully, errors, etc.
  - a block to insert other templates
    `{% block content %}`
    `{% endblock %}`
  - the footer

**Main pages and app specific templates** are inserted into base.py. Some of these templates also include other templates within them, e.g. the call to actions on the right side of the products page are inserted using  `{% include 'template url' %}`

Some templates are receiving data from views from more than one model. It is the case, for example, of the profile page, which shows the User model details but also information from the Purchase models in the Products section and the Ticket model in the Tickets section.

Some templates use `templatetags` to get some information from the models. These template tags are stored in the templatetags directory of each app (in this case in products, blog and tickets apps), in a file named `name_extras.py`. They use different types of tags depending on the funcionality: simple_tag, inclusion_tag or filter.

|App|Templatetag|Type|
|---|---|---|
|producsts|paypal_form_for|simple_tag
|blog|get_most_voted_posts|inclusion_tag|
|blog|get_most_viewed_posts|inclusion_tag|
|tickets|get_total_ticket_comments|filter|
|tickets|last_comment_user|simple_tag|
|tickets|last_comment_date|simple_tag|
|tickets|comment_date_humanized|simple_tag|

### Views

Views are Python funcions that define the busines logic that link the templates to the models. They are called on the URL patterns, run the action/functionality and render the template requested.
Views are stored in the `views.py` file inside each app.

**Overview**:

|App|view|models used|return to page|
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
This project was deployed in Heroku and it uses automatic deploys from GitHub

# Databases / Static & Media Files
- Phase 1: Local development
SQLite to manage the DB locally. All the Static and Media files were stored locally for the first phase of the project.
- Phase 2: Deployment and local development with remote static & media files
An AWS was set up to manage and host all the static and media files. Settings were updated accordingly to point to the online resources.
The database is now hosted in Heroku and MySQL Workbench is used to query it if need it.


# Testing

### Manual tests
All the apps have been extensively tested manually. Template rendering, forms, links, exceptions, etc. 
Different user roles have been used to test the different functionality in each app that works with different profiles (visitor, registered user/inactive customer, active customer and staff).
These are the users available for testing, please do not take any action that changes the user type of the user (e.g. buy a product using an inactive user). To run more extensive tests please register a new user, you can buy products and open tickets with that user. If you want to test other funcionality not available through this (e.g. see a product with a license that is about to expire in the profile page), install the app locally and change the relevant fields in the database or let me know and I will do it for you in the deployed database.
- Staff user: under request
- Active Customer: arya.stark@gmail.com pass: 123 or jon.snow@gmail.com pass:123
- Registered User (never was a customer): rose.tyler@gmail.com pass: 123
- Inactive Customer: jessica.jones@gmail.com pass: 123

[In this file](testing_tables.md) you can see a series of tables with an summary of the tests. I have only included the ones testing a more complex funcionality that depends on the type of user or other parameters.

Additional manual tests were run on the products and paypal apps due to their complexity.
More information about this challenge in the challenges and know bugs section.

### Automated tests
Automated tests are available for the most complex apps: accounts, products, blog and tickets. Each app contains a tests.py file where the tests for that app are stored.

You can see a summary table with all the tests in the second section of [this file](testing_tables.md).



# Installation

Follow the instructions below to clone the project and install it in your local computer.
1. Clone the repository in Github or via terminal
2. Create and activate a new virtual environment via terminal or in any tool like Pycharm
3. Install the project dependencies (requirements.txt)
4. Create AWS Bucket and keys and store them in a secure place
5. Set up a paypal account and change the details in settings accordingly
6. Run all migrations
7. Test in 127.0.0.1:800
8. Note that there won't be any products or blogpost as your local database is empty.
There is a testing database that you can use stored [here](db.sqlite3)
9.Generate a superuser and login to the admin panel to add more blogposts and products.


NOTE: The master branch is linked to Heroku to deploy automatically.

Deployed version in Heroku: https://spss-online.herokuapp.com/
Deployed version in custom domain: http://




# Challenges and known bugs

The lessons were referring to a paypal API signal that was no longer valid and I had to study and re-create the signal checking and processing functionality. I run manual tests buying products through the sandbox and encounter many difficulties such us the Paypal site not rendering properly sometimes, the signal being delayed and duplicated, the sandbox acounts being desactivated, etc.

For the first phase of the project I used ngrok to simulate a server and be able to test paypal, but the free version has a lot of limitations. I did test concurrent purchases from 2 different users and half of the times it worked and half of the time it only saved 1 purchase.
On the deployed version most of the tests passed. From time to time I get a 500 error when it is returning to the paypal_return page that I haven't been able to replicate. It is solved by refreshing the page. 
Also, when the user clicks very quickly in the "Return to Merchant" button after the purchase, sometimes it gets an Heroku error "Application error. An error occurred in the application and your page could not be served. If you are the application owner, check your logs for details.", that is is also solved by refreshing the page.




