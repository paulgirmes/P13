# <H1 align="center">Child Care Mini ERP</h1>

<img src="https://travis-ci.com/paulgirmes/P13.svg?token=J1YWZRU9c7XAUygKJUyG&branch=master" alt="build">

<h4 align="center">A WEB application that aims to facilitate child care facilities managers' and employee's daily life. Build with 
<a href="https://www.djangoproject.com/" target="_blank">Django</a>.</h4>

<h5 align="center">Project 13 of OpenClassrooms <a href="https://openclassrooms.com/fr/paths/68-developpeur-dapplication-python">Python developper certificate<h5></a>

## Demo

👉 Watch it deployed with Heroku <a href="https://child-care-erp.herokuapp.com/">here</a>.

### What is it ?!

Child Care  Mini ERP provides several functionalties :
* a single webpage for any user wich displays child care facility (thereafter ccf) basic informations and news created on the fly by the ccf manager.
* an access to daily facts reports of registered and authorized familly members' children.
* a utility to send daily facts reports mails to every registered and authorised family members via a cron task an manage.py command.
* a basic admin mode for ccf manager (basic indicators, CRUD of employee, child, news, employee messages, familly members...)
* an application for ccf non-manager employees that provides a way to register/change/read daily facts for ccf children and provides an access to emergency contacts for a children as well as an easy way to check for allowed familly memmbers names and pictures when handing off child.

### Using

* manager : login via the "connexion" link of the home page to have access to your admin index interface. You then have the possibility to create/change/delete all ccf related elements. If acting as an employee you still have access to the employee app via the "Transmissions-urgences" link.
when creating a parent please be carefull to the "Accès aux transmissions", "Autorisation de Prise en Charge" and "Contact en cas d'urgence" options as these define sensitive informations and permissions.
when creating an employee please be carefull to the "Direction" option if checked the employee will be allowed to access to the basic admin interface.

* employee : login via the "connexion" link of the home page to have access to your index interface. You can then consult the list of daily facts that you created or the list of ccf children where you can look at one child data/dailyfacys, note that you won't be allowed to delete any daily fact or to change a daily fact that you did not write.

* parents : login via the "connexion" link of the home page to have access to your index interface. You can then consult the list of your child and the list of daily facts written to date.

## For developers

* Clone the app directory

* Install Python3 on your computer if you are running a Windows environment.

* Install the dependencies with Pipenv from Pipfile

* this project works with a PostGreSQL engine so install it if deployed locally

* update settings.tests_production/and settings.test_settings with database credentials and STRUCTURE name

* execute manage.py makemigrations followed by manage.py migrate

* either run manage.py runserver for debug or deploy elewere as needed

* a Child_Care_Facility object must be created by a super-user via the advanced admin interface with a name matching settings.STRUCTURE for the app to work properly. The super user then must create a first set of credentials for a manager employee with the appropriate permissions (CRUD of all models except ChildCareFacility + is_staff=True).
* if you run the tests suite please specify settings=settings.test_settings

## Built with

* [Django](https://www.djangoproject.com/)
* [Bootstrap](https://github.com/maxogden/menubar)
* and a lot more ...!

## Credits

Images by 
* <a href="https://pixabay.com/users/192635-192635/?utm_source=link-attribution&amp;utm_medium=referral&amp;utm_campaign=image&amp;utm_content=317041">192635</a> from <a href="https://pixabay.com/?utm_source=link-attribution&amp;utm_medium=referral&amp;utm_campaign=image&amp;utm_content=317041">Pixabay</a>

* <a href="https://pixabay.com/users/picjumbo_com-2130229/?utm_source=link-attribution&amp;utm_medium=referral&amp;utm_campaign=image&amp;utm_content=865116">free stock photos from www.picjumbo.com</a> from <a href="https://pixabay.com/?utm_source=link-attribution&amp;utm_medium=referral&amp;utm_campaign=image&amp;utm_content=865116">Pixabay</a>

* <a href="https://pixabay.com/users/esudroff-627167/?utm_source=link-attribution&amp;utm_medium=referral&amp;utm_campaign=image&amp;utm_content=1399332">esudroff</a> from <a href="https://pixabay.com/?utm_source=link-attribution&amp;utm_medium=referral&amp;utm_campaign=image&amp;utm_content=1399332">Pixabay</a>

* <a href="https://pixabay.com/users/jarmoluk-143740/?utm_source=link-attribution&amp;utm_medium=referral&amp;utm_campaign=image&amp;utm_content=2847508">Michal Jarmoluk</a> from <a href="https://pixabay.com/?utm_source=link-attribution&amp;utm_medium=referral&amp;utm_campaign=image&amp;utm_content=2847508">Pixabay</a>

* <a href="https://pixabay.com/users/FeeLoona-694250/?utm_source=link-attribution&amp;utm_medium=referral&amp;utm_campaign=image&amp;utm_content=1864718">Esi Grünhagen</a> from <a href="https://pixabay.com/?utm_source=link-attribution&amp;utm_medium=referral&amp;utm_campaign=image&amp;utm_content=1864718">Pixabay</a>

* <a href="https://pixabay.com/users/Pezibear-526143/?utm_source=link-attribution&amp;utm_medium=referral&amp;utm_campaign=image&amp;utm_content=1357485">Pezibear</a> from <a href="https://pixabay.com/?utm_source=link-attribution&amp;utm_medium=referral&amp;utm_campaign=image&amp;utm_content=1357485">Pixabay</a>

* <a href="https://pixabay.com/users/jackmac34-483877/?utm_source=link-attribution&amp;utm_medium=referral&amp;utm_campaign=image&amp;utm_content=1256522">jacqueline macou</a> from <a href="https://pixabay.com/?utm_source=link-attribution&amp;utm_medium=referral&amp;utm_campaign=image&amp;utm_content=1256522">Pixabay</a>

Themes bases by :
<https://startbootstrap.com>

<h3>Many thanks to all contributors from the Python community.</h3>

## Author

**Paul Girmes** - *Initial work*

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details
