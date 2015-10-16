# Project 1, Part 3

Assigned:

Due: 

(worth 25% of overall Project 1 grade)


In this part of the project, you will complete the web application by building the front end
on top of the `Flask` Python webserver.  For those students doing Option 3.b, instructions are below.


* [Project overview](http://github.com/w4111/proj1)
* If your teammate has dropped the class, [see the contingency plan](http://github.com/w4111/proj1part1#contingency)
* For any questions about collaboration, [see the Syllabus](http://github.com/w4111/syllabus#cheating)
  * If there are questions of general interest, please post to piazza.


The following documentation may be helpful for you:

* [Java to Python Cheatsheet](https://github.com/w4111/syllabus/blob/master/java2python.MD)
* [Python tutorial](https://docs.python.org/2/tutorial/)
* [Learn Python The Hard Way](http://learnpythonthehardway.org/book/)
* [Flask documentation](flask.pocoo.org)
* [Flask Tutorial](http://flask.pocoo.org/docs/0.10/tutorial/)
* [Jinja Template documentation](http://jinja.pocoo.org/)
* [Jinja Tutorial](https://realpython.com/blog/python/primer-on-jinja-templating/)



# Option 3.a: The Web Application

Your job is to implement your proposed web application.  To help you out,
we have provided a bare-bones Flask web application in [./webserver/](./webserver/).
It provides code that connects to a database url, and a default index page.

Take a look at the comments in `server.py` to see how to use modify the server.
You will need to connect to your database used for part 2.

### Getting started and working with GitHub

* Fork this repository so you have your own copy of the repository that you can edit.
  You will submit a link to the repository.
* Clone it to your local machine (if you have Python installed and want to run locally) or your VM
* Edit your files
* Use the following commands to add and checkpoint (commit) your changes locally

        git add --help
        git add <new files to store in git>
        git commit -m "a sentence describing your changes" <the files you edited>

* When everything has been committed you can `push` all the committed changes so GitHub.com has a copy

        git push

* If you cloned the repository on another machine (say the VM), then you can download and apply those
  changes from GitHub.com

        git pull


        git clone git@github.com:w4111/proj1part3.git

Some notes

* Your life will be easier by setting up [SSH keys](https://help.github.com/articles/generating-ssh-keys/)
  and cloning the `git://....` versions of repositories.  That way GitHub won't keep asking for your password
  when running `git` commands
* Most errors you will encounter can be solved by [consulting](http://www.duckduckgo.com) a [search](http://www.google.com) [engine](http://www.bing.com)

### Running Locally

It often helps to program and test your application on your laptop or local computer, and
run it on the Azure VM when you are happy with the code.  

To run the webserver, go into the `webserver/` directory and run (make sure you have enabled the `virtualenv` environment)

        python server.py 

It should print something like:

        running on 0.0.0.0:8111
        * Running on http://0.0.0.0:8111/

The `0.0.0.0` listens to any IPv4 address on the machine.  The `8111` after the `:` is the port number.
So if this is running on your laptop, you can open you web browser to any of the following URLs

        http://0.0.0.0:8111
        http://127.0.0.1:8111
        http://localhost:8111


### Deployment


Once you are happy with your web application, you will deploy it to your Azure virtual machine:

1. [Open a port (e.g., 8000) on your VM so the world can access it](http://github.com/w4111/syllabus/blob/master/azure_port.pdf).  Remember the port number

1. Write down the url of your virtual machine.  It should be `<MACHINE NAME>.cloudapp.net`

1. Copy your code to the Azure virtual machine, as per instructions above or on GitHub's help pages.

1. Run the python server with the `0.0.0.0` as the host, and port from above.  Run with `--help` if you need help

        python server.py --help

1. Go to `<MACHINE NAME>.cloudapp.net:<YOUR PORT>` in your browser to check that it worked.  
   You will need this URL when presenting the project to your mentor.


### Submission

Fill out the [google submission form](http://goo.gl/forms/2TZOiBreHv)

  
On campus students will present to their project mentor between `11/11` and `11/18`.
The mentors will email you to schedule a 15 minute meeting by `11/4`.
Contact your mentor immediately if you have not been contacted by the end of `11/4`.

You will show off your project using the mentor's web browser:

1. Give your mentor the app's URL so they can run it in Chrome or Firefox -- make sure you tested in those browsers!
    * your grade will suffer _considerably_ if this step doesn't work

1. Your mentor will interact with your application and test the functionality described in Part 1

1. Your mentor may ask to look at your code, so have it available.  
   If the code is on GitHub, then it makes life _much_ easier.

1. The web interface doesn't need to be fancy, however users **should not need to type anything resembling SQL**.

1. Have a number of example interactions prepared ahead of time to show your mentor.  
   The more you impress your mentor, the better your grade is likely to be.


Grading

* Primarily how well your application matches the Part 1 submission, and how well you incorporated the mentor's feedback
* Your grade will not suffer depend on how _styled_ the user interface is (though it may mildly help)
* Your grade will suffer if it doesn't work, requires the user typing SQL, crashes or
  locks up on bad inputs, is vulnerable to the SQL injection described in lecture, and otherwise does
  not work as you described in part 1.


# Option 3.b: Extending The Design

Follow the expansion plans you described in [Part 1](http://github.com/w4111/proj1part1), namely:

1. Extend the ER diagram: more entity sets, more relationship sets, more constraints.  Same as part 1

1. Extend your SQL schema: translate your new ER diagram to SQL and create them in your database as in part 2.  Same deal.

1. Add tuples to your new tables, write 4 queries that use the tables in interesting ways ala 
   [part 2](http://github.com/w4111/proj1part2).


### Submission and Grading

Submission 

* Fill in the [google submission form](http://goo.gl/forms/Vhu6Hvlj4P)
* Submit your ER diagram and SQL schema print outs at the beginning of lecture.
* Your changes to the database should be accessible.

<!--
Follow the [same submission instructions as Part 2](http://github.com/w4111/proj1part2#submit) (this is a foreign reference!)
with the following differences:

* The folder should be named `<YOUR UNI>-proj1part3` (note it's part3 instead of part2)

* Submit to "Project 1, Part 3" on courseworks
-->


Grading will be same as [the grading criteria in Part 2](http://github.com/w4111/proj1part2#grading), 
but for your extended design instead of the original.

