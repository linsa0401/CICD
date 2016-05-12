#!/usr/bin/env python
# -*- coding:utf-8 -*-  

import os
import sys
import time
import commands
from optparse import OptionParser

import pytz
import boto3
import botocore
from boto3 import Session


	
def check_bucket( region , bucket_name):
	s3 = boto3.resource('s3')

	bucket = s3.Bucket(bucket_name)
	try:
		s3.meta.client.head_bucket(Bucket = bucket_name)
	except botocore.exceptions.ClientError as e:
		print "[Error] Check bucket: " ,e.response['Error']['Code'] , e.response['Error']['Message']
		sys.exit(552)
	except Exception as e:
		print " [Error] : ",e
		sys.exit(553)
	print '\n Check bucket : %s  successful !! '%bucket_name
	return s3

def upload_res( region, bucket_name, files):

	try:
		s3 = check_bucket(region , bucket_name)
		i = 1
		for file_name in files:		
			print '\n Waiting upload : %s --> %s'%(file_name ,bucket_name)
			with open(file_name , 'rb') as body:
				s3.Object(bucket_name , file_name).put( Body = body )
				print ' Upload Done  : %s --> %s \n'%(file_name , bucket_name)
			
	except Exception as e :
		print '[Error] Amazon S3 :  ',e 


def menu():

	usage = 'usage: %prog [options] '  
	parser = OptionParser(usage=usage)  
	parser.add_option('-f', '--file_name', dest='file_name',
					  default='', help='Upload files : '),  
	parser.add_option('-b', '--bucket_name',  dest='bucket_name',
					default='mk-community', help='uplload bucket : ')  
	parser.add_option('-r','--region' , dest = 'region' ,
				default='cn-north-1', help = 'Region ')

	options , args = parser.parse_args()
	return options ,args

if __name__ == '__main__':
	options ,args = menu()
	if options.file_name and options.bucket_name :
		res_code , res_content = commands.getstatusoutput('ls %s'%options.file_name)
		if res_code != 0 :
			print "[Error] : ", res_code , res_content			
			sys.exit(550)
		files = res_content.split('\n')
                print "Files : ",files
		upload_res(options.region, options.bucket_name, files )
	else:
		print '\n [Error] : pls check parameter \n' 

