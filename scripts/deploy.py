#!/usr/bin/python3

from pytest import governanceToken, accounts


def main():
    return governanceToken.deploy({'from' : accounts[5]})
