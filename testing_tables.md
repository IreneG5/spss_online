## Manual Tests
**Menu**
|Area/page|No.|User Type|Functionality|Test Condition(Pre-condition) |Test Case|Expected Result|Steps to replicate|Pass/Fail|Remarks|
|---|---|---|---|---|---|---|---|---|---|
|menu|1|Visitor|View Register/Login Menu in all pages|Not logged user|If the user can see the register and login menu items|Should be able to see the menu items to log in and register|Access website without login in|Pass||
|menu|2|Visitor|Not logged users can't see My Profile, My Tickets and Log out|Not logged user|If the user can see My Profile, My Tickets and Log out items in the menu|Should not be able to see My Profile, My Tickets and Log Out items in the menu||Pass||
|menu|3|Any logged in|View My Profile, My Tickets and Log out items in the menu|Logged user|If the user can see My Profile, My Tickets and Log out items in the menu|Should be able to see My Profile, My Tickets and Log Out items in the menu|Access website, log in and check the menu|Pass||
|menu|4|Any logged in|Doesn't view Register and log in items in the menu|Logged user|If the user can see Register and Log in items in the menu|Shouldn't be ablet o see Register and Log in in the menu|Access website, log in and check the menu|Pass||
**Home**
Home page content is similar for all users

**Products**

|Area/page|No.|User Type|Functionality|Test Condition(Pre-condition) |Test Case|Expected Result|Steps to replicate|Pass/Fail|Remarks|
|---|---|---|---|---|---|---|---|---|---|
|products|1|Visitor|View Call to action (cta) box to register on the right side column|Not logged user|If the user can see the register cta box|Should be able to see the register cta box|Access products page without login in|Pass||
|products|2|Visitor|Not logged users can't buy products|Not logged user|If the user can see the login/register message before the products and login message in each product box instead of the Subscribe Paypal Button|The user should see the login/register message before the products and login message in each product box instead of the Subscribe Paypal Button|Access products page without login in|Pass||
|products|3|Any logged in|View subscribe buttons to buy products|Logged user|If the user can see the button to buy products|Should be able to see the button|Access the website, log in with any user and check the products page|Pass||
|products|4|Active Customer|View active products on the right column|Logged user that is not an active customer|If the user can see the active products|Shouldn't be able to see the active products as it doesn't have any|Access the website, log in with an inactive customer user and check the products page|Pass||

**PayPal**
|Area/page|No.|User Type|Functionality|Test Condition(Pre-condition) |Test Case|Expected Result|Steps to replicate|Pass/Fail|Remarks|
|---|---|---|---|---|---|---|---|---|---|
|paypal_store|1|Any logged in|Buy product through Paypal and details are saved in user's purchases|Logged user|If the user can buy a product using Paypal easySPSS store|Should be able to go through the paypal process and see the paypal-return page with the last purchase when finished|Access the website, log in, go to products page, click Subscribe button in a product, go through the paypal process and when it finish click on Return to Merchant's website|Pass|Sometimes if the user click the button very quicky, there is an error on Heroku application "Application error. An error occurred in the application and your page could not be served. If you are the application owner, check your logs for details.", but refreshing the page solves the problem|
|paypal_store|2|Any logged in|Buy product through Paypal 2 concurrent users and details are saved correctly in each user's purchases|2 logged users|If the users can buy a product through paypal at the same time|Should be able to buy simultaneasly |Access the website from 2 different browsers and log in a different user in each. Go to products in both of them and follow the process to buy at the same time.|Pass||

**Blog**
Blog content is similar for all users

**Post Details**
|Area/page|No.|User Type|Functionality|Test Condition(Pre-condition) |Test Case|Expected Result|Steps to replicate|Pass/Fail|Remarks|
|---|---|---|---|---|---|---|---|---|---|
|post_details|1|Visitor|Not logged users can't vote blog posts|Not logged user|If the user can see the login to vote message instead of the voting icons||Access blog post page, click in one of the blog posts to see details and check content right beside number of views and votes in the blog post details|Pass||
|post_details|2|Visitor|Not logged users can't comment in posts|Not logged user|If the user can see the login to vote message instead of the disqus comments section||Access blog post page, click in one of the blog posts to see details and check content below the post detail.|Pass||
|post_details|3|Any logged in|Logged users can vote blog posts|Logged user|If the user can see the voting icons below the blog post details|Should be able to see the voting icons|Access blog post page, click in one of the blog posts to see details and check content right beside number of views and votes in the blog post details|Pass||
|post_details|4|Any logged in|Logged users can comment in posts|Logged user|If the user can see the disqus comments section below the post content|Should be able to see the disqus comments section|Access blog post page, click in one of the blog posts to see details and check content below the post detail.|Pass||

**Profile**
|Area/page|No.|User Type|Functionality|Test Condition(Pre-condition) |Test Case|Expected Result|Steps to replicate|Pass/Fail|Remarks|
|---|---|---|---|---|---|---|---|---|---|
|profile|1|Visitor|Redirect to login page if user not logged in|Not loggd in user|If the user gets redirected to login page when trying to access the profile|Should be redirected to login page|Type web URL + /profile |Pass||
|profile|2|Registered/Inactive Customer|View message inactive customer|Logged user that is not an active customer|If the user can see the message for inactive users in the profile page|Should be able to see the message|Access the website, log in with an inactive customer user and check the profile page|Pass||
|profile|3|Registered/Inactive Customer|View call to action box with offer|Logged user that is not an active customer|If the user can see the call to action box with the offer|Should be able to see that particular call to action|Access the website, log in with an inactive customer user and check the profile page|Pass||
|profile|4|Registered/Inactive Customer|View message inactive customer in Tickets section|Logged user that is not an active customer|If the user can see the message for inactive users in the tickets section of the profile page|Should be able to see the message|Access the website, log in with an inactive customer user and check the products page|Pass||
|profile|5|Active Customer|View message active customer|Logged user that is an active customer|If the user can see the message for active users in the profile page|Should be able to see the message|Access the website, log in with an active customer user and check the profile page|Pass||
|profile|6|Active Customer|View call to action box with contact us|Logged user that is not an active customer|If the user can see the call to action box with a contact us button|Should be able to see that particular call to action|Access the website, log in with an active customer user and check the profile page|Pass||
|profile|7|Staff|View message for staff user|Logged user that is staff|If the user can see the message for staff users in the profile page|Should be able to see the message|Access the website, log in with staff user and check the profile page|Pass||
|profile|8|Staff|View call to action box with shortcuts|Logged user that is staff|If the user can see the call to action box with the shortcuts|Should be able to see that particular call to action|Access the website, log in with a staff user and check the profile page|Pass||
|profile|9|Staff|View products section|Logged user that is staff|If the user can see the products section|Shouldn't be able to see the products section|Access the website, log in with a staff user and check the profile page|Pass||
|profile|10|Any logged user but staff|View products section with correct products and messages|Logged user that is not staff|If the user can see the products section with message for different licenses|Should be able to see all the products bought with a message for licenses expiring soon or expired|Access the website, log in with a user that has products and check the profile page|Pass||
|profile|11|Any logged user but staff|View tickets section with its own tickets|Logged user that is not staff|If the user can see the tickets section with all its tickets and the details|Should be ablet o see this section|Access the website, log in with a user that has tickets and check the profile page|Pass||
|profile|12|Staff|View tickets for all customers in tickets section|Logged user that is staff|If the user can see the tickets section with all customer's tickets and the details, including the customer that opened them|Should be ablet o see this section|Access the website, log in with a staff user and check the profile page|Pass||


**Tickets**
|Area/page|No.|User Type|Functionality|Test Condition(Pre-condition) |Test Case|Expected Result|Steps to replicate|Pass/Fail|Remarks|
|---|---|---|---|---|---|---|---|---|---|
|tickets|1|Visitor|Redirect to login page if user not logged in|Not logged user|If the user gets redirected to login page when trying to access the tickets page|Should be redirected to login page|Type web URL + /tickets|Pass||
|tickets|2|Registered/Inactive Customer|View message inactive customer|Logged user that is not an active customer|If the user can see the message for inactive users in the tickets page|Should be able to see the message|Access the website, log in with an inactive customer user and check the tickets page|Pass||
|tickets|3|Inactive Customer|View old tickets|Logged user that is not an active customer but has tickets.  At least 1 ticket exists for that user.|If the user can see its tickets|Should be able to see its tickets|Access the website, log in with an inactive customer user that has old tickets and check the tickets page|Pass||
|tickets|4|Active Customer|View Open New Ticket button|Logged user that is an active customer|If the user can see the button|Should be able to see the button|Access the website, log in with an active customer user and check the tickets page|Pass||
|tickets|5|Staff/Registered|View Open New Ticket button|Logged user that is staff of inactive|If the user can see the button|Shouldn't be able to see the button|Access the website, log in with a staff or inactive user and check the tickets page|Pass||
|tickets|6|Staff|View tickets table with customer name and status code|Logged user that is staff. At least 1 ticket exists.|If user can see the table with the customer name for each ticket|Should be able to see the table including Customer Name|Access the website, log in with a staff user and check the tickets page|Pass||
|tickets|7|Active Customer|Can Open New ticket|Logged user that is an active customer|If open ticket form renders when the button is clicked and saves the details when the form is valid|Should be able to fill the details and save the ticket|Access the website, log in with an active customer user, go to the tickets page and click Open New ticket, add the details and save|Pass||

**Ticket Detail**
|Area/page|No.|User Type|Functionality|Test Condition(Pre-condition) |Test Case|Expected Result|Steps to replicate|Pass/Fail|Remarks|
|---|---|---|---|---|---|---|---|---|---|
|ticket_detail|1|Visitor|Redirect to login page if user not logged in|Not logged user|If the user gets redirected to login page when trying to access the tickets page|Should be redirected to login page|Type web URL + /tickets|Pass||
|ticket_detail|2|Registered/Inactive Customer|View message inactive customer|Logged user that is not an active customer|If the user can see the message for inactive users in the tickets page|Should be able to see the message|Access the website, log in with an inactive customer user and check the tickets page|Pass||
|ticket_detail|3|Registered/Inactive Customer|Can edit the ticket|Logged user that is not an active customer but has tickets.  At least 1 ticket exists for that user.|If the user can see the buttons to add comments, close the ticket and open new ticket|Shouldn't be able to see the buttons|Access the website, log in with an inactive customer user that has old tickets, click in a ticket and check the ticket detail page|Pass||
|ticket_detail|4|Active Customer|Can edit the ticket|Logged user that is an active customer and has at least 1 ticket|If the user can see the buttons to add comments, close the ticket and open new ticket|Should be able to see the buttons|Access the website, log in with an active customer user that has tickets, click in a ticket and check the ticket detail page|Pass||
|ticket_detail|5|Staff|Can edit the ticket|Logged user that is an a staff user. At least 1 ticket exists.|If the user can see the buttons to add comments and close the ticket|Should be able to see the buttons|Access the website, log in with a staff user that has tickets, click in a ticket and check the ticket detail page|Pass||
|ticket_detail|6|Staff/Active Customer|Can add a comment to an existing ticket|Logged user that is staff. At least 1 ticket exists.|If the comment for renders and it saves the content when the form is valid|Should be able to fill the details and save the comment|Access the website, log in with a staff or customer user that has tickets, click in a ticket to go to the ticket detail page, click in Add comment and save the details|Pass||
|ticket_detail|7|Staff/Active Customer|Can close tickets|Logged user that is staff or active customer. At least 1 open ticket exists.|If the ticket changes to close when the button is pressed|Status should change to close, closed date should appear in the details and Reopen ticket button should be visible|Access the website, log in with a staff or customer user that has tickets, click in a ticket to go to the ticket detail page, click in Close Ticket|Pass||
|ticket_detail|8|Staff/Active Customer|Can reopen tickets|Logged user that is staff or active customer. At least 1 closed ticket exists.|If the ticket reopens when the button is pressed|Status should change to PCR or PER (depending on last comment's user)|Access the website, log in with a staff or active customer user, click in a closed ticket to go to the detail page and click Reopen Ticket|Pass||
|ticket_detail|8|Staff/Active Customer|Status changes to (PCR) Pending Customer Response when last comment is from a staff user|Logged user that is staff or active_customer. At least 1 open ticket exists and last comment is not from staff|If the ticket status changes to PCR when staff adds a new comment|Status should change to PCR (for all users) when the staff user adds a new comment|Access the website, log in with a staff user, click on an open ticket to go to the detail page and add a comment|Pass||
|ticket_detail|8|Staff/Active Customer|Status changes to (PER) Pending easySPSS Response when last comment iss from a customer user|Logged user that is staff or active_customer. At least 1 open ticket exists and last comment is not from customer|If the ticket status changes to PER when customer adds a new comment|Status should change to PCR (for all users) when the customer user adds a new comment|Access the website, log in with a customer user, click on an open ticket to go to the detail page and add a comment.|Pass||
|||||||||||


## Automated tests
All tests pass

|App|class|test|
|---|---|---|
|home|HomePageTest|test_index_menu_item_has_class_active|
|home|MenuVisitorUserTest|test_menu_shows_login_and_register_for_not_logged_users|
|home|MenuVisitorUserTest|test_menu_doesnt_show_profile_tickets_log_for_not_logged_users|
|home|MenuLoggedUserTest|	test_menu_doesnt_show_register_and_login_for_logged_users|
|home|MenuLoggedUserTest|test_menu_shows_profile_tickets_and_logout_for_logged_users|
|accounts|ProfilePageVisitorTest|def test_redirect_to_login_page_when_not_logged_in(self):|
|accounts|ProfilePageTest|test_profile_menu_item_has_class_active|
|accounts|ProfilePageTest|test_check_template_is_correct|
|accounts|ProfilePageStaffUserTest|test_check_user_type_message_is_staff_for_staff_user|
|accounts|ProfilePageStaffUserTest|test_check_cta_is_shortcuts_for_staff_user|
|accounts|ProfilePageStaffUserTest|test_check_products_section_not_shown_for_staff_user|
|accounts|ProfilePageActiveCustomerUserTest|test_check_user_type_message_is_active_for_active_customer_user|
|accounts|ProfilePageActiveCustomerUserTest|test_check_cta_is_contactus_for_active_customer_user|
|accounts|ProfilePageActiveCustomerUserTest|test_check_products_section_is_shown_for_active_customer_user|
|accounts|ProfilePageInactiveUserTest|test_check_user_type_message_is_inactive_for_inactive_user|
|accounts|ProfilePageInactiveUserTest|test_check_cta_is_offer_for_inactive_user|
|accounts|ProfilePageInactiveUserTest|test_check_products_section_is_shown_for_inactive_user|
|accounts|RegistrationFormTest|test_form_is_valid|
|accounts|RegistrationFormTest|test_form_fails_when_missing_password1|
|accounts|RegistrationFormTest|test_form_fails_when_missing_password2|
|accounts|RegistrationFormTest|test_form_fails_when_password_too_short|
|accounts|RegistrationFormTest|test_form_fails_when_password_not_numbers|
|accounts|RegistrationFormTest|test_form_fails_when_password_not_letters|
|accounts|RegistrationFormTest|test_form_fails_when_password_dont_match|
|accounts|RegistrationFormTest|test_form_fails_when_email_not_unique|
||||
|blog|BlogPageTest|test_blog_menu_item_has_class_active|
|blog|PostDetailPageTest|test_blog_menu_item_has_class_active|
|blog|PostDetailPageVisitorUserTest|test_voting_not_shown_for_visitors|
|blog|PostDetailPageVisitorUserTest|test_login_shown_for_visitors_instead_of_voting|
|blog|PostDetailPageVisitorUserTest|test_comments_not_shown_for_visitors|
|blog|PostDetailPageVisitorUserTest|test_login_shown_for_visitors_instead_of_comments|
|blog|PostDetailPageLoggedUserTest|test_voting_shown_for_logged_users|
|blog|PostDetailPageLoggedUserTest|test_login_not_shown_for_logged_users|
|blog|PostDetailPageLoggedUserTest|test_comments_shown_for_logged_users|
|blog|PostDetailPageLoggedUserTest|test_login_not_shown_for_logged_users_instead_of_comments|
||||
|products|ProductsPageTest|test_products_menu_item_has_class_active|
||||
|tickets|TicketsPageVisitorTest|test_redirect_to_login_page_when_not_logged_in|
|tickets|TicketsPageTest|test_tickets_menu_item_has_class_active|
|tickets|TicketDetailPageTest|test_tickets_menu_item_has_class_active|
|tickets|TicketsPageInactiveUserTest|test_message_shown_for_inactive_user|
|tickets|TicketsPageInactiveUserTest|test_open_ticket_button_not_shown_for_inactive_user|
|tickets|TicketsPageActiveCustomerUserTest|test_message_not_shown_for_active_user|
|tickets|TicketsPageActiveCustomerUserTest|test_open_ticket_button_shown_for_active_user|
|tickets|TicketsPageStaffUserTest|test_message_not_shown_for_staff_user|
|tickets|TicketsPageStaffUserTest|test_open_ticket_button_not_shown_for_staff_user|
|tickets|TicketsPageStatusNewTest|test_ticket_status_new_for_new_ticket|
|tickets|TicketsPageStatusPCRTest|test_ticket_status_PCR_when_last_comment_by_staff|
|tickets|TicketsPageStatusPERTest|test_ticket_status_PER_when_last_comment_by_customer|
|tickets|TicketDetailPageDeleteCommentsTest|test_staff_can_delete_comments_if_more_than_one|
|tickets|TicketDetailPageCantDeleteCommentsTest|test_staff_cant_delete_comments_if_less_than_two|
|tickets|TicketDetailPageInactiveUserTest|test_message_shown_for_inactive_user|
|tickets|TicketDetailPageInactiveUserTest|test_buttons_not_shown_for_inactive_user|
|tickets|TicketDetailPageClosedTicketTest|test_buttons_not_shown_for_closed_ticket|
|tickets|TicketDetailPageClosedTicketTest|test_reopen_buttons_shown_for_closed_ticket|
|tickets|TicketDetailPageClosedTicketTest|test_close_date_shown_for_closed_ticket|
