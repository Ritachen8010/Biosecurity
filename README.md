# Biosecurity
- COMP639 Assignment 1 - Individual
- Student Name:Yingyue(Rita) Chen
- Student ID: 1126418

## Project Description
- This project is to develop a Python Web app functioning as a biosecurity guide, providing information on agricultural pests and weeds present in New Zealand. The Web comes with agricultural theme which is friendly-use interface that contain three different user role and access control: Agronomists, Staff and Administrator. 

+ User ID, Staff ID, Agronomists ID, Guide ID and Image ID is unique and primary key (cannot edit).

+ Username is unique(cannot edit).

- Agronomists - Able to view guide of pest and weed, manager their own account (edit name, password, address, email, and phone number).
- Staff - As a mid level of manager the web able to view agronomists list and manager guide infor(edit, delete and add new species) and manager their own account (edit name, email, work phone number).

- Admin - Hold the highest control to view agronomists, staff and guide details/add/edit/delete, and manager their own account (edit name, email, work phone number).

- According to the requirement above I have achieved most of the functions which is an easy and friendly interface, except the image function which still needs to fix the delete and edit.

## Web application structure
1. The whole Web structure has been refactoring by role. 
- `/Biosecurity`: Root directory of the project.
  - `/app`: Contains the Flask application and its modules.
    - `__init__.py`: Initializes the Flask application and brings together all the components.
    - `admin_view.py`: Contains routes and views for the admin.
    - `agro_view.py`: Contains routes and views for agronomists.
    - `connect.py`: Configuration file for database connection.
    - `database.py`: Contains database connection.
    - `guide_views.py`: Contains routes and views for guide.
    - `login_register_logout.py`: User authentication, registration, and logout.
    - `public.py`: Contains routes and views for public pages.
    - `staff_views.py`: Contains routes and views for staff.
    - `/templates`: Contains HTML templates for rendering views.
      - `xxx.html`: -------------------------------
      - (additional HTML templates for other views)
      - `xxx.html`: -------------------------------
    - `/static`: Contains static files such as CSS stylesheets and images.
      - `/css`: Contains CSS files for styling the web pages.
      - `/images.jpg`: image file.
  - `run.py`: The entry point to run the Flask application.
  
2. The web through 'POST' and 'GET' to fetches and displays the details to send the request to update the database. 
3. Use different HTML to redirect to different page. 
4. When login the web can lead user to different types of dashboard by adding a role determine, as the web only allow agronomists to register. staff require admin to add the system.

## Getting Started
- Please read requirment.txt to install.

## Design decision
- My main point of this web is
1. easy to use
2. match with agricultural theme
3. a message prompt will be returned for operation.
- Therefore, the main color is green and provide relate support tools for user eg, met service and information of weeds and pests. 

## Database design
- The database I have design that is put comonly value together, eg: agronomists, staff and admin they both need name, email, role and status. Therefore, I can put these value into one table and create tables based on different role or function. 

- user (stored account and details)
- agronomists (stored agronomists value)
- staff + admin (as they are requir same value therefore they could join one value)
- guide info (stored guide info only)
- image (stored image only)

+ agronomists and staff + admin references user as forgeigner key.
+ guide info as foreigner key to image.

## Demo
- AGRICULTURAL | BIOSECURITY | PEST AND WEED
- http://ritachen1126418.pythonanywhere.com/ 

