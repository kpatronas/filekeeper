# filekeeper
Take backup of files based on modification time

Usage: Create a crontab entry that that will check a file (or recursivelly a directory) periodically (a configuration file maybe?), if the file have been modified a backup will be taken. Newer backups do not overwrite older ones, instead an extension with the modification timestamp is added
