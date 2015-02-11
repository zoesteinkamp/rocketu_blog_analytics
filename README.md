# Intro to DevOps & Sysadmin

## What's DevOps?
DevOps stands for development operations. The general concept deals with the ability for developers producing software to collaborate with IT professionals in deploying that software.

Historically, development and IT work was very siloed. There was not much communication between the two groups. Developers would hand their work off to the IT department and they would be responsible to deploy this work that they didn't know much about.

In modern development, DevOps is often referred to when a small team has no dedicated sysadmin and it's the developer's responsibility to launch their own product. Usually this developer splits their role between being part-time developer and part-time sysadmin. The idea is that through a better process and with some programming, the workflow can be much more efficient.

Continuous Deployment is one way that development can exist more closely with operations. [Heroku](https://www.heroku.com/) is actually another solution to DevOps, but having the Ops part of the equation mostly outsourced.

In this repo we'll actually be learning sysadmin done manually as well as automated.

## Setup Project
First let's see how we could get a simple static site up and running first, before we graduate to a full Django project.

There's a sample "Coming Soon" portfolio site on github [here](https://github.com/rocketu/portfolio). Fork it, clone it, and edit it so that it's "Your" portfolio site. You could simply just swap in your name, change some of the text, or change the colors, it's up to you. Spend about 15 minutes to do that.

## AWS Setup
For the rest of the week we will be using Amazon's Web Services to learn how to deploy our websites ourselves and get an introduction to IT and DevOps work.

You'll need to create a AWS account to use for these exercises. Don't worry, there's a free usage tier valid for 12 months! The signup process does take some time and requires a verification phone call as well as putting in a credit card.

RocketSpace also has credits for AWS that you can make use of. After today's lesson, if you don't want to use up all of your free hours for the month, shut down your EC2 instances or you may be charged.

## First EC2 Instance
Let's set up our first virtual server on Amazon. AWS calls these EC2 (Elastic Compute Cloud) Instances.

1. Navigate to the EC2 Service and select Launch Instance
2. Select the Ubuntu 14.04 AMI (Amazon Machine Image)
3. Confirm you'd like the t2.micro instance type. This is the free tier type, but has the lowest hardware specs.
4. Click 5. Tag Instance from the top. For the Value field, name this "portfolio" so we can more easily tell what this EC2 instance is for in the future.
5. Click 6. Configure Security Group. We need to add a new rule and select HTTP. This will allow our EC2 instance to host a website and allow website traffic access to it.
6. Select the Launch option. We'll need to create a new key pair. Once it's created, make sure you click the Download Key Pair button. A pem file will download (we'll get back to this in a minute).
7. Select Launch Instances. Go back to your dashboard for EC2 and check that you now have a running EC2 instance.


## Connecting to EC2
If you're not already there, navigate to your running EC2 instance via the EC2 dashboard and the Running Instance link.

We need to find the public IP address of our EC2 instance in order to connect to it. Locate it in the bottom info panel.

Now that we know the IP address, we just need to set up our pem file, which we downloaded while we were setting up our EC2 instance. This file is our "key" that gets us into the server.

First, locate your pem file on your computer and move it to your user's .ssh folder for safe keeping. You can do this with a GUI or command line, up to you. On a mac, the command you likely can run is: <code>mv ~/Downloads/portfolio.pem ~/.ssh/</code> assuming you named your EC2 instance portfolio.

Now we need to change the permissions of the pem file so that we can use it. Change directory to your .ssh folder then run <code>chmod 400 portfolio.pem</code>. This allows our currently logged in user to read our pem file.

## SSHing
Now that we have the IP address of our EC2 instance and our pem file we can securely connect to our server. We can do this using SSH (Secure Shell). This is a protocal for connecting to a remote server.

Let's run <code>ssh -i portfolio.pem ubuntu@your-ip-address</code>. Make sure you use your IP address. This is telling ssh to connect to our server at our public ip address as the ubuntu user using our pem file. If we don't pass it the pem file, we won't be allowed in.

If it asks if you're sure you want to connect, say yes. It does this whenever you're sshing to a new IP address for the first time.

Now we're in our EC2 instance! And everything's ready for us to set up our website.

## apt-get
First thing we want to do is install nginx so that we can start setting up our web server, which will be responsible for receiving and returning our HTTP requests and responses.

Ubuntu uses a tool called apt-get to manage installing software. This works by keeping a large list of repositories where the software is stored. Over time, these repositories get updated as new versions of the software is released.

Before we can install nginx, we want to make sure Ubuntu has the most up to date apt-get repositories or we may install an older version of nginx or some other software. To do this we can run <code>sudo apt-get update</code>. Once that finishes we can run <code>sudo apt-get upgrade</code>, which will then upgrade all of our installed packages.

We're currently logged in as the user, <code>ubuntu</code>. Usually to run apt-get commands we need to have "root" permissions. By using <code>sudo</code> we're saying "SuperUser DO" this command.

Once Ubuntu finishes updating it's apt-get repositories, now we can install nginx. We can do this by running <code>sudo apt-get install nginx</code>. This should look fairly similar to when we're using pip with python packages. Ultimately apt-get and pip are both just different tools used for downloading software, one for Ubuntu, the other for python.

## Site Setup
The stage is set, let's get our portfolio site on our server and nginx serving it!

Let's get our portfolio site's code onto our EC2 instance. The easiest way to do this, is just to clone it onto our server. In the future, if we make an update to it, we can just pull it down via git.

This means we'll need to install git: <code>sudo apt-get install git</code>.

For our instance to have access to our github repository, it will need an authorized ssh key.

## Nginx Setup
Last, but not least, we need to set up our web server so that it knows about the new website code we just placed onto our server.

Nginx has it's own configuration file format, which we'll need to setup for our website. You can potentially have multiple websites running on the same server, by using multiple configuration files.

The configuration files all live in a specific folder, let's change directory to it so we can make our new one: <code>cd /etc/nginx/sites-enabled/</code>.

You'll notice there is already a <code>default</code> configuration file in here. Take a look at your dashboard again on EC2 for this running instance. Go to the public dns url listed in the info pane. You should see a Welcome to nginx! page. This is controlled by this <code>default</code> nginx config.

For us to get up and running as quick as possible, let's edit and use this config. Let's rename it to something more appropriate: <code>sudo mv default portfolio.conf</code>.

## Editing Nginx Conf
Since we're ssh'd into a remote server, we can't just open up this file in our favorite text editor. This means we have to use one of the universal text editors that is installed on most servers.

Our options are nano, vim, and emacs. If you are familiar with one of these, please use that one to start editing the file. If you're not, let's use emacs. The shortcut keys can be hard to learn, so let's walk through it step by step.

1. Let's install emacs: <code>sudo apt-get install emacs</code>
2. Next, let's open our file: <code>sudo emacs portfolio.conf</code>
3. All we need to do is edit the location of where the website files exist: <code>root /usr/share/nginx/html;</code> becomes <code>root /home/ubuntu/portfolio;</code>
4. To save in emacs we need to hit: cntrl-x then cntrl-s
5. To exit emacs we need to hit: cntrl-x then cntrl-c
6. Lastly, we need to restart nginx so our changes take affect: <code>sudo service nginx restart service</code> is a useful tool that helps give us some shortcut commands to start|stop|restart various tools on our server.

## Creating a New User
1. Create an ssh key: <code>ssh-keygen -t rsa</code>
2. Then copy and paste this key to the deploy key setting for our repository in github: <code>cat ~/.ssh/id_rsa.pub</code>, Settings -> Deploy keys
3. <code>cd ~/</code> to make sure we're back in our home folder and now let's clone our site: <code>git clone git@github.com:username/rocketu-portfolio.git</code>. Make sure you replace <code>username</code> with your github username and the proper link to your repo.


## Recap - So how is this working?
[Nginx](http://docs.python-guide.org/en/latest/scenarios/web/#web-servers) is the web server and responsible for receiving and sending messages to our user's browser.

Since this first example is only a static website and not using python, we do not need to worry about the WSGI layer of our architecture.

Our <code>index.html</code> is just a static file and nginx knows how to read the static file and send the contents to the browser. Essentially it turns our HTML into a string that gets sent in the data portion of the HTTP response.

We'll see that things get a bit more complicated once we need to set up a Django application. We'll also dive a bit more into the nginx configuration file.


## SSH Convenience
It may be annoying to have to constantly remember our IP addresses and pem files when sshing into our servers. It becomes especially annoy when you have many different ones you need to ssh into often.

On our computers we can edit a configuration file, which let's us give just a nickname so we could simply type ssh portfolio and our configuration file will do the rest of the work for us.

Let's set it up!

* Let's first create the file if it doesn't exist already: <code>touch ~/.ssh/config</code>.
* Since we're on our computer, let's open the file in our preferred text editor: <code>open ~/.ssh/config</code>.
* Add the follow lines of code, replacing the IP address with your EC2 instances public IP address.

````
Host portfolio
         HostName your_ec2_ip_address
         User ubuntu
         IdentityFile ~/.ssh/portfolio.pem
````
* This is simply just configuring the different parts of our normal ssh statement:
	<code>ssh -i ~/.ssh/portfolio.pem ubuntu@your_ec2_ip_address</code> ->
	<code>ssh -i IdentityFile User@HostName</code>
* Save the file and now try to <code>ssh portfolio</code>. Now you don't have to look up your IP address everytime!

## Mission: Part I
* Make a change to your portfolio site locally on your computer. Commit and push the changes back to github.
* SSH back into your server, pull down the changes and restart nginx.
* Confirm you see your new changes in the browser!

# Django SysAdmin

## Deploying Django Setup
<strong>From this point forward, we will be using the [rocketu_blog_analytics](https://github.com/rocketu/rocketu_blog_analytics) for deployment using Fabric and then Ansible</strong>. First, let's trace back through our steps and create a new EC2 instance for our Django application.

We're using a new EC2 instance for repetition in setting one up. Remember to shut down one or both of these instances when you're done with them.

Create a new key pair to have practice chmoding it, moving it, and sshing with it.

Once you've sshed back into your server, continue to follow the previous steps: update apt-get, install git, setup a deploy ssh key, clone it to /home/ubuntu, install nginx and install emacs.

Wait to set up your nginx config, this will be more complicated for our Django application!

## Building the Environment
Just like all of the steps involved in starting a new Django project, we will need to do many of the same things on our server. This includes creating a virtual environment, installing packages, setting up postgreSQL, and running migrations.

Let's tackle these one by one.

## Virtualenv
Let's start with setting up our virtualenv.

* We need to install apt-get's python libraries, which include pip: <code>sudo apt-get install python-pip python-dev build-essential</code>
* Then we need to upgrade pip, virtualenv, and install virtualenv wrapper: <code>sudo pip install pip --upgrade</code> , <code>sudo pip install virtualenv --upgrade</code>, <code>sudo pip install virtualenvwrapper</code>
* Now we need to setup the proper folder where our virtualenvs will save: <code>mkdir ~/.virtualenvs</code>
* Next let's edit our basrc to point to our folder and where we installed virtualenvwrapper:
<code>emacs ~/.bashrc</code>, then add <code>export WORKON_HOME=~/.virtualenvs</code> and <code>source "/usr/local/bin/virtualenvwrapper.sh"</code> to the bottom of the file.
* Reload our bashrc so the changes take affect: <code>source ~/.bashrc</code>
* Create our virtualenv that we'll be using: <code>mkvirtualenv blog_analytics</code>

## PostgreSQL
Next up, let's set up PostgreSQL on our server.

* First we need to add a new user account for our server: <code>sudo adduser blog_analytics</code>. When prompted set a secure password for this user. Remember it! You'll need it in the next step.
* We need to install the appropriate postgreSQL packages from apt-get: <code>sudo apt-get install postgresql postgresql-contrib libpq-dev</code>.
* Once those finish installing we can switch to the postgres user account, which has access to the database: <code>sudo -i -u postgres</code>.
* We want to create a new postgres user for our application: <code>createuser --interactive</code>. Name the user <code>blog_analytics</code> when prompted. We don't want to give the user any extra permissions so just say no to the questions.
* Now we can create the database for our user and Django application: <code>createdb blog_analytics</code>.
* Our user and db should be created, let's switch to that user. If you're still the postgres user, you'll need to type exit first, then <code>sudo -i -u blog_analytics</code>.
* Now just type <code>psql</code>, and you should connect to the database.
* Let's set up a password for our postgres user blog_analytics by running: <code>ALTER USER blog_analytics WITH PASSWORD 'myawesomepassword';</code>. Make sure you replace myawesomepassword with your secure password.

## Local Settings
Now that we have PostgreSQL and our virtualenv set up, now we can set up our local settings file and install our python dependencies.

* Let's make a copy of our local settings template: <code>cp local_settings.py.template local_settings.py</code>.
* Now let's edit the file using <code>emacs local_settings.py</code> and edit our file with some new information about our server,

````Python
import os
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'blog_analytics',
        'HOST': 'localhost',
        'USER': 'blog_analytics',
        'PASSWORD': 'myawesomepassword'
    }
}

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
STATIC_URL = '/static/'
````

## Packages
* Next we can install all of the packages in our requirements file: <code>pip install -r requirements.txt</code>.
* Make sure you have all of your packages listed in your requirements file!
* Run <code>python manage.py runserver</code> to test that we have everything working and can talk to the database.
* Note we have a warning in red saying we should apply our migrations, let's do that next! <code>python manage.py migrate</code>
* We also set up our static files directory in <code>local_settings.py</code>. Let's run <code>python manage.py collectstatic</code>, which will help set up our static files for later.

## Gunicorn, Supervisord, and Nginx Oh My!
We have now gone through all the familiar bits of getting our project working locally, except on Ubuntu. Next we need to get our Django application synced with nginx so we can actually receive and respond to web requests to our server.

Please follow along carefully. Any wrong character type or file misplaced in the wrong directory will lead to your setup not working.

Likely, you're also not very comfortable with the command line text editor yet as well as all of the terminology so even more reason to pay careful attention.

## Gunicorn
Gunicorn is a WSGI layer that we can use to allow our Django application to talk with nginx. Setting it up is very straightforward.

* First, let's install it in our virtualenv: <code>pip install gunicorn</code>.
* Next let's create our gunicorn config file: <code>touch rocketu_blog_analytics/gunicorn.conf.py</code>. Make sure it's in the root folder of our Django project.
* We'll need to open it in our text editor, <code>emacs rocketu_blog_analytics/gunicorn.conf.py</code>, and place the following code:

````Python
proc_name = "rocketu_blog_analytics"
bind = '127.0.0.1:8001'
loglevel = "error"
workers = 2
````

* There are a lot more configuration options then the ones we specified, but keeping it this simple for now works.
* <code>workers</code> specifies how many threads to use for gunicorn. This means we could handle 2 incoming requests at the same time. Usually you want to have a number of workers that corresponds to the number of CPU cores on your machine.
* <code>bind</code> refers to localhost and the port gunicorn is running on. If we had multiple Django applications on this EC2 instance we could bind the other to port 8001, we'd choose something else.

## Supervisor
Supervisor is a tool that basically helps manage other tools. The idea is that we can easily use supervisor to stop, start, and restart gunicorn quickly and reliable.

* As usual, let's install it first: <code>sudo apt-get install supervisor</code>.
* To get it started and check it was installed let's restart the supervisor service: <code>sudo service supervisor restart</code>.
* Supervisor also works by having a configuration file. Let's create one for our project: <code>sudo touch /etc/supervisor/conf.d/rocketu_blog_analytics.conf</code>. Note, it belongs inside supervisor's conf.d directory.
* Now let's open it up in our editor, <code>sudo emacs /etc/supervisor/conf.d/rocketu_blog_analytics.conf</code>, and add the following:

````
[group:rocketu_blog_analytics]
programs=gunicorn_rocketu_blog_analytics

[program:gunicorn_rocketu_blog_analytics]
command=/home/ubuntu/.virtualenvs/blog_analytics/bin/gunicorn -c gunicorn.conf.py -p gunicorn.pid wsgi:application --pythonpath /home/ubuntu/rocketu_blog_analytics/rocketu_blog_analytics
directory=/home/ubuntu/rocketu_blog_analytics
user=ubuntu
autostart=true
autorestart=true
redirect_stderr=true
````

* Let's restart supervisor to make sure it works: <code>sudo service supervisor restart</code>. This will run the gunicorn program we created in our supervisor config file.
* Notice that we set the command to run gunicorn for our project and target our <code>gunicorn.conf.py</code> configuration file we setup.
* We specifiy we want to use our ubuntu user to run the command and that it should be run from our Django project directory.

## Nginx
To put it all together, we now need to set up nginx to point to our Django project and the gunicorn wsgi server we just set up.

* This time we're going to make the nginx config file from scratch: <code>sudo touch /etc/nginx/sites-available/rocketu_blog_analytics.conf</code>.
* Let's open it up for editing: <code>sudo emacs /etc/nginx/sites-available/rocketu_blog_analytics.conf</code> and place in the following.

````
server {
    server_name your_ec2_url;

    access_log off;

    location /static/ {
        alias /home/ubuntu/static/;
    }

    location / {
        proxy_pass http://127.0.0.1:8001;
        proxy_set_header X-Forwarded-Host $server_name;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header Host $host;
    }
}
````

* Make sure you replace your ec2 public url in the nginx config.
* Notice we set up a special location for the static files. This helps us server our css, js, and images for our application.
* We also point the <code>proxy_pass</code> to 127.0.0.1:8001. This has to match what we configured gunicorn to run on.
* The rest of these headers are just informing nginx to pass on the appropriate information to gunicorn and subsequently Django.

* You may not have noticed, but we put the file in the <code>sites-available</code> folder this time, instead of <code>sites-enabled</code>. You're supposed to put all available nginx configs in the available folder, and then symlink the ones you want active to the enabled folder.
* Let's symlink our new nginx config file: <code>sudo ln -s /etc/nginx/sites-available/rocketu_blog_analytics.conf /etc/nginx/sites-enabled/rocketu_blog_analytics.conf</code>.
* Now let's also remove the old symlinked default file: <code>sudo rm /etc/nginx/sites-enabled/default</code>.
* Let's restart nginx <code>sudo service nginx restart</code>, and go to our browser!

## Cleanup
Our site's up! There's still some things left that we should do, before it's complete.

* Navigate to a url that you know doesn't exist. Oops, we're still in debug mode! Not good.
* Let's edit our local settings file, <code>emacs local_settings.py</code>, and add <code>DEBUG = False</code>
* We then need to restart supervisor: <code>sudo service supervisor restart</code>
* And we need to restart nginx: <code>sudo service nginx restart</code>
* Note, you'll need to do these everytime you change some python code. This recompiles our python code to .pyc files.
* Uh oh, we broke something!?

Something about our site does not work when we're not in DEBUG mode. This is something that will definitely happen to you again so pay attention!

* We need to set the <code>ALLOWED_HOSTS</code> setting to allow requests from our EC2 url.
* Edit our local settings file, <code>emacs local_settings.py</code>, and add the following: <code>ALLOWED_HOSTS = ['your_ec2_url']</code>. Note, you need to use your ec2 instance url!
* Again we need to restart supervisor: <code>sudo service supervisor restart</code>.
* And restart nginx: <code>sudo service nginx restart</code>.
* And our site works!
* Navigate around the site, and create a superuser to log into the admin to see your analytics.

# Automating Deployment
## Sysadmin Recap
Up to this point, we have seen what it takes to get a virtual server up and running with a web server and project on it.

Imagine if we were working with a large team of developers and we had to push new updates every day, maybe even multiple times a day.

Imagine if the website we were running actually received hundreds of thousands of users in traffic every day. We would need to have many servers running simultaneously.

Our entire job, every day, would just be sshing into servers and updating the code. Training someone else to also do our job or collaborating with a team of sysadmins would be a nightmare.

## Automating
On a team, when the realities of all the scenarios we just started talking about set it, sysadmins and developers start looking for tools we can use to help automate this process. After all, it is essentiall just a repeatable list of steps.

Today we're going to take a walk through those automation tools and see how we can abstract away the need to manually ssh into a server.

This is going to make deploying much better, but we wouldn't have the ability to put together these automation tools unless we had done it by hand before.

It's also going to give us some insight into what Heroku is probably doing, when we run specific commands to launch our application.

## Fabric
Our tool of choice this morning will be Fabric. This is a python library that gives us handy functions for running commands on remote servers. It also allows us to parallelize these commands, so that we could potentially update multiple servers at once.

Fabric also has the ability to assign roles to different servers. This means we can run certain commands on different servers we may have running in our system.

For today's purposes though, we'll just be worrying about writing some commands to automate tasks on our one server.

## I'm Alive!
Let's create our first Fabric task, which will just print out to the console to prove we have it working.

* Let's first install fabric so we can use it: <code>pip install fabric</code>
* Next, we'll need to make a new file in our blog analytics project called <code>fabfile.py</code>. Make this file in your root folder, the same that contains <code>manage.py</code>
* Let's define our first task, hello.

````Python
@task
def hello():
    print("I'm alive!")
````
* Note that we're using a decorator called <code>@task</code>. This comes from Fabric and we have to specify this on any function that we want to be able to call from the command line.
* Let's run our new task: <code>fab hello</code>. When we run a fabric command using fab, it looks for a file called <code>fabfile.py</code> or a directory called <code>fabfile</code> to import commands from.

We're now successfully ran a fabric command and had something print out to our console. We can run <code>fab -l</code> to see the list of all of our available commands at any given time.

Our message right now is trivial though. Let's spruce it up by adding some color. Change your print line to this: <code>print(green("I'm alive!"))</code>, then run your command again.

It's green! An important part of fabric scripts is making sure that appropriate output is being displayed to the user running the script. Using different colors can help signify successes, warnings, and failures.

## Local Commands
Now that we have our fabfile working, let's do something more than just printing. Fabric gives us a command, <code>local()</code>, which takes a command as a string and runs this locally on your computer.

Let's create a task, which will make an empty file on our Desktop as an example.

````Python
@task
def create_file():
    local("touch ~/Desktop/dummy_file.txt")
````

Please change the path to your Desktop as needed to work with your computer. Run this fab command and try it out: <code>fab create_file</code>. Check that the file was created on your Desktop.

We can do even better with our new task. Let's say we want the ability to specific the name of the file that our Fabric task should create. Our tasks can receive arguments just like normal functions and we can pass in these arguments to them when we call the command.

````Python
@task
def create_file(file_name):
    local("touch ~/Desktop/{}.txt".format(file_name))
````
All we did was add an argument to our function and then use it to edit our command to make a file with that name.

Let's run it and pass it a file name: <code>fab create_file:test_arguments</code>. This should create an empty <code>test_arguments.txt</code> file on your Desktop! All we did was pass the arguments after the command name, separated by a colon.

## Mission: Part II
Let's try to quickly write our own tasks to do something locally on our computer, to make sure we understand what's happening.

* Write a task to create a new directory called "my_directory" on your Desktop.
* Write a task that takes in two arguments, one is the name of the directory you should create and the other is the path to the folder you should make that directory in.

## Remote Commands
Okay, the real reason for using fabric is to be able to ssh into our server and run commands remotely. Let's see how we can easily do that.

At the top of our fabfile, we're going to need to set some global env variables so our script knows how to ssh into our server. The way this works is a bit "unpythonic", but we have no other choice.

````Python
from fabric.api import *

env.hosts = ['your_public_ip_address']
env.user = 'ubuntu'
env.key_filename = '~/.ssh/your_pem_file.pem'
````

As usual, remember to substitute the appropriate public IP address and name of your pem file in your local version of the fabfile.

Now let's write a simple task, which will run a remote command on our server. Fabric's <code>run</code> method can be used to accomplish this.

````Python
@task
def ubuntu_hello():
    run("lsb_release -a")
````

<code>lsb_release -a</code> is a command that has Ubuntu print out version info about itself. This will prove that we actually made it onto our server. All we did was pass the command we wanted to run, as a string to <code>run</code>.

** Run our new command using <code>fab ubuntu_hello</code>, and test that it works.

If you look at the output of our command, the info we get from <code>lsb_release -a</code> is a bit hidden with the rest of the fab output.

By default, the stdout and stderror of our commands on our server is just printed out to our console locally.

We can change this by choosing not to show the output of the command and instead storing it in a variable. We can then color and print the output so that it stands out more. This is a common way to make important output standout in a script.

````Python
@task
def ubuntu_hello():
    with hide("stdout"):
        output = run("lsb_release -a")
        print(yellow(output))
````

Run the command again, to see the change in the output.

Here, we've used the context manager <code>hide</code> to suppress and output to stdout that happens inside of it's code block. Then as we mentioned, we save the output of <code>run</code> to a variable so we can print and style it as we see fit.

## Scripting Our Deployment
We've played with a few of the basics of Fabric, let's see how this would really apply to us in DevOps.

A common task is to update our existing Django project on our server. That process has the following steps:

* Pull the latest from git
* pip install our requirements file in case there was a new library added
* Run migrations in case there have been any schema changes.
* Run collectstatic to get any new static files
* Restart supervisor
* Restart nginx
We've got our list of remote commands that need to be run. Let's set up a Fabric task, which sequentially executes this list.

## First Steps
Let's work on pull the latest from github first. In order to do this, we'll need to be in the proper directory that our Django project lives in. This is easy enough with the cd context manager that fabric defines for us.

````Python
@task
def deploy():
    with cd("/home/ubuntu/rocketu_blog_analytics"):
        run("git pull origin master")
````
What this is doing, is running any command inside of the context manager inside of the <code>rocketu_blog_analytics</code> folder. This will effectively run <code>cd /home/ubuntu/rocketu_blog_analytics</code> then run <code>git pull origin master</code>.

Try it out!

## Virtualenvs
Next on our list is installing any changes from our requirements file. The command part is easy enough, but the trick here is that we need to be inside of our virtualenv when we run this command.

Again, fabric has another context manager called <code>prefix</code> that we can use so that we can run <code>workon blog_analytics</code>, before we use <code>pip</code>.

````Python
@task
def deploy():
    with prefix("workon blog_analytics"):
        with cd("/home/ubuntu/rocketu_blog_analytics"):
            run("git pull origin master")
            run("pip install -r requirements.txt")
````

Trying running this, it still won't work. This is because we're using virtualenvwrapper, which requires that our <code>.bashrc</code> file is loaded. To do this, we need to add a line to the top of our file: <code>env.shell = "/bin/bash -l -i -c"</code>

This line, specifically the <code>-i</code> flag, informs our remote commands that it should be source any bash profiles that exist for our user.

## Mission: Part III
There's 4 commands left you need to automate. We now have all of the context managers set up properly to be inside of the proper virtualenv and in the right folder to run them all.

Try to implement the rest yourself. Hint: You need to use sudo to restart supervisor and nginx. Check out the fabric documentation for it if you need help.

* Run migrations in case there have been any schema changes.
* Run collectstatic to get any new static files
* Restart supervisor
* Restart nginx

## Reusable Pieces
Since our examples this morning our so small, we can't see the immediate benefit, but splitting up our fabfile methods into small reusable chunks will be great for saving time later.

In this exercise we could split out restarting supervisor and nginx into it's own method called <code>restart_app</code>.

````Python
def restart_app():
    sudo("service supervisor restart")
    sudo("service nginx restart")
````

Note that I don't have to use the @task decorator, since this isn't a stand alone task I want to call via <code>fab restart_app</code>. It is just a helper method that will be called by the other methods.

## PostgreSQL
Let's take a look at another example that's completed already.

````Python
@task
def setup_postgres(database_name, password):
    sudo("adduser {}".format(database_name))
    sudo("apt-get install postgresql postgresql-contrib libpq-dev")

    with settings(sudo_user='postgres'):
        sudo("createuser {}".format(database_name))
        sudo("createdb {}".format(database_name))
        alter_user_statement = "ALTER USER {} WITH PASSWORD '{}';".format(database_name, password)
        sudo('psql -c "{}"'.format(alter_user_statement))
````

This fabric task helps automate setting up the different moving parts of a PostgreSQL database for our Django application.

Step by step, this runs the list of necessary commands that were run earlier. It also takes in variables, so we could optionally configure this for any database name and password.

There is one new bit of functionality introduced here, which is the <code>settings</code> context manager. This specifies that any command ran inside this code block uses the <code>postgres</code> user.

## Templates
Fabric also comes with some built-in methods for manipulating files. Specifically we're going to take a look at <code>upload_template</code>, which will help us set up files on our remote server, like our nginx configuration file.

As the name suggests, they are templates, and like Django templates they have some basic functionality to replace variables in them with a dictionary of data we pass to it.

Let's check out how we would upload our nginx configuration file.

We'll create a deploy folder in our Django project. It is best practice to designate a folder where you will keep these configuration templates.
Inside this folder, let's create an empty file called <code>nginx.conf</code>. In here, we want to put our basic nginx configuration file.

Below are the contents of the <code>nginx.conf</code> file.
````
server {
    server_name %(server_name)s;

    access_log off;

    location /static/ {
        alias /home/ubuntu/static/;
    }

    location / {
        proxy_pass http://127.0.0.1:8001;
        proxy_set_header X-Forwarded-Host $server_name;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header Host $host;
    }
}
````

Note that we've set up a variable for our server name. In a real life deployment scenario, we may want to use this script to not only deploy to production, but possibly to a staging or development server as well. By setting our fabfile up to work with variables, we're giving ourselves flexibility to deploy to different environments.

## Upload Template
Now let's actually upload this template to our server.

````Python
@task
def setup_nginx(project_name, server_name):
    upload_template("./deploy/nginx.conf",
                    "/etc/nginx/sites-enabled/{}.conf".format(project_name),
                    {'server_name': server_name},
                    use_sudo=True,
                    backup=False)

    restart_app()
````

Here we've specified:

* the local path to the configuration file to be uploaded
* the remote path on the server to where it should be uploaded to
* a dictionary of data to be used to replace variables in the template
* that we should use sudo
* that we do not want to make a backup
Run it! <code>fab setup_nginx:rocketu_blog_analytics,your_ec2_url</code>

## Mission: Part IV
Let's wrap up our lesson on fabric with trying to implement the gunicorn and supervisor conf files we set up yesterday.

* Create the appropriate conf files in your deploy folder. Make them project agnostic, so that <code>rocketu_blog_analytics</code> or <code>blog_analytics</code> does not show up anywhere in them.
* Create a new task, which will upload those templates, insert the appropriate variables, and place them in the right directory on our server.
* Make sure you use our helper method, <code>restart_app</code>, to restart supervisor and nginx after you're finished uploading the templates.

## Further Learning:
Obviously we have just scratched the surface of what a large fabric deployment script would look like. Mezzanine, an open source Django blog project, has a built-in fabfile, which is very comprehensive and a good place to see [examples](https://github.com/stephenmcd/mezzanine/blob/master/mezzanine/project_template/fabfile.py).

Here are some learned lessons from using Fabric to keep in mind if you find yourself at one point needed to automate your deployment process:

* Try to keep your fabfile's methods in small reusable chunks.
* Splitting your <code>fabfile.py</code> out into a <code>fabfile</code> directory with multiple files can make it easier to read and maintain.
* First manually attempt whatever you're trying to automate and take careful notes of each step. This will save you both time and headaches.
* Find a good way to reliable test your script is working. Rerunning the whole script from the beginning every time you make a small change can be a nightmare.

# Configuration Management
As we saw earlier, Fabric is great for automating our deployment process by scripting it in python. In practice, this works great at first and for small teams, this can perfect.

As the complexity and size of your system grows as well as the number of people who need to work and interact with your fabfile issues start to come up. The fabfile can quickly become a burdensome application to maintain and is hard to keep clean and organized. It is usually hard for anyone outside of the core maintainers to understand how it operates.

This is where Ansible comes in. Ansible is a Configuration Management and Deployment Automation tool, which at the core does a lot of the same things our fabfile does, but makes it easier to configure, read, and understand for the developer.

Popular competitors to Ansible are Chef, Puppet, and Salt Stack. Chef & Puppet have been around for much longer and are considered more mature options, but both are written in Ruby and have a very difficult learning curve. Ansible and Salt Stack are newer and are both implemented in python.

We've chosen to go with Ansible, but there is still not a clear favorite yet between Ansible and Salt Stack. They both have their pros and cons. Read more about the debate [here](http://jensrantil.github.io/salt-vs-ansible.html).

## Ansible
Ansible is an open source technology that has thousands of contributors, with all of the code up on github. The open source project is backed by a company called Ansible Works, which is/was a startup that has investors.

Ansible Works has a few paid for services that enhance their open source project. A major one being consulting on how to implement Ansible in the enterprise and another product called Ansible Tower. Ansible Tower let's you manage your hundreds of servers from a GUI and let's you run your "playbooks" from a web application.

We'll get into what a playbook is shortly.

## Ansible Vocabulary
Every configuration management tool has it's own list of vocabulary for what it calls it's moving pieces. Let's have a quick rundown up front.

* Playbook - Each playbook is made up of multiple plays, which say for each server what list of commands should be run on that server.
* Inventory - Your inventory is a list of all of your different servers in your system and what roles each of them have.
* Role - A role defines a set of functionality your server should have. For example your server may be an application server, a database server, or could be both.
* Variables - Variables help define information that we may want to change. This could make it so that our Playbooks our reusable among different projects or so we can define a list of variables for our production server and a slightly different list for our staging server.

Ansible uses yaml as it's configuration language of choice. Yaml is a good choice since it is meant to be very human readable, which is necessary when the nature of what you're configuring can be very complicated.

## First Ansible Playbook
At this point we've probably figured out the sports analogy that Ansible is trying to make use of. Let's make our first Playbook and get our first Ansible play running.

* The first thing we need to do is install Ansible. Since it is written in python, we can just install it from pip! <code>pip install ansible</code>.
* Next we want to create our Playbook. Create a file called <code>production.yml</code> in our deploy folder.
* At first, we want to put the following code in that file:

````YAML
---

- name: Provision a RocketU Blog Analytics server
  hosts: all
  sudo: yes
  sudo_user: root
````

* To keep it simple, we're going to use one Play, which is in charge of setting up one server with our Django project. We give it a name, specify that it should use all of our servers (which will just be 1), and it can use sudo as root.

## First Ansible Role
In order to start listing out commands for our Play to do, we need to create our first role. Best practices is to have a <code>base</code> role, which we give to every server.

* Let's create a folder called <code>roles</code> in our <code>deploy</code> folder.
* Then let's make another folder called <code>base</code> inside of our <code>roles</code> folder.
* Role's come with their own list of vocabulary:
* Task - This is a single command to run on the server.
* Handlers - These are commonly reused tasks, such as restarting nginx.
* Templates - Like we saw with fabric, we can have jinja templates that we can upload to our server.
* Variables - These are variables that we set for this specific role.

Each one of these can have it's own folder inside of the role. Let's make a folder called <code>tasks</code> inside of base.
And finally, let's make another empty file inside of tasks called <code>main.yml</code>.

## First Ansible Task
Okay! We've got all of the pieces set up to write our first task. Our goal with Ansible is to create a Playbook that will set up a new EC2 instance from scratch for our website as well as be re-runable so that it will update our instance with our latest code, migrations, requirements, etc.

So for our first task, let's automate the first step, which is to update and upgrade apt-get.

In <code>main.yml</code> in our <code>base</code> role, let's put the following:

````yaml
---

- name: Update and upgrade apt-get
  apt: update_cache=yes upgrade=yes
````

We declare the name of our task, then we use the Ansible apt module and specify that we want to update and upgrade.

Ansible comes with lots of core modules built-in. There is also a large community that creates 3rd party modules you can use as well for all common types of tasks you'd like to run.

## Register Ansible Role
Now that we created our role and our first task, we need to register our role with our play in our playbook:

````yaml
- name: Provision a RocketU Blog Analytics server
  hosts: all
  sudo: yes
  sudo_user: root
  roles:
    - base
````

This tells our Play to run all of the tasks in the <code>base</code> role.

## Running Our First Ansible Playbook
Let's checkout the command which will run our first task, in our first play, of our first playbook.

<code>ansible-playbook -i server_public_ip, --private-key ~/.ssh/blog-analytics.pem -u ubuntu -v deploy/production.yml</code>

This is long, so let's break it down into it's parts:

* ansible-playbook - this is the ansible command that is available after we installed it
* -i your_public_ip - this is specifying our inventory, which is just our one server
* --private-key - this points to our identityfile we need to use to ssh to our server
* -u ubuntu - we need to ssh in as ubuntu
* -v deploy/production.yml - finally, we specify the playbook that we want to run
Run it!

## Ansible {{ items }}
Ansible has some fairly subtle, but powerful features in the way you can define tasks and variables. Next let's automate the apt-get installing of our different packages we'd like to use on every server.

We'll make a new task in <code>main.yml</code> for our base role. This will just go sequentially, below the last task we
just made.

````yaml
- name: Install base packages
  apt: name={{ item }}- name: Ensure the PostgreSQL service is running
  service: name=postgresql state=started enabled=yes state=installed
  with_items:
    - nginx
    - emacs
    - git
    - python-pip
    - python-dev
    - build-essential
    - supervisor
  tags: packages
````
This task will actually get run for every item in the with_items list, meaning
<code>apt-get install {{ item }}</code>

will be called with every item.

Let's run our playbook again and see that our packages get installed.

## Pip Setup
Following along with our setup slides, next we want to install the latest version of pip. Again this is a new task in our role's yaml file.

````yaml
- name: Latest version of pip
  pip: name=pip state=latest
  tags: packages
````

Note that we're specifying that we want the latest version of pip and we're using the pip module, which is the equivalent of running <code>pip install</code>.

Again, run your playbook and verify it worked.

## Mission: Part V
Lastly to finish our base role's task list, we need to install the latest version of virtualenv. Try this out on your own! It should look awfully similar to the last task we just created.

## PostgreSQL
Next up, we're going to create the <code>db</code> role, which will handle installing PostgreSQL, creating the proper user, and the correct database.

Let's create the appropriate files and folders for our new role. This means a db folder on roles, a tasks folder under db and a main yaml file in the tasks folder.

Our first task, will be to install all of the necessary packages for PostgreSQL:

````yaml
---

- name: Install PostgreSQL
  apt: name={{ item }} update_cache=yes state=installed
  with_items:
    - postgresql
    - postgresql-contrib
    - libpq-dev
    - python-psycopg2
  tags: packages
````

Place this in our new <code>main.yml</code> tasks file. We need to install psycopg2 globally in order for Ansible's following postgreSQL modules to work.

We also need to register our new db role in <code>production.yml</code> by just adding <code>- db</code> under roles.

## Restart PostgreSQL
Now that we've installed postgresql, we want to make sure it's running:

````yaml
- name: Ensure the PostgreSQL service is running
  service: name=postgresql state=started enabled=yes
````

This task simply runs <code>service postgresql restart</code>

Let's run our script and make sure we have installed and started postgres properly.

## Create DB
Now that we have postgresql installed, we can create the database. Again, Ansible has a handy, postgresql_db module we can use to accomplish this:

````yaml
- name: Ensure database is created
  sudo_user: postgres
  postgresql_db: name={{ db_name }}
                 encoding='UTF-8'
                 lc_collate='en_US.UTF-8'
                 lc_ctype='en_US.UTF-8'
                 template='template0'
                 state=present
````

But this time, we'd like to make the name of the database configurable. We're going to need this name later to put in <code>local_settings.py</code>.

## Setting Up Vars
Now it's time to set up some variables. We want to make a new folder in our <code>deploy</code> folder called env_vars. Inside this folder, let's make a file called <code>production.yml</code>. Here we can configure variables for our production environment. Put the following inside of it:

````yaml
---

db_name: "blog_analytics"
````

We then need to tell our play in our playbook, that we want to use this variables file. This snippet of code can be defined right after our <code>roles</code> section.

Now run our playbook. We should now have postgresql set up with a new database for our application to use.

## PostgreSQL User
Lastly, we need to make sure our postgresql user is created with the proper name and password. This will again require a few more variables that we'd like to setup.

** db/tasks/main.yml
````yaml
- name: Ensure user has access to the database
  sudo_user: postgres
  postgresql_user: db={{ db_name }}
                   name={{ db_user }}
                   password={{ db_password }}
                   priv=ALL
                   state=present
````

** env_vars/production.yml
````yaml
db_user: "blog_analytics"
db_password: myawesomepassword
````

Let's run our playbook again. We should have postgresql entirely ready for our Django project.

## Web
Let's define our last role, web, by creating all of the appropriate files and folders. <code>roles -> web -> tasks -> main.yml</code>

We then need to make sure we register our role in <code>production.yml</code>

Our web role is where the meat of our Ansible script is going to take place so instead of place all of our tasks in <code>main.yml</code>, we're going to instead split them out into separate files.

Let's create a new file in our tasks folder called <code>setup_virtualenv.yml</code>. In our <code>main.yml</code>, let's put the following, which will include this new file:

````yaml
---

- include: setup_virtualenv.yml
````

## Virtualenv
In <code>setup_virtualenv.yml</code>, we only need to write one task. We don't have access to virtualenvwrapper, so we'll use the command for reguar virtualenv.

````yaml
---

- name: Create the virtualenv
  command: virtualenv {{ virtualenv_path }} --no-site-packages
           creates={{ virtualenv_path }}/bin/activate
````

Note the <code>creates</code> part of this command. If we run this script multiple times, Ansible will not try to create this virtualenv again if that file and folders already exist.

You'll notice we also used another variable here, since we're going to want to refer to the location of the virtualenv often and have that be configurable.

In our <code>web</code> role let's create a new folder <code>vars</code> with it's on <code>main.yml</code>. Inside of it, let's define this variable:

````yaml
---

virtualenv_path: "/home/ubuntu/.virtualenvs/blog_analytics"
````

## Mission: Part VI
Next we want to clone our github repository onto our server. We'll want to create a new file at <code>tasks/setup_git_repo.yml</code> and put - include: <code>setup_git_repo.yml</code> in <code>tasks/main.yml</code>.

We will want to define three new variables in <code>vars/main.yml</code>:

````yaml
git_repo: https://github.com/rocketu/rocketu_blog_analytics.git
project_name: rocketu_blog_analytics
project_path: "/home/ubuntu/{{ project_name }}"
````

We will need to use <code>git_repo</code> and <code>project_path</code> in our task. Read Ansible's [documentation](http://docs.ansible.com/git_module.html) on the git module and try to implement the task yourself!

## Git Repo Ownership
After we've pulled down the repo from git we need to ensure that our ubuntu user owns the repository folder.

Potentially, if we used sudo, the root user will own the folder and will cause hiccups with running our application later.

Let's put the following task in our <code>tasks/setup_git_repo.yml</code>:

````yaml
- name: Ensure user owns our project
  file: state=directory path={{ project_path }} owner=ubuntu
````

## Django App Setup
Now that we have our code cloned to our server we can start installing our packages and running our migrations.

Let's create a new file for our Django app setup tasks: <code>tasks/setup_django_app.yml</code> and include it:
<code>-include: setup_django_app.yml</code>.

The first thing we're going to do is create our <code>local_settings.py</code> file by using Ansible's templates. Just like Fabric and Django, Ansible is using a templating library, Jinja2, to help make it easy to upload files to our server and replace variables as needed.

## Local Settings Template
Our local settings template task will look like this:

````yaml
---

- name: Create the local settings file
  template: src=local_settings.j2
            dest={{ project_path }}/local_settings.py
            owner=ubuntu
            group=ubuntu
            mode=0755
````

We're using Ansible's template module and we're specifying where the template exists locally and where its destination is on our server. We need to make a new folder <code>web/templates</code> with the file <code>local_settings.j2</code> in it.

Our local settings template should have the following in it:

````yaml
import os
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': '{{ db_name }}',
        'HOST': 'localhost',
        'USER': '{{ db_user }}',
        'PASSWORD': '{{ db_password }}'
    }
}

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
STATIC_URL = '/static/'

DEBUG = False
ALLOWED_HOSTS = ['{{ nginx_server_name }}']
````

Ansible will replace all of these variables, with what we have set already. We have one new one that we need to define in <code>env_vars/production.yml</code>: <code>nginx_server_name: "your_ec2_url"</code>.

Run it! Check that your local settings file looks correct on your server.

## Requirements
Next we need to install our requirements file. This task is fairly straightforward. We should put the following in <code>setup_django_app.yml</code>

````yaml
- name: Install packages required by the Django app inside virtualenv
  pip: virtualenv={{ virtualenv_path }} requirements={{ requirements_file }}
````

We do have one new variable we want to keep track of here, which is the location of our requirements file. In <code>web/vars/main.yml</code> let's define that:
<code>requirements_file: "{{ project_path }}/requirements.txt"</code>

## Manage.py Commands
Lastly, we need to run our migrations and collectstatic. First let's migrate our application. We'll use Ansible's django_manage module, which knows about Django's manage.py commands.

````yaml
- name: Run Django migrations
  django_manage:
    command: migrate
    app_path: '{{ project_path }}'
    virtualenv: '{{ virtualenv_path }}'
    settings: '{{ django_settings_file }}'
  tags: django
````

Put this code in <code>setup_django_app.yml</code>. Again, we see one new variable we need to define. The django_manage module needs to know where to find our Django setting file.

Let's define this in <code>env_vars/production.yml</code>: <code>django_settings_file: rocketu_blog_analytics.settings</code>. In the future, if we wanted to use a different settings file per deployment environment, we could now do that easily by changing this setting.

## Mission: Part VII
Following the same template, write the last task, which will collectstatic. Check out the Ansible [documentation](http://docs.ansible.com/django_manage_module.html) on the django_manage module.

## Supervisor
Finally, we're on to configuring our WSGI and web server then we're done!

Let's create a new file for our supervisor setup tasks: <code>tasks/setup_supervisor.yml</code> and include it: <code>- include: setup_supervisor.yml</code>.

First, we need to make sure we've installed gunicorn, so here's our first task, which should look familiar:

````yaml
- name: Ensure gunicorn is installed
  pip: virtualenv={{ virtualenv_path }} name=gunicorn
````

## Gunicorn Config
Next we need to create our gunicorn config file. We'll use Ansible's template module again and create one that looks like what we manually created yesterday.

Put the following in <code>templates/gunicorn.conf.j2</code>

````
proc_name = "rocketu_blog_analytics"
bind = '127.0.0.1:8001'
loglevel = "error"
workers = 2
````

And here's our task to copy that file over to our server:

````yaml
- name: Create the Gunicorn conf file
  template: src=gunicorn.conf.j2
            dest={{ project_path }}/gunicorn.conf.py
            owner=ubuntu
            group=ubuntu
            mode=0755
````

## Mission: Part VIII
Now we need to do the same thing for our supervisor config file. Look [above](https://github.com/rocketu-missioncontrol/intro-devops#gunicorn) and emulate the template process we just did for the gunicorn conf file.

You'll need to make use of two variables in your template:
<code>{{ virtualenv_path }}</code> and <code>{{ project_path }}</code>.

## Reload
Lastly, we need to have supervisor reload our new config files when it's done and then restart supervisor. Put these final tasks in our <code>setup_supervisor.yml</code> taks file.

````yaml
- name: Restart Supervisor
  supervisorctl: name={{ project_name }} state=restarted

- name: Restart Supervisor Service
  service: name=supervisor state=restarted sleep=1
````

Note we <code>sleep</code> supervisor for 1 second. This is because sometimes the task can erroneously fail because supervisor can take a little while to restart.

## Nginx
And lastly, we need to set up our web server then our website should be up!

Let's create a new file for our nginx setup tasks: tasks/setup_nginx.yml and include it: - include: setup_nginx.yml.

The first task we'll implement is uploading our nginx config. Again, we'll use Ansible's template module to help us do this. Put the following as the first task in our file:

````yaml
---

- name: Create the Nginx configuration file
  template: src=nginx_site_config.j2
            dest=/etc/nginx/sites-available/{{ project_name }}
  notify: reload nginx
````

Notice we have a new command here called <code>notify</code>. This is the last new Ansible concept we'll be introduced to.

## Notify
At the beginning of this section we mentioned handlers are reusable tasks that we may want to call more than once, specifically after another task has been run. Reloading nginx's config files is a good example of this.

Let's create a new folder and file <code>web/handlers/main.yml</code> and put the following handler in it:

````yaml
---

- name: reload nginx
  service: name=nginx state=reloaded
````

## Nginx Config
Now we need to just define the nginx config template file. Create the template file in <code>web/templates/nginx_site_config.j2</code>. Put the following template in our new file.

````
server {
    server_name {{ nginx_server_name }};

    access_log off;

    location /static/ {
        alias /home/ubuntu/static/;
    }

    location / {
        proxy_pass http://127.0.0.1:8001;
        proxy_set_header X-Forwarded-Host $server_name;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header Host $host;
    }
}
````

We already have defined <code>nginx_server_name</code>. This would allow us to easily in the future change what the URL is for our application and have it update both in our nginx config and in <code>ALLOWED_HOSTS</code> when we redeploy.

## Enable/Disable Configs
Next we want to make sure we disable the default nginx config and enable ours, by deleteing and creating symlinks. Here are the two tasks that we should put into <code>setup_nginx.yml</code>:

````yaml
- name: Ensure that the default site is disabled
  command: rm /etc/nginx/sites-enabled/default
           removes=/etc/nginx/sites-enabled/default
  notify: reload nginx

- name: Ensure that the application site is enabled
  command: ln -s /etc/nginx/sites-available/{{ project_name }}
           /etc/nginx/sites-enabled/{{ project_name }}
           creates=/etc/nginx/sites-enabled/{{ project_name }}
  notify: reload nginx
````

These should match up with the commands from the slides from yesterday.

Lastly, we need to make sure that nginx is actually running, so we'll put in one last task:

````yaml
- name: Ensure Nginx service is started
  service: name=nginx state=started enabled=yes
````

## Run It!
Run it! Then try to go to your URL in your browser. If we set up our script right, we should see our blog analytics application running in the browser.

Unfortunately when writing an Ansible script it is often hard and tedious to test every single change. There are also no great testing tools available and writing unit tests for DevOps tools is generally a hard thing to do.

Soon we'll see how other services abstract the entire process away. Still, it's important to have context for what's going on behind the scenes.