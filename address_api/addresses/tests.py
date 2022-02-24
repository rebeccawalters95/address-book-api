from django.test import TestCase

# Create your tests here.

"""
Did not have time to write proper tests however, some tests that I think would be useful:
1. Make sure user cannot be created with same email address
2. Make sure that user cannot add address with same address_line_1 (additional test would be to check that 
   this is case insensitive)
3. Make sure that only authenticated users can view the data
4. Check that authenticated users can only view their OWN set of addresses (VERY important, when I figure out 
   how to add the correct permissions)
5. Check that a large number of addresses can be added (e.g. if a company is using this API and must keep track
   of all of their users addresses, they will need to store lots of data)
"""
