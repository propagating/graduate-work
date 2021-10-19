#--------------------------------------------------
# Lab 1: Basic R and Plotting with ggplot2
#--------------------------------------------------

# You can think of R like a fancy calculator!
# executing each of these lines generates output
# to the console
1 / 300
3 * 45
4^3
sin(3*pi)

# To create variables and other reuseable objects 
# you can either use "<-" or "="
# by convention R uses "<-" but if you find it weird, you can use "="

# assign the value of 1 to the variable x
x <- 1

# see the class of an object you created
class(x)

y <- 3

# we can manipulate combinations of the objects
z <- x * y
print(z)

# note objects inherit the type from their parents
class(z)

# we can also store characters as objects
x <- "i love R!"
print(x)

# functions
# there are many helper functions that allow you 
# perform more complicated processes

# these functions usually take in arguments
# to view the arguments the function expects type '?`function_name`()'
?seq

# print a sequence of numbers from 1 to 10 in steps of 1
seq(from = 1,to = 10)

# print a sequence of numbers from 1 to 10 in steps of 3!
# we can omit the "from =" and "to =" because these are in order 
# the function expects
seq(1,12, by = 3)


### Vectors # 
# vectors are an arbitrary collection of numbers or characters
# but not both types!

# create a vector 
myVec <- c(5, 3, 7)
print(myVec)
is.vector(myVec)


# We can store characters as vectors character vectors
my_Char_Vec <- c("I", "love", "R")
my_Char_Vec


# We can create a function in the following way
thank_you_next <- function(){
  print("Thank you")
}

# execute the function
thank_you_next()

#--------------------------------------------------
# installing and loading external packages
#--------------------------------------------------
# R has many number of helpful packages created by other users. 
# to use these packages we first need to install them using the command 
# install.packages()

# read the help on install.packages
?install.packages()

# The only argument this function takes is the name of the package 
# we want to install

# install the package "here"
install.packages('here')

# note, you only need to run this once. 
# install.packages() copies the files to your hard drive 
# but does not load the package

# to load the package use the command 'library()' or 'require()'
library('here')

# see if the package has loaded using the sessionInfo() command
sessionInfo()

#--------------------------------------------------
# File path and directories
#--------------------------------------------------
# download the IMDB movies dataframe from Canvas and move it 
# into the "datasets" folder in your home directory

# What is my current "home" directory?
getwd()

# any command where we read in a file starts at this directory
# your current home directory should be BUS_696
# if we want to open a file in the "datasets" subdirectory 
# of BUS_696 we need to reference 

# first read about what the command here does
?here()

# the here function allows us to easily load files outside of the home directory. 
# To load the IMDB_movies data frame execute the following 
movies <- read.csv(here("datasets","IMDB_movies.csv"))

#--------------------------------------------------
# Data frames
#--------------------------------------------------
# data frames are the most common object we will work with in this class
# data frames hold tabular data that we will use in our statistical analysis

# view the variables in your data frame
names(movies)

# what are the number of observations and variables in your df?
dim(movies)
# number of observations
nrow(movies)
# number of variables
ncol(movies)

# Visually explore the df
View(movies)

# quickly summarize the dataset
summary(movies)

# use "$" to refer to variables in the dataset
# what is the average box office gross of movies in our dataset?
mean(movies$gross)

# what is the average budget of movies in our dataset?
mean(movies$budget)

# why does this generate an error?
mean(movies)

# we can refer to individual observations using [] notation
# this is the first column of the first observation in the dataset
movies[1,1] 

# second observation in the third column
movies[2,3]

# this is the first column of the dataset
movies[ ,1]

# note it just printed the titles to the console
# to store it as an object we can do the following
titles <- movies[, 1]

#--------------------------------------------------
# RMarkdown
#--------------------------------------------------

# If you have time, please go to the Assignments section of 
# Canvas, and in the Problem Sets folder there is a page called 
# Problem Set RMarkdown Template. Please install RMarkdown and 
# try running and exporting a compiled .html file. 

