# pylw
Python Lightweight Web framework

This is intended to be a simple web framework that I will be reusing for other
projects.  This is not a CMS, but I will be building some kind of blogging/CMS
on top of this software.

It supports WSGI.  Unlike some frameworks, WSGI is the primary interface here.

This code borrows ideas and examples from other places, such as falconframework.
I recommend you check out that framework as it's probably better than this one,
at least for now.  My other suggestion is to use flask.

#Idea

The motivation behind this project is to demystify what is happening in the
framework you are running.  Sometimes, I find myself in what I like to call
"Object Oriented Hell".  I spend far too much time tracing through source to
figure out where objects are being initialized, how objects are being passed
around, and how my response is actually getting sent.

#Usage

See main.py for an example on how to use this software.

#Known issues
Too many to list.

Error handling is very primitive.

Need to limit how much post body data we read.
Need to parse form data that is posted.
Would be nice to parse the query string for the user.
