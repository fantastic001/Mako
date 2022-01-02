
Mako
==============

Tool for making weekly schedules, organizing projects and measuring progress in achieving goals. 


# Installation 

In order to install Mako run the following:

    pip install MakoTool

and to check if it works, run:

    mako help 

If you get ImportError, try installing dependencies manually:

    pip install YAPyOrg ArgumentStack dropbox colorama termcolor odspy lxml easy-widgets urwid

# Introduction 


Mako is a tool for keeping track of your tasks, To-Do lists, weekly schedules. It can also measure various things such that
you are able to keep track of progress on projects and it can generate monthly and quarterly reports of how your time is spent. 

# Basic usage


When you install Mako you are able to use it without any initialization part and configuration. So let's explain basic 
infrastructure how database is organized. 

Set of tasks is divided into projects where every project has its subprojects. For example, you can have university project and 
then subproject for every course you are attending on the university. So, in university project, you can have algebra subproject 
and every task related to algebra on the university can be placed here. So let's create our first project:

	mako projects add university

so now when you list your projects, it will show that you have one project:

	~ mako projects 
	Projects:
	_________________
	university
	~ 

Now it's time to add some subprojects to our university project:

	mako project university subprojects add algebra

now we can list subprojects of university project:

	mako project university subprojects 

When we have project and its subprojects we can add individual tasks to them:

	mako project university subproject algebra tasks add "Read chapter 1" 2017-08-21 2

First argument to task add option is description of the task, second is due date and third is estimated time to complete given task. This is important since Mako will calculate how much time you are spending on tasks and how this time relates to your expectations. 

Now we can list tasks:

	mako project university subproject algebra tasks

to increase spent time on a task, do the following:

	mako project university subproject algebra task 1 do 2

first you specify task index given by task list and after "do" you specify how much time did you spend doing particular task, this will increase spent time on a task every time you run "do" command. 

To mark task as done:

	mako project university subproject algebra task 1 done 

Now, when you list tasks, you will see that our task is green instead of red which means it is marked as done. 


# Getting help


Since one blog post is not enough to explain whole functionality and since I explained just a little bit of this tool, I suggest to run:

	mako help

to see what you can use. 


# Schedules


For schedules to work, you will have to create needed projects and subprojects inside them. Schedule is basically your weekly
plan of what to do during next week. To create new schedule, just run:

	mako schedule new 

to show lastly created schedule, just run:

	mako schedule

Now you will see that our schedule is empty, to add entry in schedule you can run the following command:

	mako schedule add 1 15 2 myproject mysubproject

First number represents day in a week (1=Monday, 7=Sunday), second number represents starting time of task (15h or 3PM) and 
last number represents task duration - how long you plan doing this activity. Then you have to specify project and subproject. 

Now you can keep making your schedule. When week ends and you want new schedule, just run `mako schedule new` and you'll get new empty schedule. If you've made mistake during data entry into schedule, you can delete entries:

	mako schedule remove 1 15 2 

First you specify day, then starting point and then how many hours to clear. In this way, you can remove multiple entries for 
different projects. 

You can see that we do not specify tasks in schedule entries, just project and subproject. This is because Mako will 
give us ability to see what tasks we need to do today, it will look into schedule, see what projects and subprojects are scheduled, see undone tasks for each of them, sort them by urgency and print them such that it respects the time we have given in schedule. 
To use this functionality, just run:

	mako today

and you'll get list of tasks for today. Mako won't increase spent time for tasks so you need to do it manually:

	mako project myproject subproject mysubproject task "task description" do <NUM HOURS> 


# Schedule conditions

Schedule conditions is list of conditions to be satisfied for schedule to be correct. These conditions we can specify ourselves.
For example, we can add condition to forbid adding entries on Sunday (so we can rest of work) or not to add specific project 
during some time period or to some project has to be in some time period (for example, work hours or university or important meetings).

Every condition is one JSON file in `~/.mako/db/Schedule conditions/` (or different path if you specify different database path, this is default). Every JSON file is JSON-encoded data with following fields:

* description - description of condition
* `project_name` - specifies project name for which condition is applied
* `subproject_name` - specified subproject name for which condition is applied

These are required fields for every condition, additional, optional fields are:

* `allowed_days` - days in which project/subproject pair can be added, defaults to [1,...,7]
* `min_start_by_day` - minimal time when entry can start in schedule for every day, defaults to [0,0,0,0,0,0,0] - it can start every day after 0AM.
* `max_start_by_day` - maximal time in day when project can start, default to (23, 23, ..., 23) 
* `min_duration` - minimal amount of hours for entry in schedule to fill, defaults to 0
* `max_duration` - maximal amount of hours for entry to fill, defaults to 23
* `allowed_date` - allowed dates when entry can be used in schedule, default to (1, ..., 31)

For example, to limit yourself to cannot add work hours on weekends:

	{
		"description": "Do not work on weekends",
		"project_name": "Work",
		"subproject_name": "UpWork",
		"allowed_days": [1,2,3,4,5]
	}

When you add new condition, it is applied to all future schedules (not current one), so let's make new schedule:

	mako schedule new

Now you'll see your condition is listed. Let's try to add work to weekend

	mako schedule add 6 12 4 Work Upwork 

Mako will output that condition is not satisfied and will output all descriptions of unsatisfied conditions. 

# Metrics and progress


Mako enables you to measure some metrics and track your progress. You have to specify your metrics in `~/.mako/db/Measurements`. 
For every metric, you have to create one directory and create `measure.json` file. For example, the following structure:

	.
	./Notes size
	./Notes size/measure.json

We create `measure.json` like JSON-encoded data with the following required fields:

* `id` - unique identifier for metric, it si recommended to be without spaces 
* `action` - measurement method to use

Action can be one of the following and every has its own parameters:

* `filesystem.directory.size` - Measures the size of directory in megabytes, requires `path` parameter which is path of directory which size is being measured 
* `filesystem.file.lineCount` - requires `path` and computes number of lines in particular file 
* `org.sections.done.count` - requires `path` parameter which is path to .org file, action computes number of DONE sections in file
* `org.sections.count` - requires `path` and computes number of sections in .org file 
* `os.script` - measurement based on output of executing some script. Requires parameters: `path` - path to the script, `interpreter` - interpreter to run script with (default: sh), `result_as` - path to file where result is stored (stdout to take output as result), `args` - string which represents arguments to script, it is specified like you would pass arguments in command-line. 
* `table.entry.count` - counts entries in a given table. Parameters: `table_name` - name of Mako table, `filter` - specified filter which is used to count only entries where this string is included.

To show all metrics in database, run:

	mako metrics

To run all measurement, run:

	mako measure

# Tables



Tables are a method to store your custom notes and data in tables. It is like small database which comes with Mako. To create table run:

	mako tables new mytable "A|B|C" 

So you have to specify table name and its header, every column is separated by '|'.

To show table, run:

	mako table mytable 

and you'll see empty table, to add an entry to it, run:

	mako table mytable add "1|2|3"

so you basically separate different columns of your entry with pipeline like you do when you create table. You can filter table 
when you want to search for something:

	mako table mytable filter "2"

which will output only entries where at least one column contains specified string. 

In tables you can keep track of something important to you and then measure how many things you have done by using metric which counts entries in table. 

Entries in table are shortened such that it fills screen nice, you can show whole entry by using:

	mako table mytable entry 1 

here 1 is number of entry which you can get when you are showing table with `mako table mytable`.

To delete entry:

	mako table mytable entry 1 delete 

To update entry:

	mako table mytable entry 1 update "column 1|column 2|column 3".

# Reporting system


Mako can make reports on various topics. At this time, two kinds of reports are supported: monthly and quarterly reports. These reports
show some statistics about tasks and projects in general. To generate monthly report, run:

	mako reports generate monthly 2018 1 

where you specify year and month for which you want statistics. 

For quarter reports, run:

	mako reports generate quarterly 2018 1

to generate statistics for the first quarter in 2018. 

To list reports you can do:

	mako reports

and to show particular report, run:

	mako reports show reportName 


# Exporting/importing database to/from JSON

Mako can export its whole database in one json file which you can easily transfer over devices or upload somewhere. For example, you can export whole database and then encrypt it and save to cloud for backup. It can also import database from json.

To export database:

	mako database export json mydb.json

or to import database:

	mako database import json mydb.json

# Importing data from Taskwarrior


You can import data from taskwarrior with:

	mako database import taskwarrior ~/.task

Here just note that taskwarrior is not as powerful as Mako and is not strict as Mako so you can end up with additional work to 
fix some things manually. 
