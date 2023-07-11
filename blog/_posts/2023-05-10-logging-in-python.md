---
title: "Mastering the Art of Logging in Python: A Complete Guide"
categories:
  - Tutorials
toc: true
author: Ashutosh Krishna
editor: Mustapha Ahmad Ayodeji

internal-links:
 - Pyhton
 - Logging
 - Guide
 - Logs
excerpt: |
    Learn how to effectively use the Python logging module to track and analyze events in your application. This comprehensive guide covers everything from basic logging to advanced techniques like rotating log files and structured JSON logging.
---

Logging is an essential part of software development, serving as a means to track and analyze events that occur within an application. By recording and storing these events, developers can gain valuable insight into the behavior of their code, identify, and diagnose issues, and optimize application performance. Effective logging is crucial for creating stable, reliable, and scalable applications.

Python's [`logging`](https://docs.python.org/3/library/logging.html) module provides a powerful and flexible framework for implementing logging in software applications. With a wide range of built-in features and configuration options, the `logging` module enables developers to log events at different levels of severity, control the format of log messages, and route logs to different destinations such as files or email. By using the `logging` module, Python developers can easily integrate logging into their code and ensure that their applications are stable and reliable.

By the end of this article, you will have a comprehensive understanding of how to use the Python's logging module, how to configure its behavior according to your specific needs and create robust and reliable applications.

## Prerequisites

Before diving into this tutorial, you should have:

- Working knowledge of the Python programming language, including basic syntax and control flow constructs
- Python version 3.8+ and a code editor installed on your machine

You can find the code samples used in this tutorial in [this repository](https://github.com/ashutoshkrris/logging-tutorial).

## Getting Started With Logging

![Start]({{site.images}}{{page.slug}}/start.png)\

Python's built-in `logging` module provides a flexible and powerful framework for implementing logging in software applications. In this section, you will learn the basics of logging using Python's logging module. These basics include setting up [logging](/blog/understanding-docker-logging-and-log-files) and using different log levels.

### Setting Up Basic Logging

A logger is an object that allows you to record events that occur during the execution of a program. It provides a way to capture and store log messages and events that can be used for debugging, troubleshooting, and analysis of the application's behavior. To get started with logging in Python, you first need to set up the logger. The `logging` module provides a `root` logger by default.
To setup the `root` logger in Python's logging module, you typically use the  [`basicConfig()`](https://docs.python.org/3/library/logging.html#logging.basicConfig) method with the default configuration after importing the logging module:

~~~{.python caption="basic_logging.py"}
import logging

logging.basicConfig()
~~~

> Note: You can skip the `logging.basicConfig()` for a simple logger with no custom configuration, but you'll require it when you wish to configure the logger.

However, it is important to note that it's not always necessary to use `basicConfig()` to set up the root logger. You can simply import the logging module and use the root logger directly, which will use a default configuration that allows messages with a level severity of `WARNING` or above (more about severity level in the next section) to be printed to the console.

### Logging Messages Using Different Log Levels

Logging levels in Python's `logging` module allow you to control the verbosity and importance of the logged messages. Each logging level has a specific purpose and is useful in different situations. Each logging level has a numeric value associated with it that represents its severity. Here are the different [logging](/blog/understanding-docker-logging-and-log-files) levels (or severity levels) that you get with the `logging` module:

- `NOTSET` (0): It is the lowest level in the logging hierarchy and is used to indicate that no specific logging level has been set for a logger or a handler (more on handler later on in the article). It is essentially a placeholder level that is used when the logging level is not explicitly defined.

- `DEBUG` (10): It is used for low-level debugging messages that provide detailed information about the code's behavior. These messages are typically used during development and are not required in production.

- `INFO` (20): It is used to log informational messages about the program's behavior. These messages can be used to track the program's progress or to provide context about the user.

- `WARNING` (30): It is used to log messages that indicate potential issues or unexpected behavior in the program. These messages do not necessarily indicate an error but are useful for diagnosing problems.

- `ERROR` (40): It is used to log messages that indicate an error has occurred in the program. These messages can be used to identify and diagnose problems in the code.

- `CRITICAL`(50): It is used to log messages that indicate a critical error has occurred that prevents the program from functioning correctly. These messages should be used sparingly and only when necessary.

By using different logging levels, you can control the amount of information that is logged and focus on the messages that are most important for your application. This can help you diagnose problems quickly and efficiently, while also reducing the amount of noise in your logs.

When a logger is created, its [logging](/blog/understanding-docker-logging-and-log-files) level is set to `NOTSET` by default. This means that the logger will inherit its effective logging level from its parent logger (more on this in the logging hierarchy section), and if no parent logger is set, it will behave as if its logging level is `NOTSET`.

It's important to note that the `root` logger, which is the highest-level logger in the logging hierarchy, has a default logging level of `WARNING`.

In general, you should not use the `NOTSET` logging level directly. Instead, it is used as a default value when a logging level is not specified. If you want to set a specific logging level for a logger or a handler, you should use one of the predefined logging levels (`DEBUG`, `INFO`, `WARNING`, `ERROR`, `CRITICAL`) or create your own custom logging level.

In the following code, you are using different functions provided by the `logging` module to output messages of different severity levels to the console:

~~~{.python caption="log_levels.py"}
import logging

logging.debug('A Debug Message')
logging.info('An Info Message')
logging.warning('A Warning Message')
logging.error('An Error Message')
logging.critical('A Critical Message')
~~~

Note that it is not mandatory to call the `basicConfig()` method here as you're not required to customize the logger. When you execute the above program, you will observe the following output:

~~~{ caption="debug.log"}
WARNING:root:A Warning Message
ERROR:root:An Error Message
CRITICAL:root:A Critical Message
~~~

The output format for each record includes the log level (e.g. WARNING, ERROR) in uppercase, followed by the name of the default logger, `root`. Finally, the log message that was passed as an argument to the logging function is displayed. Thus the output format looks like this:

~~~{ caption="debug.log"}
<LOG_LEVEL>:<logger_name>:<message>
~~~

As you would notice that only three messages were logged. The `DEBUG` and `INFO` log levels have lower severity than `WARNING`, which is the default severity level set for the root logger, hence they were not logged.

You can use the `logging.basicConfig()` function to set the default severity level as follows:

~~~{.python caption="default_log_level.py"}
import logging

logging.basicConfig(level=logging.INFO)

logging.debug('A Debug Message')
logging.info('An Info Message')
logging.warning('A Warning Message')
logging.error('An Error Message')
logging.critical('A Critical Message')
~~~

The above code can now log messages with a severity level of `INFO` or higher.

Output:

~~~{ caption="debug.log"}
INFO:root:An Info Message
WARNING:root:A Warning Message
ERROR:root:An Error Message
CRITICAL:root:A Critical Message
~~~

Notice that the `DEBUG` message is still not printed because its severity is lesser than `INFO`.

The approach demonstrated above for setting a default log level can help you control the volume of logs generated by your application.

## Customizing Logs

![Customized]({{site.images}}{{page.slug}}/customizing.png)\

The `logging` module provides a powerful and flexible framework for logging messages from your application. In addition to the built-in log levels, you can define your own custom log levels to better represent the severity of messages and to organize and filter your log output based on different parts of your application. You can also customize the format of your log messages using the [string format specifiers](https://docs.python.org/3/howto/logging-cookbook.html#formatting-styles) and adding contextual data to make it easier to read and understand the log output. In this section, you'll explore how to do all of these and more to help you get the most out of the `logging` module.

### Adding Custom Log Levels

The standard logging levels in Python are useful for most use cases, but sometimes you need more levels to better represent the severity or importance of certain log messages.

For example, you might want to add a new log level called `VERBOSE` to represent messages that are more detailed than `DEBUG` messages. The detailed message could be useful for debugging complex problems or monitoring the internal workings of an application.

Here's how you can create a custom `VERBOSE` log level:

~~~{.python caption="custom_log_level.py"}
import logging

# Define the custom log level
VERBOSE = 15
logging.VERBOSE = VERBOSE
logging.addLevelName(logging.VERBOSE, 'VERBOSE')

# Set up basic logging configuration for the root logger
logging.basicConfig(level=logging.DEBUG)


# Define a custom logging method for the new level
def verbose(self, message, *args, **kwargs):
    if self.isEnabledFor(logging.VERBOSE):
        self._log(logging.VERBOSE, message, args, **kwargs)


# Add the custom logging method to the logger class
logging.Logger.verbose = verbose

# Create a logger instance
logger = logging.getLogger()

# Log a message using the custom level and method
logger.verbose("This is a verbose message")
~~~

First, you define a custom log level called `VERBOSE` with a value of 15. You named the log level `VERBOSE` and add it to the logging module's constants. Since the severity value for `VERBOSE` is 15, you'll need to set up the default logging level to `DEBUG` (has a value of 10). It means that all messages with a severity level of `DEBUG` or higher will be logged.

Similar to other methods like `logging.debug`, `logging.info`, etc, you create a `verbose` method that takes in a message, along with optional arguments and keyword arguments. The method checks if the logger is enabled for the `VERBOSE` level, and if it is, it logs the message using the [`_log()`](https://github.com/python/cpython/blob/3.11/Lib/logging/__init__.py#L1610) method.

Then, you'll need to add this verbose method to the [`Logger`](https://docs.python.org/3/library/logging.html#logging.Logger) class in the `logging` module, so that it can be used by any logger instance.

Next, you can test the `verbose` log level by creating a logger instance using the [`getLogger()`](https://docs.python.org/3/library/logging.html#logging.getLogger) method. The method returns a logger object that can be used to emit log messages from the calling module. Finally, you can log a verbose message.

Output:

~~~{ caption="debug.log"}
VERBOSE:root:This is a verbose message
~~~

> You can find a more advanced example in [this Stackoverflow thread](https://stackoverflow.com/a/35804945/1691778).

### Customizing the Log Format

By default, the `logging` module uses a simple format that shows the severity level, the name of the logger, and the log message. This format is shown below:

~~~{ caption="debug.log"}
WARNING:root:A Warning Message
~~~

However, the `logging` module provides a way to customize the log message's format. Customizing the log format helps developers to identify and diagnose issues in their code more easily. By including additional information such as the timestamp, the severity level, the module or function that generated the log message, and any relevant contextual data, developers can get a more complete picture of what's happening in their application and can quickly pinpoint the source of any issues.

If you notice the default log format, you'll find the timestamp missing. Most of the log management tools such as [Datadog](https://www.datadoghq.com/), [Splunk](https://www.splunk.com/), etc. provide filtering options for timestamps, and hence it's a good idea to add timestamps in your log format.

To customize the log format, you can use the `format` parameter of the `basicConfig()` method. The `format` parameter takes a string that defines the format of the log message. If the `format` parameter is specified, it determines the `style` for the format string to be used with one of the three options: `%` for [printf-style](https://docs.python.org/3/library/stdtypes.html#old-string-formatting), `{}` for [str.format()](https://docs.python.org/3/library/stdtypes.html#str.format), or `$` for [string.template](https://docs.python.org/3/library/string.html#string.Template). The default value for the `style` parameter is `%`.

Here's an example showing how you can customize the log format using the `format` parameter:

~~~{.python caption="customized_log_format.py"}
import logging

logging.basicConfig(format='%(asctime)s | %(levelname)s : %(message)s')

logging.error('An error occurred!')
~~~

The log message format string can include placeholders that represent various [LogRecord attributes](https://docs.python.org/3/library/logging.html#logrecord-attributes). These attributes include the log message, log level, logger name, timestamp, and more.

In the above example, the `format` parameter's value contains three placeholders:

- `%(asctime)s`: The timestamp of the log message.
- `%(levelname)s`: The severity level of the log message, with a width of 8 characters.
- `%(message)s`: The log message.

The `"s"` at the end of `%(placeholder)s` is a code used in string formatting. It indicates that the value being inserted is a string data type.

Output:

~~~{ caption="debug.log"}
2023-03-05 11:05:50,528 | ERROR : An error occurred!
~~~

Now you can see that the output contains the timestamp, log level, and message.

### Setting Up Custom Loggers

Creating custom loggers can be useful when you want to separate different parts of your codebase into different logs, each with its own configuration. This can be particularly useful when working on large projects with multiple modules or when you want to log to different destinations or with different formats. Custom loggers can also allow you to control the level of logging for each part of your codebase independently, providing more fine-grained control over which logs are emitted in different parts of the application.

Up until this point in the tutorial, you have utilized the default `root` logger for logging in the provided examples. To create a custom logger, you can use the [`logging.getLogger(name)`](https://docs.python.org/3/library/logging.html#logging.getLogger) method, where `name` is a string identifier for your logger. The identifier can be any string, but it's recommended to use the name of the module or component you're logging for clarity.

You can then configure the custom logger's behavior separately from the root logger using the same configuration methods covered earlier, such as `logging.basicConfig()`. Any log entries created using this custom logger will be filtered and formatted according to the custom configuration you've set up.

Here's an example of how to set up a custom logger:

~~~{.python caption="custom_logger.py"}
import logging

logger = logging.getLogger("my_module")

logger.debug('A Debug Message')
logger.info('An Info Message')
logger.warning('A Warning Message')
logger.error('An Error Message')
logger.critical('A Critical Message')
~~~

The `getLogger()` method returns an instance of the `Logger` class with the specified name argument (in this case, "my_module"). By default, you only get the log message in the output:

~~~{ caption="debug.log"}
A Warning Message
An Error Message
A Critical Message
~~~

You can see that the Logger object logs to the [standard error](https://docs.python.org/3/library/sys.html#sys.stderr) (stderr) by default.

## Handlers, Formatters, and Filters

To customize the output format and behavior of a custom logger, the `logging` module provides the `Formatter` and the `Handler` classes. The [`Formatter`](https://docs.python.org/3/library/logging.html#formatter-objects) is responsible for formatting the log output, while the [`Handler`](https://docs.python.org/3/library/logging.html#handler-objects) specifies where the log messages should be sent, such as the console, a file, or an HTTP endpoint. The [`Filter`](https://docs.python.org/3/library/logging.html#filter-objects) objects are available to provide advanced filtering capabilities for both Loggers and Handlers.

### Understanding Handlers and Their Role in Logging

Handlers are responsible for defining where the log messages should be sent. A Handler can be thought of as a "channel" through which log messages are passed. When a log message is created, it is sent to the associated logger which then passes the message to its Handlers.

Handlers can be configured to write logs to various destinations, such as a file, the console, a network socket, or an email. There are several [built-in Handlers](https://docs.python.org/3/library/logging.handlers.html) in the logging module that provide various logging options, including StreamHandler, FileHandler, and SMTPHandler.

Here's an example that sends the output of the logger to a file called `my_module.log` instead of the standard error:

~~~{.python caption="handlers.py"}
import logging

# Create a custom logger
logger = logging.getLogger('my_module')

# Create a file handler for the logger
handler = logging.FileHandler('my_module.log')

# Add the handler to the logger
logger.addHandler(handler)

# Log a message using the custom logger
logger.warning('This is a log entry for my_module')
~~~

The [`FileHandler`](https://docs.python.org/3/library/logging.handlers.html#filehandler) accepts a filename as the argument. The `filename` parameter is a string value that represents the path of the file where the logs will be written. If the file specified in the `filename` parameter of the `FileHandler` does not exist, the `FileHandler` will create it automatically. If the file already exists, the `FileHandler` will open it in append mode by default. The `handler` object is added to the logger so that any messages logged by the logger will be written to the file.

When you run the code for the first, you'll have a new `my_module.log` file created with the content below:

~~~{ caption="my_module.log"}
This is a log entry for my_module
~~~

For the subsequent runs, the log output will be appended to the same file.

### Understanding Formatters and Their Impact on the Log Format

Formatters are an essential component of the Python logging system, used to specify the structure of log messages. They control the output format of log messages, which can include information like timestamps, log levels, and log message details.

By default, the log message from the `Logger` has a format of `%(message)s`. But you can customize the format by creating your own formatter instance and specifying the format. To create a custom formatter, you can use the `Formatter` class provided by the `logging` module. The class takes a string argument that specifies the format of the log message output.

~~~{.python caption="formatters.py"}
import logging

# Create a custom logger
logger = logging.getLogger('example')

# Create a file handler for the logger
handler = logging.FileHandler('example.log')

format = logging.Formatter(
    "%(asctime)s | %(name)s | %(levelname)s : %(message)s"
)

handler.setFormatter(format)

# Add the handler to the logger
logger.addHandler(handler)

# Log a message using the custom logger
logger.critical('This is a log entry for example')
~~~

This code sets up a custom logger named `example` and creates a file handler for it. It then creates a `Formatter` object with a specific log format and associates it with the handler using the [`setFormatter()`](https://docs.python.org/3/library/logging.html#logging.Handler.setFormatter) method. Finally, the handler is added to the logger using the `addHandler()` method.

When a log entry is made using the logger, the [log record](https://docs.python.org/3/library/logging.html#logging.LogRecord) is passed to the handler, which applies the formatter to the record and then outputs the resulting log message to a file named `example.log`. In this case, the log message will include the timestamp, logger name, log level, and log message.

~~~{ caption="example.log"}
2023-03-05 12:15:11,374 | example | CRITICAL : \
This is a log entry for example
~~~

### Understanding Filters and Their Usage in Logging

Filters provide a way to perform more advanced filtering of log records than just specifying a logging level. A filter is a class that has a method called [`filter(record)`](https://docs.python.org/3/library/logging.html#logging.Logger.filter) which is called for each record passed to the filter. The method should return `True` if the record should be processed further, or `False` if the record should be ignored.

Filters can be applied to both loggers and handlers. When applied to a logger, the filter will be applied to all handlers associated with the logger. When applied to a handler, the filter will be applied to all records that pass through the handler.

To use a filter in a logger or handler, you create an instance of the filter class and add it to the logger or handler using the [`addFilter()`](https://docs.python.org/3/library/logging.html#logging.Logger.addFilter) method. For example:

~~~{.python caption="filters.py"}
import logging


class RecordFilter(logging.Filter):
    def filter(self, record):
        return record.msg.startswith('Important:')


logger = logging.getLogger('filtered_logger')
handler = logging.FileHandler('filtered_log.log')
handler.setFormatter(logging.Formatter(
    '%(asctime)s | %(levelname)s : %(message)s'))
handler.addFilter(RecordFilter())
logger.addHandler(handler)

logger.warning('Important: This message should be logged')
logger.warning('This message should not be logged')
~~~

In this example, the custom filter class `RecordFilter` inherits from the `logging.Filter` class. You override the `filter()` method to check if the log record message starts with the string `"Important:"`. If it does, the method returns `True` indicating that the record should be logged, otherwise it returns `False` indicating that the record should be discarded.

Next, you create a logger object named `filtered_logger` and add a file handler to it. You set the formatter for the handler to print the timestamp, log level, and message. Finally, you add an instance of `RecordFilter` to the handler using the `addFilter()` method. This means that the `filter()` method of the `RecordFilter` class will be called for each log message before it is emitted, and any log messages that do not start with the string `Important:` will be discarded.

You then log two messages using the logger object. If you see the newly created `filtered_log.log` file, you'll have the following content:

~~~{ caption="filtered_log.log"}
2023-03-05  12:33:14,810 | WARNING : \
Important: This message should be logged
~~~

The first message starts with the string "Important:", so it passes the filter and is logged with a level of `WARNING`. The second message does not start with the string "Important:", so it fails the filter and is not logged.

## Structured JSON Logging and Error Logging

Up to this point in the tutorial, we have been using a custom plain text format for logging that is designed to be readable by humans. Traditional logging can sometimes fall short in providing comprehensive insights into the application's behavior. Structured [JSON](/blog/convert-to-from-json) logging aims to solve this problem by providing more structured, machine-readable log entries that can be easily analyzed and processed.

### The `python-json-logger` Library

The [`python-json-logger`](https://pypi.org/project/python-json-logger/) library is a popular Python library for structured logging. It extends Python's built-in logging module and provides a new formatter that outputs log records in JSON format. With this library, you can easily customize the format of your logs, add additional metadata, and make your logs more machine-readable.

To use this library, you first need to install it by running the following command:

~~~{.bash caption=">_"}
pip install python-json-logger
~~~

The `python-json-logger` library provides a custom formatter called [`JsonFormatter`](https://github.com/madzak/python-json-logger#integrating-with-pythons-logging-framework) to format log records as JSON strings. Once installed, you can use the `JsonFormatter`  as shown below:

~~~{.python caption="json_formatter.py"}
import sys
import logging
from pythonjsonlogger import jsonlogger

logger = logging.getLogger(__name__)

stdout = logging.StreamHandler(stream=sys.stdout)

format = jsonlogger.JsonFormatter(
    "%(asctime)s | %(levelname)s : %(message)s"
)

stdout.setFormatter(format)
logger.addHandler(stdout)

logger.warning('A Warning Message')
logger.error('An Error Message')
logger.critical('A Critical Message')
~~~

The `jsonlogger.JsonFormatter("%(asctime)s | %(levelname)s : %(message)s")` creates a formatter that formats the log record in JSON format, including the timestamp, log level, and log message.

Output:

~~~{ caption="debug.log"}
{"asctime": "2023-03-05 12:46:07,625", "levelname": \
"WARNING", "message": "A Warning Message"}
{"asctime": "2023-03-05 12:46:07,625", "levelname": \
"ERROR", "message": "An Error Message"}
{"asctime": "2023-03-05 12:46:07,626", "levelname": \
"CRITICAL", "message": "A Critical Message"}
~~~

By default, you'll see the original names from the [LogRecord attributes](https://docs.python.org/3/library/logging.html#logrecord-attributes) as the keys. If you want to rename the keys, you can use the `rename_fields` argument as shown below:

~~~{.python caption="rename_fields.py"}
format = jsonlogger.JsonFormatter(
    "%(asctime)s | %(levelname)s : %(message)s",
    rename_fields={"levelname": "log_level", "asctime": "timestamp"},
)
~~~

The above code renames the `levelname` key to `log_level` and the `asctime` key to `timestamp`.

Output:

~~~{ caption="debug.log"}
{"timestamp": "2023-03-05 12:51:23,538", "log_level": \
"WARNING", "message": "A Warning Message"}
{"timestamp": "2023-03-05 12:51:23,539", "log_level": \
"ERROR", "message": "An Error Message"}
{"timestamp": "2023-03-05 12:51:23,539", "log_level": \
"CRITICAL", "message": "A Critical Message"}
~~~

### The `extra` Property

The `python-json-logger` library allows you to add contextual information to your logs via the `extra` parameter without requiring modifications to the log format. For example, if you are logging events from a web application, you might want to include information about the current user, the HTTP request being processed, or the session ID in the log entries. By adding this information to the `extra` dictionary, you can include it in the log output without cluttering up the log format itself. The keys provided in the extra dictionary will be included in the JSON output as top-level keys.

In the previous example, you can add the `extra` property as:

~~~{.python caption="extra_property.py"}
logger.warning('A Warning Message')
logger.error('An Error Message', extra={'type': 'fatal error'})
logger.critical('A Critical Message')
~~~

Output:

~~~{ caption="debug.log"}
{"timestamp": "2023-03-05 17:48:20,531", "log_level": \
"WARNING", "message": "A Warning Message"}
{"timestamp": "2023-03-05 17:48:20,531", "log_level": \
"ERROR", "message": "An Error Message", "type": "fatal error"}
{"timestamp": "2023-03-05 17:48:20,531", "log_level": \
"CRITICAL", "message": "A Critical Message"}
~~~

You can see that an extra `type` key has been added in the output for `logger.error()`.

Note that you should avoid using default [LogRecord attribute names](https://docs.python.org/3/library/logging.html#logrecord-attributes) to prevent `KeyError` exceptions.

~~~{.python caption="extra_property.py"}

logger.error('An Error Message', extra={'name': 'Ashutosh'})
~~~

The above code throws a `KeyError` exception because `name` is one of the LogRecord attributes:

~~~{ caption="debug.log"}
KeyError: "Attempt to overwrite 'name' in LogRecord"
~~~

### Logging Errors

In Python, logging errors is crucial to the debugging process. The logging module provides different levels of severity to record errors. For example, the primary way to log an error is at the `ERROR` level, but if the issue is particularly severe, you can use the `CRITICAL` level instead.

Let's say you're running a critical system, such as a financial transaction processing application, and there's an issue with the system that may cause financial transactions to fail or be lost. In such situations, logging the error at the `CRITICAL` level would indicate the severity and urgency of the issue, and may be more suitable than logging it at the `ERROR` level.

To log exceptions, the module offers an [`exception()`](https://docs.python.org/3/library/logging.html#logging.Logger.exception) method that is an alias for `logging.error(<msg>, exc_info=1)`. The `exc_info` argument should only be used in an exception context; otherwise, it will be set to `None` in the output.

Here's an example of logging an error with exception info:

~~~{.python caption="logging_error.py"}
import sys
import logging
from pythonjsonlogger import jsonlogger

logger = logging.getLogger(__name__)

stdout = logging.StreamHandler(stream=sys.stdout)

format = jsonlogger.JsonFormatter(
    "%(asctime)s | %(levelname)s : %(message)s",
    rename_fields={"levelname": "log_level", "asctime": "timestamp"},
)

stdout.setFormatter(format)
logger.addHandler(stdout)
logger.setLevel(logging.INFO)

try:
    num = int('A')
except ValueError as e:
    logger.error('Failed to convert to int', exc_info=True)
    logger.exception('Failed to convert to int')
~~~

In the above code, a try-except block is used to simulate an error. An attempt is made to convert the string 'A' to an integer, which will raise a `ValueError`. The error is caught in the except block and logged using the `error()` and `exception()` methods of the logger. The `exc_info` parameter is set to `True` in the `error()` method to include the exception information in the log message.

Output:

~~~{ caption="debug.log"}
{"timestamp": "2023-03-05 18:04:10,876", 
"log_level": "ERROR", "message": "Failed to convert to int", 
"exc_info": "Traceback (most recent call last):\n  
File \"D:\\Blog-Codes\\logging\\code14.py\", line 19, in <module>\n    
num = int('A')\n          ^^^^^^^^\n
ValueError: invalid literal for int() with base 10: 'A'"}
{"timestamp": "2023-03-05 18:04:10,877", "log_level": "ERROR", 
"message": "Failed to convert to int", 
"exc_info": "Traceback (most recent call last):\n  
File \"D:\\Blog-Codes\\logging\\code14.py\", line 19, in <module>\n    
num = int('A')\n          ^^^^^^^^\n
ValueError: invalid literal for int() with base 10: 'A'"}
~~~

Both the log outputs are exactly the same. As mentioned, the `exception()` method is just a shortcut for `error(exc_info=True)` and will log both the error message and the traceback of the exception.

> Note: Using `1` or `True` for the `exc_info` parameter would have the same effect of adding information about the current exception being handled to the log message.

## Advanced Logging

![Advanced]({{site.images}}{{page.slug}}/advance.png)\

In this section, you will learn an advanced logging techniques like rotating log files automatically using [`RotatingFileHandler`](https://docs.python.org/3/library/logging.handlers.html#rotatingfilehandler) and [`TimedRotatingFileHandler`](https://docs.python.org/3/library/logging.handlers.html#timedrotatingfilehandler). Additionally, you'll also learn about the logging hierarchy.

### Automatically Rotating Log Files

Rotating log files is a common technique to avoid filling up your hard drive with old log messages. It is useful when a large number of log messages are being generated and you want to save disk space by keeping only a certain number of log files. By rotating log files, you can keep a specific number of log files and automatically delete older log files to avoid using up too much disk space. This is particularly useful in production environments where logging can generate large amounts of data over time. Additionally, rotating log files can help with troubleshooting and debugging by providing a history of log messages.

For example, consider a web application that receives a high volume of traffic and generates log files for each user request. Without rotating log files, these log files can quickly grow to consume a significant amount of disk space, which can be a problem if disk space is limited. In this case, rotating log files allows the application to continue generating logs without running out of disk space. The logs are split into smaller files, which are easier to manage, compress, and delete as necessary.

In the logging module, the [`RotatingFileHandler`](https://docs.python.org/3/library/logging.handlers.html#rotatingfilehandler) class is used to rotate logs based on size or time intervals. This class will create a new log file once the current log file reaches a certain size or after a certain time interval.

Here is an example of how to use `RotatingFileHandler` to create a log file that is rotated when it reaches 1 MB in size:

~~~{.python caption="rotating_file_handler.py"}
import logging
from logging.handlers import RotatingFileHandler

logger = logging.getLogger(__name__)

handler = RotatingFileHandler('app.log', maxBytes=1000000, backupCount=5)
handler.setLevel(logging.DEBUG)

formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)

logger.addHandler(handler)
~~~

The `RotatingFileHandler` takes a filename as its argument and also includes two important properties - `backupCount` and `maxBytes`. The `backupCount` determines the number of backup files to keep, while the `maxBytes` sets the maximum size of each log file before it is rotated.

The above code creates a `RotatingFileHandler` object that will rotate the log file `app.log` once it reaches 1 MB in size, keeping up to 5 backups of the previous log files. The `logging.Formatter` object is used to format the log messages, and the handler is added to the logger.

Once the log file reaches the maximum size, the `RotatingFileHandler` will rename the current log file to a numbered backup file (e.g. `app.log.1`), and create a new log file with the original name (`app.log`). This process continues as new log files are created, with older log files being renamed and rotated out of the system to make room for newer logs. In this way, the `RotatingFileHandler` provides a simple and effective way to manage log files and keep them from growing too large.

The [`TimedRotatingFileHandler`](https://docs.python.org/3/library/logging.handlers.html#timedrotatingfilehandler) is another handler provided by the Python logging module that can be used for rotating log files. This handler rotates the log files based on time intervals, rather than file size. The `TimedRotatingFileHandler` takes a few arguments, including the filename, the [interval](https://docs.python.org/3/library/logging.handlers.html#timedrotatingfilehandler) at which to rotate the log files (e.g., 'S' for seconds, 'M' for minutes, etc.), and the number of backups to keep. This handler is useful for applications that generate large log files and need to maintain a regular log rotation schedule.

~~~{.python caption="timed_rotating_file_handler.py"}
import logging
from logging.handlers import TimedRotatingFileHandler

# Set up the logger
logger = logging.getLogger(__name__)

# Create the TimedRotatingFileHandler
handler = TimedRotatingFileHandler(filename='myapp.log', \
when='midnight', backupCount=7)

# Set the log message format
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)

# Add the handler to the logger
logger.addHandler(handler)
~~~

### Understanding the Python Logging Hierarchy

The Python `logging` module provides a hierarchical structure for organizing loggers and handlers. Understanding the hierarchy is essential to creating a flexible and scalable logging system. In the logging hierarchy, each logger is associated with a hierarchical name, and loggers are arranged in a tree-like structure. The `root` logger is at the top of the hierarchy, and other loggers are its descendants.

The logger hierarchy is organized in a dot-separated namespace, similar to the module namespace in Python. For example, a logger named "a.b.c" is a descendant of "a.b", which is, in turn, a descendant of "a". If a logger is not explicitly defined, it inherits from its parent logger.

~~~{.python caption="logging_hierarchy.py"}
import logging

abc_logger = logging.getLogger("a.b.c")
ab_logger = logging.getLogger("a.b")
a_logger = logging.getLogger("a")

print(abc_logger.parent)
print(ab_logger.parent)
print(a_logger.parent)
~~~

Output:

~~~{ caption="Output"}
<Logger a.b (WARNING)>
<Logger a (WARNING)>
<RootLogger root (WARNING)>
~~~

The [`propagate`](https://docs.python.org/3/library/logging.html#logging.Logger.propagate) method in the logging hierarchy refers to the way a log message is passed up the logger hierarchy. By default, loggers propagate messages up to their ancestors in the logger hierarchy until a logger with a handler is found. The message is then handled by the handler of that logger.

The `propagate` method is a boolean attribute of a logger that controls whether messages generated by child loggers of a logger are passed up to the parent logger. If `propagate` is set to True (default), then messages generated by child loggers are passed up to the parent logger. If `propagate` is set to False, then messages generated by child loggers are not passed up to the parent logger.

Consider an example where we have two loggers named "a.b" and "a". Here's an example of how the `propagate` attribute works in this scenario:

~~~{.python caption="propagate.py"}
import logging

# Create two loggers
logger_a = logging.getLogger('a')
logger_a_b = logging.getLogger('a.b')

# Set the propagate attribute of logger_a_b to False
logger_a_b.propagate = False

# Create a StreamHandler and set the logging level to INFO
handler = logging.StreamHandler()
handler.setLevel(logging.INFO)

# Create a formatter and set the format of handler
format = logging.Formatter('%(levelname)s:%(name)s:%(message)s')
handler.setFormatter(format)

# Add the handler to both loggers
logger_a.addHandler(handler)
logger_a_b.addHandler(handler)

# Log messages
logger_a.warning('warning message from logger_a')
logger_a_b.warning('warning message from logger_a_b')
~~~

Output:

~~~{ caption="debug.log"}
WARNING:a:warning message from logger_a
WARNING:a.b:warning message from logger_a_b
~~~

In this output, the first message was generated by the `logger_a` logger, and the second message was generated by the `logger_a_b` child logger. Since `propagate` was set to `False` for `logger_a_b`, the message generated by `logger_a_b` was not passed up to the parent logger `logger_a`.

### Configuring Loggers With `dictConfig`

Up until now in the tutorial, you have learned to configure the logger using Python script directly. The `logging` module provides a [`logging.config`](https://docs.python.org/3/library/logging.config.html#module-logging.config) API for configuring the loggers. While the API provides four functions, you're going to learn about [`logging.config.dictConfig`](https://docs.python.org/3/library/logging.config.html#logging.config.dictConfig) in this section.

The `logging.config.dictConfig` accepts a [dictionary](https://blog.ashutoshkrris.in/everything-you-need-to-know-about-python-dictionaries) with the logging configuration. If there's a configuration error, the function raises an appropriate exception (`ValueError`, `TypeError`, `AttributeError`, or `ImportError`) with a helpful error message.

The dictionary must have the following keys:

1. `version` - an integer indicating the schema version that is being used. If the logging configuration schema changes in the future, the `version` key will be used to indicate which version of the schema the `dictConfig` is using. This allows the `dictConfig` function to handle both current and future schema versions.

2. `formatters` - a dictionary with each key being a formatter id and its value describing how to configure the corresponding [Formatter](https://docs.python.org/3/library/logging.html#logging.Formatter) instance.

3. `filters` - a dictionary with each key being a filter id and its value describing how to configure the corresponding [Filter](https://docs.python.org/3/library/logging.html#logging.Formatter) instance.

4. `handlers` - a dictionary with each key being a handler id and its value describing how to configure the corresponding [Handler](https://docs.python.org/3/library/logging.html#logging.Handler) instance.

      All other keys are passed through as keyword arguments to the handler's constructor.

5. `loggers` - a dictionary with each key being a logger name and its value describing how to configure the corresponding Logger instance.

6. `root` - the configuration for the root logger. It's processed like any other logger, except that the propagate setting is not applicable.

7. `incremental` - a boolean indicating whether the configuration specified in the dictionary should be merged with any existing configuration, or should replace entirely. Its default value is `False`, which means that the specified configuration replaces any existing configuration.

8. `disable_existing_loggers` - a boolean indicating whether any non-root loggers that currently exist should be disabled. If absent, this parameter defaults to `True`. Its value is ignored when incremental is `True`.

Here's how you can define the configurations in the form of a dictionary using `dictConfig`:

~~~{.python caption="dictconfig.py"}
import logging
import logging.config

# Declare handlers, formatters and all functions \
# using dictionary 'key' : 'value' pair
logging.config.dictConfig({
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'consoleFormatter': {
            'format': '%(asctime)s | %(name)s | \
            %(levelname)s : %(message)s',
        },
        'fileFormatter': {
            'format': '%(asctime)s | %(name)s | \
            %(levelname)s : %(message)s',
        },
    },
    'handlers': {
        'file': {
            'filename': 'debug.log',
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'formatter': 'fileFormatter',
        },
        'console': {
            'level': 'CRITICAL',
            'class': 'logging.StreamHandler',
            'formatter': 'consoleFormatter',
        },
    },
    'loggers': {
        '': {
            'handlers': ['file', 'console'],
            'level': 'DEBUG',
        },
    },
})

# Define your own logger name
logger = logging.getLogger("my_logger")

# Write messages with all different types of levels
logger.debug('A Debug Message')
logger.info('An Info Message')
logger.warning('A Warning Message')
logger.error('An Error Message')
logger.critical('A Critical Message')
~~~

The dictionary contains several keys that define the different components of the logging system. These include the `version` of the configuration schema, `formatters` for formatting log messages, `handlers` for specifying where the log messages should be sent, `loggers` for organizing log messages by name, and settings for configuring the root logger.

In this example, two formatters are defined, one for the console output and another for file output. Two handlers are also defined, one for writing to a file and another for console output. The logger is then defined to use both of these handlers and set to log at the `DEBUG` level. The empty string `''` as the logger name in the `loggers` dictionary refers to the root logger. In other words, this configuration applies to the root logger, which is the parent logger for all loggers in the hierarchy that have not been explicitly configured.

After configuring the logging system, a custom logger is created with the name `my_logger`. Messages with different log levels are then logged using this logger, including DEBUG, INFO, WARNING, ERROR, and CRITICAL messages.

Here's the output you'll see in the `debug.log` file:

~~~{ caption="debug.log"}
2023-03-15 08:53:22,046 | my_logger | DEBUG : A Debug Message
2023-03-15 08:53:22,046 | my_logger | INFO : An Info Message
2023-03-15 08:53:22,046 | my_logger | WARNING : A Warning Message
2023-03-15 08:53:22,046 | my_logger | ERROR : An Error Message
2023-03-15 08:53:22,046 | my_logger | CRITICAL : A Critical Message
~~~

But, in the console, you'll see this output:

~~~{ caption="debug.log"}
2023-03-15 08:53:22,046 | my_logger | \
CRITICAL : A Critical Message
~~~

There is a difference in the outputs because the `file` handler handles messages of level DEBUG and higher. But the `console` handler only handles messages of level CRITICAL and higher.

Apart from this, the `logging` module in Python also provides the ability to configure loggers and handlers using configuration files in YAML or JSON format. YAML is generally used because it's a little more readable than the equivalent Python source form for the dictionary.

Here is an equivalent YAML configuration file called `config.yaml` for the above-shown configuration:

~~~{.yml caption="config.yaml"}
version: 1
disable_existing_loggers: False

formatters:
  consoleFormatter:
    format: '%(asctime)s | %(name)s | %(levelname)s : %(message)s'
  fileFormatter:
    format: '%(asctime)s | %(name)s | %(levelname)s : %(message)s'

handlers:
  file:
    filename: debug_yaml.log
    level: DEBUG
    class: logging.FileHandler
    formatter: fileFormatter
  console:
    level: CRITICAL
    class: logging.StreamHandler
    formatter: consoleFormatter

loggers:
  root:
    level: DEBUG
    handlers: [file, console]
~~~

To read this YAML configuration file in a Python application, you first need to install the [`PyYAML`](https://pypi.org/project/PyYAML/) library as below:

~~~{.bash caption=">_"}
pip install pyyaml
~~~

Once the library is installed, you can use this configuration file in your Python application as below:

~~~{.python caption="yaml_config.py"}
import logging.config
import yaml

with open('config.yaml') as f:
    config = yaml.safe_load(f.read())
    logging.config.dictConfig(config)

# Now, log messages using the your own logger
logger = logging.getLogger("my_logger")

# Write messages with all different types of levels
logger.debug('A Debug Message')
logger.info('An Info Message')
logger.warning('A Warning Message')
logger.error('An Error Message')
logger.critical('A Critical Message')
~~~

In this code, you first open and load the YAML configuration file using the `yaml` module. You then pass the configuration dictionary to the `dictConfig` method of the `logging.config` module. This sets up the logging configuration for the application using the settings specified in the configuration file.

When you run the Python file, the output will remain the same as in the previous example.

## Best Practices for Logging in Python

In order to effectively use logging in Python, you should consider the following best practices:

- Use meaningful log messages that accurately describe what's happening in your code.
- Log at the appropriate level to ensure that your logs contain the necessary information without being cluttered with unnecessary details.
- Consider using custom loggers to help organize and categorize your logs based on different parts of your code or different components of your application.
- Rotate your logs to save disk space and ensure that you can easily find and analyze relevant logs from different points in time.
- Make sure to handle errors and exceptions appropriately in your logging code to avoid unexpected behavior and ensure that you capture all relevant information.
- Consider using structured logging formats like [JSON](/blog/convert-to-from-json) or XML to make it easier to parse and analyze your logs with automated tools.

## Conclusion

Logging is an important aspect of software development that helps in monitoring, debugging, and analyzing the behavior of an application. Python provides a powerful and flexible logging module that allows developers to implement various logging features in their applications.

In this article, you learned the basics of logging in Python, including setting up logging, logging messages at different levels, and customizing logs. We also explored the concept of loggers, handlers, formatters, and filters, and how they work together to produce useful logs. You also explored more advanced logging techniques such as rotating log files and using the structured JSON logging library.

In addition, the article also discussed the Python logging hierarchy, which provides a way to organize loggers in a hierarchy and control how log messages are propagated up the hierarchy. The article also highlighted best practices for logging in Python, such as using meaningful log messages, logging at the appropriate level, using custom loggers, and rotating logs to save disk space. By following best practices and leveraging the advanced features of the logging module, developers can ensure that their applications are well-architected and easily maintainable.

{% include_html cta/bottom-cta.html %}
