from rest_framework import serializers
import re


def number_validator(password):
    if not re.findall('\d{' + str(2) + ',}', password):
        raise serializers.ValidationError("This password must contain at least 2 numbers")


def uppercase_validator(password):
    if not re.findall('[A-Z]{' + str(2) + ',}', password):
        raise serializers.ValidationError("This password must contain at least 2 uppercase letters")


def lowercase_validator(password):
    if not re.findall('[a-z]{' + str(3) + ',}', password):
        raise serializers.ValidationError("This password must contain at least 3 lowercase letters")


def symbol_validator(password):
    if not re.findall('[\(\/)\[\]\{\}\|`~!@#\$%\^&\*_\-+=;:\'",<>./?]{' + str(2) + ',}', password):
        raise serializers.ValidationError("This password must contain at least two special characters")


def is_valid(password):
    return number_validator(password) and uppercase_validator(password) and lowercase_validator(password) and symbol_validator(password)
