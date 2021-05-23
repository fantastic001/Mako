
# Requirements 

What has to be done:

* User guide 
* better error checking and input checking
* curses gui 
* GCal integration (check https://developers.google.com/calendar/v3/reference/calendarList)
* Trello integration (check https://github.com/tghw/trello-py)
* Jira integration
* Providing REST API to Mako database (possibly integrate this into ArgumentStack)



# Adaptability of the system 

the whole system has to be adaptable in a sense it supports plugin system where plugins can add additional functionality to:

* command line interface 
* transformations on tables created and entities added
* additional classes to measurement activities 
* schedule transformations on schedule changes and creations
* project/subproject/task transformations on CRUD operations 
* plugin system should have access to Mako database used 
* easy plugin installation process 


# Autonomy

* Mako should not depend on other tools except ArgumentStack, other modules should be loaded if needed only 


# Database redundancy 

* Mako should keep all history of its databases and ability to recover and see differences in history
* Database backups should be packed into JSON as just one file 


# Refactoring 

* refactor whole application to use 3-tier architecture pattern:
	* Data management (with database backends, data representation etc) - provides MakoDatabaseFactory to return wanted database given the configuration as MakoConfiguration object
	* business logic - all data transformations and functionality available to user through MakoCRUD component 
	* Data view - ArgumentStack based or curses based or GUI based. Has only access to MakoCRUD instance 
* Dividing MakoDatabase interface into multiple interfaces which are provided by MakoDatabaseFactory 
* Transaction handling - implement something like journaling 
* All interfaces should have only one function, for instance: MakoTableAddInterface and every interface provides:
	* operation functionality 
	* consistency checking mechanism after operation is done 
	* rollback mechanism 
	* execute() method which will:
		* do consistency check 
		* if check fails, do the following: execute operation, do consistency check, if it fails again, rollback and throw InconsistencyDetectionException
	* these interfaces also should have methods for journaling 
* Databases should be organized to be normalized at least to BCNF 
* As database backend, sqlite can be considered  which keeps sync with other databases maybe 
* checking all input from ArgumentStack if it is valid 
* In MakoCRUD, all exceptions should be caught and sent to ErrorListeners registered in MakoCRUD instance if these exceptions cannot be handeled 
* Error messages should be detailed as much as possible since applications is used in local mode. MakoCRUD should publish errors in MakoError object with: 
	* title
	* message
	* underlying exception
	* timestamp of error occurance 
* For each copy of database in history, checksum is also stored 
* MakoCRUD uses logging to log every aspect of working application 
* MakoLogger is used for logging and it is an interface registered to MakoCRUD as well as to all MakoDatabaseInterface objects inheriting Loggable which has addLogger and info(...), debug(...), ... methods


# Ideas 

+ move report views to reports directory 
+ create AMS action for excel tables 
+ use better declarative style for stack arguments 