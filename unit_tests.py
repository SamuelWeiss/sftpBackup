import random
import unittest
import sftpbackup_util as util
import sftpBackup as master
import random
import json


# Will require some valid server credentials to test with
# these will not be stored in the local directory and will not be on git
# in order to run this testing module, valid credentials must be provided

testing_connection = json.loads(open('../testing_connection', 'r').read())

class TestUtilFunctions(unittest.TestCase):
	def setUp(self):
		self.good_prefs = {'max_size':1000000,
                           'server':"google.com",
                 		   'user':"Jim",
                           'pass':"superSecretPass",
                           'destination':'/files/backups',
                           'folder':'/home/'
                           }
        self.good_schedule = {'pattern':'repeating',
                     	      'time':3600, #in seconds - ?
                     	      'function':util.backup_folder_history,
                     	      'store':True,
                              'prefs':self.good_prefs
                              }
        self.current_dir = ['backup.log',
        					'gui.py',
        					'readme.txt',
        					'sftpBackup.py', 
        					'sftpbackup_util.py',
        					'unit_tests.py'
        					]

	def test_get_files_to_move(self):
		pass

	def test_get_target_dir_clean(self):
		self.assertEqual(util.get_target_dir_clean('.'), self.current_dir)

	def test_store_prefs(self):
		#store something arbitrary
		data = random.random()
		util.store_prefs(object)
		#read it manually
		error = False
		try:
			f = open('.sftpBackup_prefs', 'r')
			f = json.loads(f.read())
		expect Exception as e:
			error = True
		self.assertEqual(f, data)
		self.assertEqual(error, False)
		#store some good data
		util.store(self.good_schedule)
		error, data = util.read_prefs()
		self.assertEqual(error, True)
		self.assertEqual(self.good_schedule)
		#read it using read_prefs

	def test_read_prefs(self):
		# store some good data
		util.store(self.good_schedule)
		error, data = util.read_prefs()
		self.assertEqual(error, True)
		self.assertEqual(self.good_schedule)
		# retrieve it
		# store some bad data
		temp = self.good_schedule
		keys = temp.keys()
		for key in keys
			temp = self.good_schedule
			temp = {key: value for key, value in temp.items()
					  if value is not key}
			util.store_prefs(temp)
			error, data = util.read_prefs()
			self.assertEqual(error, False)
			self.assertEqual(data, {})
		# expect an error

	def test_backup_folder_history(self):
		pass

	def test_backup_folder_simple(self):
		pass

class TestMasterFunctions(unittest.TestCase):
	def setUp(self):
		self.good_prefs = {'max_size':1000000,
                           'server':"None",
                 		   'user':"None",
                           'pass':"None",
                           'destination':'None',
                           'folder':'None'
                           }
        # read credentials somehow
		self.good_schedule = {'pattern':'repeating',
                     	      'time':3600, #in seconds - ?
                     	      'function':util.backup_folder_history,
                     	      'store':True,
                              'prefs':self.good_prefs
                              }

	def test_worker(self):
		pass

	def test_scheduler(self):
		pass

	def test_confim_schedule(self):
		pass